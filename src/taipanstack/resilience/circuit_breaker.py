"""
Circuit Breaker pattern implementation.

Provides protection against cascading failures by temporarily
blocking calls to a failing service. Compatible with any
Python framework (sync and async).
"""

import contextlib
import functools
import inspect
import logging
import math
import threading
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import (
    TYPE_CHECKING,
    ParamSpec,
    Protocol,
    TypeGuard,
    TypeVar,
    cast,
    overload,
)

from taipanstack.core.result import Err

P = ParamSpec("P")
R = TypeVar("R")


class CircuitBreakerDecorator(Protocol):
    """Protocol for the circuit breaker decorator."""

    @overload
    def __call__(self, func: Callable[P, R]) -> Callable[P, R]: ...

    @overload
    def __call__(
        self,
        func: Callable[P, Awaitable[R]],
    ) -> Callable[P, Awaitable[R]]: ...


logger = logging.getLogger("taipanstack.resilience.circuit_breaker")

if TYPE_CHECKING:

    class StructlogProtocol(Protocol):
        """Protocol for structural logging to appease static checkers."""

        def error(self, _event: str, **kwargs: object) -> None:
            """Log an error event."""
            ...

        def warning(self, _event: str, **kwargs: object) -> None:
            """Log a warning event."""
            ...
else:
    StructlogProtocol = object

try:
    import structlog as _structlog

    _structlog_logger: StructlogProtocol | None = cast(
        StructlogProtocol,
        _structlog.get_logger("taipanstack.resilience.circuit_breaker"),
    )
    _HAS_STRUCTLOG = True
except ImportError:
    _structlog_logger = None
    _HAS_STRUCTLOG = False


class CircuitState(Enum):
    """States of the circuit breaker."""

    CLOSED = "closed"  # Normal operation, requests flow through
    OPEN = "open"  # Circuit is tripped, requests are blocked
    HALF_OPEN = "half_open"  # Testing if service has recovered


def _safe_str(e: Exception) -> str:
    try:
        return str(e)
    except Exception:
        try:
            return repr(e)
        except Exception:
            return "<unprintable exception>"


class CircuitBreakerError(Exception):
    """Raised when circuit breaker is open."""

    def __init__(self, message: str, state: CircuitState) -> None:
        """Initialize CircuitBreakerError.

        Args:
            message: Error description.
            state: Current circuit state.

        """
        self.state = state
        super().__init__(message)


@dataclass(frozen=True)
class CircuitBreakerConfig:
    """Configuration for circuit breaker behavior.

    Attributes:
        failure_threshold: Number of failures before opening circuit.
        success_threshold: Successes needed in half-open to close.
        timeout: Seconds before trying half-open after open.
        excluded_exceptions: Exceptions that don't count as failures.
        failure_exceptions: Exceptions that count as failures.

    """

    failure_threshold: int = 5
    success_threshold: int = 2
    timeout: float = 30.0
    excluded_exceptions: tuple[type[Exception], ...] = ()
    failure_exceptions: tuple[type[Exception], ...] = (Exception,)

    def _check_finite(self, value: int | float, name: str) -> None:
        if type(value) not in (int, float):
            raise TypeError(f"{name} must be of type int or float")
        # type narrowing for type checker
        val = float(value)
        if not math.isfinite(val) or val < 0:
            raise ValueError(f"{name} must be finite and non-negative")

    def __post_init__(self) -> None:
        """Validate configuration values."""
        self._check_finite(self.failure_threshold, "failure_threshold")
        self._check_finite(self.success_threshold, "success_threshold")
        self._check_finite(self.timeout, "timeout")


@dataclass
class CircuitBreakerState:
    """Internal state tracking for circuit breaker."""

    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    success_count: int = 0
    half_open_attempts: int = 0
    last_failure_time: float = 0.0
    lock: threading.Lock = field(default_factory=threading.Lock)


class CircuitBreaker:
    """Circuit breaker implementation.

    Monitors function calls and opens the circuit when too many
    failures occur, preventing further calls until the service
    recovers. Supports both sync and async functions.

    Example:
        >>> breaker = CircuitBreaker(failure_threshold=3)
        >>> @breaker
        ... def call_external_api():
        ...     return requests.get("https://api.example.com", timeout=10)

    """

    @staticmethod
    def _is_valid_metric(value: object, min_val: float = 0) -> TypeGuard[int | float]:
        """Check if metric is a valid finite number >= min_val."""
        if not isinstance(value, (int, float)):
            return False
        try:
            return math.isfinite(value) and value >= min_val
        except Exception:
            return False

    @staticmethod
    def _get_safe_threshold(value: object, min_val: float, default: float) -> float:
        """Return the threshold if valid, otherwise return the default."""
        if CircuitBreaker._is_valid_metric(value, min_val):
            return float(value)
        return default

    @staticmethod
    def _check_finite_val(value: float, min_val: float, err_msg: str) -> None:
        if (
            not isinstance(value, (int, float))
            or not math.isfinite(value)
            or value < min_val
        ):
            raise ValueError(err_msg)

    @staticmethod
    def _validate_thresholds(
        timeout: float,
        failure_threshold: int,
        success_threshold: int,
    ) -> None:
        CircuitBreaker._check_finite_val(
            timeout,
            0,
            "timeout must be a finite non-negative number",
        )
        CircuitBreaker._check_finite_val(
            failure_threshold,
            1,
            "failure_threshold must be a finite number >= 1",
        )
        CircuitBreaker._check_finite_val(
            success_threshold,
            1,
            "success_threshold must be a finite number >= 1",
        )

    def __init__(
        self,
        *,
        failure_threshold: int = 5,
        success_threshold: int = 2,
        timeout: float = 30.0,
        excluded_exceptions: tuple[type[Exception], ...] = (),
        failure_exceptions: tuple[type[Exception], ...] = (Exception,),
        name: str = "default",
        on_state_change: Callable[[CircuitState, CircuitState], None] | None = None,
    ) -> None:
        """Initialize CircuitBreaker.

        Args:
            failure_threshold: Failures before opening circuit.
            success_threshold: Successes to close from half-open.
            timeout: Seconds before attempting half-open.
            excluded_exceptions: Exceptions that don't trip circuit.
            failure_exceptions: Exceptions that count as failures.
            name: Name for logging/identification.
            on_state_change: Optional callback invoked on state transitions
                with (old_state, new_state). Useful for custom monitoring.

        """
        CircuitBreaker._validate_thresholds(
            timeout,
            failure_threshold,
            success_threshold,
        )

        self.config = CircuitBreakerConfig(
            failure_threshold=failure_threshold,
            success_threshold=success_threshold,
            timeout=timeout,
            excluded_exceptions=excluded_exceptions,
            failure_exceptions=failure_exceptions,
        )
        self.name = name
        self._state = CircuitBreakerState()
        self._on_state_change = on_state_change

    @property
    def state(self) -> CircuitState:
        """Get current circuit state."""
        return self._state.state

    @property
    def failure_count(self) -> int:
        """Get current failure count."""
        return self._state.failure_count

    @property
    def is_closed(self) -> bool:
        """Check if circuit is closed."""
        return self._state.state == CircuitState.CLOSED

    @property
    def is_open(self) -> bool:
        """Check if circuit is open."""
        return self._state.state == CircuitState.OPEN

    @property
    def is_half_open(self) -> bool:
        """Check if circuit is half-open."""
        return self._state.state == CircuitState.HALF_OPEN

    def _log_callback_failure(
        self,
        old_state: CircuitState,
        new_state: CircuitState,
        e: Exception,
    ) -> None:
        if _HAS_STRUCTLOG and _structlog_logger is not None:
            _structlog_logger.error(
                "circuit_state_change_callback_failed",
                circuit=self.name,
                old_state=old_state.value,
                new_state=new_state.value,
                error=_safe_str(e),
            )
        else:
            logger.error(
                "Circuit %s state change callback failed: %s",
                self.name,
                _safe_str(e),
            )

    def _log_structlog_warning(
        self,
        old_state: CircuitState,
        new_state: CircuitState,
    ) -> None:
        if _HAS_STRUCTLOG and _structlog_logger is not None:
            _structlog_logger.warning(
                "circuit_state_changed",
                circuit=self.name,
                old_state=old_state.value,
                new_state=new_state.value,
                failure_count=self._state.failure_count,
            )

    def _notify_state_change(
        self,
        old_state: CircuitState,
        new_state: CircuitState,
    ) -> None:
        """Notify callback of state transition if registered.

        Emit a structured log via structlog when no callback is provided
        and structlog is available.
        """
        if self._on_state_change is not None:
            try:
                self._on_state_change(old_state, new_state)
            except Exception as e:
                self._log_callback_failure(old_state, new_state, e)
            return

        self._log_structlog_warning(old_state, new_state)

    def _get_safe_timeout(self) -> float:
        try:
            return float(self.config.timeout)
        except (TypeError, ValueError):
            return 30.0

    def _is_valid_failure_val(self, val: float, now: float) -> bool:
        return math.isfinite(val) and now - val >= 0

    def _calculate_safe_elapsed(
        self, parsed_failure: float | int, safe_timeout: float, now: float
    ) -> float:
        try:
            val = float(parsed_failure)
            if self._is_valid_failure_val(val, now):
                return now - val
            return safe_timeout
        except Exception:
            return safe_timeout

    def _compute_elapsed(
        self, last_failure: float | None, safe_timeout: float, now: float
    ) -> float | None:
        if not isinstance(last_failure, (int, float)):
            return None
        return self._calculate_safe_elapsed(last_failure, safe_timeout, now)

    def _calculate_elapsed_time(self, now: float) -> float | None:
        """Calculate time elapsed since last failure."""
        return self._compute_elapsed(
            self._state.last_failure_time, self._get_safe_timeout(), now
        )

    def _transition_to_half_open(
        self,
        elapsed: float,
    ) -> tuple[bool, tuple[CircuitState, CircuitState] | None]:
        """Transition the circuit to half-open state."""
        # Before transitioning, verify if we can make an attempt
        # This happens in a lock, so it's thread-safe. However, once
        # the state changes to HALF_OPEN, subsequent threads in the
        # same lock block will hit the HALF_OPEN case.
        self._state.state = CircuitState.HALF_OPEN
        self._state.success_count = 0
        # Initialize half_open_attempts to 1 because this first call
        # that transitions the state is also an attempt.
        self._state.half_open_attempts = 1
        logger.info(
            "Circuit %s entering half-open state (was open for %.1fs, failures=%d)",
            self.name,
            elapsed,
            self._state.failure_count,
        )
        return True, (CircuitState.OPEN, CircuitState.HALF_OPEN)

    def _evaluate_open_timeout(
        self,
        elapsed: float,
    ) -> tuple[bool, tuple[CircuitState, CircuitState] | None]:
        timeout = self._get_safe_threshold(self.config.timeout, 0, 30.0)
        if elapsed >= timeout:
            return self._transition_to_half_open(elapsed)
        return False, None

    def _is_valid_monotonic_time(self, now: float) -> bool:
        return isinstance(now, (int, float)) and math.isfinite(now)

    def _get_valid_elapsed(self) -> float | None:
        try:
            now = time.monotonic()
            if self._is_valid_monotonic_time(now):
                return self._calculate_elapsed_time(now)
            return None
        except Exception:
            return None

    def _handle_open_state(
        self,
    ) -> tuple[bool, tuple[CircuitState, CircuitState] | None]:
        """Handle logic for OPEN state in _should_attempt."""
        elapsed = self._get_valid_elapsed()
        if elapsed is None:
            return False, None
        return self._evaluate_open_timeout(elapsed)

    def _handle_attempt_half_open(self) -> bool:
        if not self._is_valid_metric(self._state.half_open_attempts):
            return False

        success_threshold = self._get_safe_threshold(
            self.config.success_threshold,
            1,
            2,
        )

        if self._state.half_open_attempts < success_threshold:
            self._state.half_open_attempts += 1
            return True
        return False

    def _acquire_lock(self) -> bool:
        """Safely attempt to acquire the lock."""
        try:
            return self._state.lock.acquire(timeout=0.1)
        except Exception:
            return False

    def _safe_release(self) -> None:
        with contextlib.suppress(Exception):
            self._state.lock.release()

    def _process_state(
        self, state: CircuitState
    ) -> tuple[bool, tuple[CircuitState, CircuitState] | None]:
        if state is CircuitState.OPEN:
            return self._handle_open_state()
        if state is CircuitState.HALF_OPEN:
            return self._handle_attempt_half_open(), None
        return False, None

    def _evaluate_state_for_attempt(
        self,
    ) -> tuple[bool, tuple[CircuitState, CircuitState] | None]:
        state = self._state.state
        if state is CircuitState.CLOSED:
            return True, None
        return self._process_state(state)

    def _should_attempt(self) -> bool:
        """Check if a call should be attempted."""
        if not self._acquire_lock():
            return False
        try:
            should_attempt, state_change = self._evaluate_state_for_attempt()
        finally:
            self._safe_release()

        if state_change:
            self._notify_state_change(*state_change)

        return should_attempt

    def _handle_success_half_open(self) -> tuple[CircuitState, CircuitState] | None:
        if not self._is_valid_metric(self._state.success_count):
            # Type corruption detected, reset and increment
            self._state.success_count = 1
        else:
            self._state.success_count += 1

        success_threshold = self._get_safe_threshold(
            self.config.success_threshold,
            1,
            2,
        )

        if self._state.success_count >= success_threshold:
            self._state.state = CircuitState.CLOSED
            self._state.failure_count = 0
            self._state.half_open_attempts = 0
            logger.info(
                "Circuit %s closed after recovery (%d consecutive successes)",
                self.name,
                self._state.success_count,
            )
            return (CircuitState.HALF_OPEN, CircuitState.CLOSED)
        return None

    def _get_success_state_change(self) -> tuple[CircuitState, CircuitState] | None:
        state = self._state.state
        if state is CircuitState.HALF_OPEN:
            return self._handle_success_half_open()
        if state is CircuitState.CLOSED:
            # Reset failure count on success
            self._state.failure_count = 0
            return None
        return None

    def _record_success(self) -> None:
        """Record a successful call."""
        if not self._acquire_lock():
            return
        try:
            state_change = self._get_success_state_change()
        finally:
            self._safe_release()

        if state_change:
            self._notify_state_change(*state_change)

    def _handle_failure_half_open(self) -> tuple[CircuitState, CircuitState] | None:
        """Handle failure when in HALF_OPEN state."""
        self._state.state = CircuitState.OPEN
        self._state.half_open_attempts = 0
        logger.warning(
            "Circuit %s reopened after failure in half-open",
            self.name,
        )
        return (CircuitState.HALF_OPEN, CircuitState.OPEN)

    def _handle_failure_closed(self) -> tuple[CircuitState, CircuitState] | None:
        """Handle failure when in CLOSED state."""
        # Check against corrupted NaN/Inf failure_count
        if not self._is_valid_metric(self._state.failure_count):
            self._state.state = CircuitState.OPEN
            logger.warning(
                "Circuit %s opened due to state/type corruption in failure_count",
                self.name,
            )
            return (CircuitState.CLOSED, CircuitState.OPEN)

        failure_threshold = self._get_safe_threshold(
            self.config.failure_threshold,
            1,
            5,
        )

        if self._state.failure_count >= failure_threshold:
            self._state.state = CircuitState.OPEN
            logger.warning(
                "Circuit %s opened after %d failures (threshold=%d)",
                self.name,
                self._state.failure_count,
                failure_threshold,
            )
            return (CircuitState.CLOSED, CircuitState.OPEN)

        return None

    def _increment_failure_count(self) -> None:
        if not self._is_valid_metric(self._state.failure_count):
            # Handle type mutation (e.g. failure_count became string) or Inf/NaN
            # Safe degradation: reset to max so it opens immediately
            self._state.failure_count = self.config.failure_threshold
        else:
            self._state.failure_count += 1

    def _try_get_monotonic(self) -> float:
        try:
            return time.monotonic()
        except Exception:
            return float("nan")

    def _update_failure_metrics(self) -> None:
        self._increment_failure_count()
        now = self._try_get_monotonic()
        if isinstance(now, (int, float)) and math.isfinite(now):
            self._state.last_failure_time = now

    def _get_failure_state_change(self) -> tuple[CircuitState, CircuitState] | None:
        """Get state change for a failure."""
        if self._state.state is CircuitState.HALF_OPEN:
            return self._handle_failure_half_open()
        if self._state.state is CircuitState.CLOSED:
            return self._handle_failure_closed()
        return None

    def _is_excluded_exception(self, exc: Exception) -> bool:
        try:
            return isinstance(exc, self.config.excluded_exceptions)
        except TypeError:
            return False

    def _process_failure_with_lock(self) -> tuple[CircuitState, CircuitState] | None:
        self._update_failure_metrics()
        return self._get_failure_state_change()

    def _try_process_failure_change(self) -> tuple[CircuitState, CircuitState] | None:
        try:
            return self._process_failure_with_lock()
        finally:
            self._safe_release()

    def _execute_failure_record(self) -> None:
        if self._acquire_lock():
            state_change = self._try_process_failure_change()
            if state_change:
                self._notify_state_change(*state_change)

    def _record_failure(self, exc: Exception) -> None:
        """Record a failed call."""
        if not self._is_excluded_exception(exc):
            self._execute_failure_record()

    def _apply_reset_state(self) -> tuple[CircuitState, CircuitState] | None:
        old_state = self._state.state
        state_change = (
            (old_state, CircuitState.CLOSED)
            if old_state is not CircuitState.CLOSED
            else None
        )

        self._state.state = CircuitState.CLOSED
        self._state.failure_count = 0
        self._state.success_count = 0
        self._state.half_open_attempts = 0
        logger.info("Circuit %s manually reset", self.name)
        return state_change

    def reset(self) -> None:
        """Reset circuit breaker to closed state."""
        state_change: tuple[CircuitState, CircuitState] | None = None
        if not self._acquire_lock():
            return
        try:
            state_change = self._apply_reset_state()
        finally:
            self._safe_release()

        if state_change:
            self._notify_state_change(*state_change)

    def _is_failure_exception(self, exc: Exception) -> bool:
        try:
            return isinstance(exc, self.config.failure_exceptions)
        except TypeError:
            return True

    def _process_result(self, result: R) -> R:
        """Process Result outcome and record success/failure.

        Args:
            result: The result to process.

        Returns:
            The original result.

        """
        if isinstance(result, Err):
            err_val = result.unwrap_err()
            if self._is_failure_exception(err_val):
                self._record_failure(err_val)
                return result
            # Ignored exception in Result monad
            return result
        self._record_success()
        return result

    def _check_half_open_value(self, val: float | int) -> bool:
        try:
            return math.isfinite(val) and val >= 0
        except Exception:
            return False

    def _is_valid_half_open_attempts(self) -> bool:
        """Validate half-open attempts value against corruption."""
        val = self._state.half_open_attempts
        if not isinstance(val, (int, float)):
            return False  # type: ignore[unreachable]
        return self._check_half_open_value(val)

    def _apply_half_open_decrement(self) -> None:
        if not self._is_valid_half_open_attempts():
            # Reset if state is corrupted to prevent crash
            self._state.half_open_attempts = 0
        elif self._state.half_open_attempts > 0:
            self._state.half_open_attempts -= 1

    def _safe_decrement_half_open_attempts(self) -> None:
        """Safely decrement half-open attempts."""
        if self._state.state is CircuitState.HALF_OPEN:
            self._apply_half_open_decrement()

    def _try_acquire_lock_for_decrement(self) -> bool:
        try:
            return self._state.lock.acquire(timeout=0.1)
        except Exception:
            return False

    def _decrement_half_open(self, is_half_open: bool) -> None:
        """Decrement half-open attempt count if applicable."""
        if is_half_open and self._try_acquire_lock_for_decrement():
            try:
                self._safe_decrement_half_open_attempts()
            finally:
                self._safe_release()

    def _handle_exception_in_call(self, e: Exception) -> None:
        try:
            is_failure = isinstance(e, self.config.failure_exceptions)
        except TypeError:
            is_failure = True
        if is_failure:
            self._record_failure(e)

    def _check_should_attempt_or_raise(self) -> None:
        if not self._should_attempt():
            raise CircuitBreakerError(
                f"Circuit {self.name} is open",
                state=self._state.state,
            )

    async def _run_coro_and_process(
        self, func_coro: Callable[..., Awaitable[R]], *args: object, **kwargs: object
    ) -> R:
        try:
            result = await func_coro(*args, **kwargs)
            return self._process_result(result)
        except Exception as e:
            self._handle_exception_in_call(e)
            raise

    def _execute_async_wrapper(
        self,
        func_coro: Callable[P, Awaitable[R]],
    ) -> Callable[P, Awaitable[R]]:
        @functools.wraps(func_coro)
        async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            self._check_should_attempt_or_raise()
            is_half_open = self._state.state is CircuitState.HALF_OPEN

            try:
                return await self._run_coro_and_process(func_coro, *args, **kwargs)
            finally:
                self._decrement_half_open(is_half_open)

        return async_wrapper  # type: ignore[misc]

    def _run_sync_and_process(
        self, func_sync: Callable[..., R], *args: object, **kwargs: object
    ) -> R:
        try:
            result = func_sync(*args, **kwargs)
            return self._process_result(result)
        except Exception as e:
            self._handle_exception_in_call(e)
            raise

    def _execute_sync_wrapper(
        self,
        func_sync: Callable[P, R],
    ) -> Callable[P, R]:
        @functools.wraps(func_sync)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            self._check_should_attempt_or_raise()
            is_half_open = self._state.state is CircuitState.HALF_OPEN

            try:
                return self._run_sync_and_process(func_sync, *args, **kwargs)
            finally:
                self._decrement_half_open(is_half_open)

        return wrapper

    def __call__(
        self,
        func: Callable[P, R] | Callable[P, Awaitable[R]],
    ) -> Callable[P, R] | Callable[P, Awaitable[R]]:
        """Decorate a sync or async function with circuit breaker protection."""
        if inspect.iscoroutinefunction(func):
            func_coro = cast(Callable[P, Awaitable[R]], func)
            return self._execute_async_wrapper(func_coro)

        func_sync = cast(Callable[P, R], func)
        return self._execute_sync_wrapper(func_sync)


def circuit_breaker(
    *,
    failure_threshold: int = 5,
    success_threshold: int = 2,
    timeout: float = 30.0,
    excluded_exceptions: tuple[type[Exception], ...] = (),
    failure_exceptions: tuple[type[Exception], ...] = (Exception,),
    name: str | None = None,
    on_state_change: Callable[[CircuitState, CircuitState], None] | None = None,
) -> CircuitBreakerDecorator:
    """Decorate a sync or async function with circuit breaker pattern.

    Args:
        failure_threshold: Failures before opening circuit.
        success_threshold: Successes to close from half-open.
        timeout: Seconds before attempting half-open.
        excluded_exceptions: Exceptions that don't trip circuit.
        failure_exceptions: Exceptions that count as failures.
        name: Optional name for the circuit.
        on_state_change: Optional callback invoked on state transitions
            with (old_state, new_state).

    Returns:
        Decorated function with circuit breaker protection.

    Example:
        >>> @circuit_breaker(failure_threshold=3, timeout=60)
        ... def call_api(endpoint: str) -> dict:
        ...     return requests.get(endpoint, timeout=10).json()

        >>> @circuit_breaker(
        ...     failure_threshold=3,
        ...     on_state_change=lambda old, new: print(f"{old} -> {new}"),
        ... )
        ... def monitored_call() -> str:
        ...     return service.call()

    """

    def decorator(
        func: Callable[P, R] | Callable[P, Awaitable[R]],
    ) -> Callable[P, R] | Callable[P, Awaitable[R]]:
        breaker = CircuitBreaker(
            failure_threshold=failure_threshold,
            success_threshold=success_threshold,
            timeout=timeout,
            excluded_exceptions=excluded_exceptions,
            failure_exceptions=failure_exceptions,
            name=name or cast(str, getattr(func, "__name__", "unknown")),
            on_state_change=on_state_change,
        )
        return breaker(func)

    return cast(CircuitBreakerDecorator, decorator)
