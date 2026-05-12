"""
Circuit Breaker pattern implementation.

Provides protection against cascading failures by temporarily
blocking calls to a failing service. Compatible with any
Python framework (sync and async).
"""

import functools
import inspect
import logging
import math
import threading
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import ParamSpec, Protocol, TypeVar, cast, overload

from taipanstack.core.result import Err

P = ParamSpec("P")
R = TypeVar("R")


class CircuitBreakerDecorator(Protocol):
    """Protocol for the circuit breaker decorator."""

    @overload
    def __call__(self, func: Callable[P, R]) -> Callable[P, R]: ...

    @overload
    def __call__(
        self, func: Callable[P, Awaitable[R]]
    ) -> Callable[P, Awaitable[R]]: ...


logger = logging.getLogger("taipanstack.resilience.circuit_breaker")

try:
    import structlog as _structlog

    _structlog_logger = _structlog.get_logger("taipanstack.resilience.circuit_breaker")
    _HAS_STRUCTLOG = True
except ImportError:
    _structlog_logger = None
    _HAS_STRUCTLOG = False


class CircuitState(Enum):
    """States of the circuit breaker."""

    CLOSED = "closed"  # Normal operation, requests flow through
    OPEN = "open"  # Circuit is tripped, requests are blocked
    HALF_OPEN = "half_open"  # Testing if service has recovered


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


@dataclass
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

    def __post_init__(self) -> None:
        """Validate configuration values."""
        if not math.isfinite(self.failure_threshold):
            raise ValueError("failure_threshold must be finite")
        if not math.isfinite(self.success_threshold):
            raise ValueError("success_threshold must be finite")
        if not math.isfinite(self.timeout):
            raise ValueError("timeout must be finite")


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
    def _check_finite_val(value: float, min_val: float, err_msg: str) -> None:
        if not math.isfinite(value) or value < min_val:
            raise ValueError(err_msg)

    @staticmethod
    def _validate_thresholds(
        timeout: float, failure_threshold: int, success_threshold: int
    ) -> None:
        CircuitBreaker._check_finite_val(
            timeout, 0, "timeout must be a finite non-negative number"
        )
        CircuitBreaker._check_finite_val(
            failure_threshold, 1, "failure_threshold must be a finite number >= 1"
        )
        CircuitBreaker._check_finite_val(
            success_threshold, 1, "success_threshold must be a finite number >= 1"
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
            timeout, failure_threshold, success_threshold
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
                error=str(e),
            )
        else:
            logger.error(
                "Circuit %s state change callback failed: %s",
                self.name,
                str(e),
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
        elif _HAS_STRUCTLOG and _structlog_logger is not None:  # pragma: no branch
            _structlog_logger.warning(
                "circuit_state_changed",
                circuit=self.name,
                old_state=old_state.value,
                new_state=new_state.value,
                failure_count=self._state.failure_count,
            )

    def _handle_open_state(
        self,
    ) -> tuple[bool, tuple[CircuitState, CircuitState] | None]:
        """Handle logic for OPEN state in _should_attempt."""
        now = time.monotonic()
        try:
            elapsed = now - self._state.last_failure_time
        except TypeError:
            # Type corruption detected (e.g. last_failure_time is string)
            return False, None

        # Safe check against NaN and Inf time corruption
        # If elapsed < 0, a backward clock jump occurred. We should
        # allow a transition to prevent permanent lockout.
        if elapsed < 0:
            elapsed = self.config.timeout

        if math.isfinite(now) and elapsed >= self.config.timeout:
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
        return False, None

    def _handle_attempt_half_open(self) -> bool:
        try:
            if not math.isfinite(self._state.half_open_attempts):
                return False
        except TypeError:
            # Type corruption detected, deny attempt to be safe
            return False

        if self._state.half_open_attempts < self.config.success_threshold:
            self._state.half_open_attempts += 1
            return True
        return False

    def _should_attempt(self) -> bool:
        """Check if a call should be attempted."""
        state_change: tuple[CircuitState, CircuitState] | None = None
        should_attempt = False

        with self._state.lock:
            match self._state.state:
                case CircuitState.CLOSED:
                    should_attempt = True
                case CircuitState.OPEN:
                    should_attempt, state_change = self._handle_open_state()
                case CircuitState.HALF_OPEN:
                    should_attempt = self._handle_attempt_half_open()

        if state_change:
            self._notify_state_change(*state_change)

        return should_attempt

    def _handle_success_half_open(self) -> tuple[CircuitState, CircuitState] | None:
        try:
            if not math.isfinite(self._state.success_count):
                self._state.success_count = 0
            self._state.success_count += 1
        except TypeError:
            # Type corruption detected, reset and increment
            self._state.success_count = 1

        if self._state.success_count >= self.config.success_threshold:
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

    def _record_success(self) -> None:
        """Record a successful call."""
        state_change: tuple[CircuitState, CircuitState] | None = None

        with self._state.lock:
            match self._state.state:
                case CircuitState.HALF_OPEN:
                    state_change = self._handle_success_half_open()
                case CircuitState.CLOSED:
                    # Reset failure count on success
                    self._state.failure_count = 0
                case CircuitState.OPEN:  # pragma: no branch
                    pass  # Should not happen, but handle gracefully

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
        try:
            if not math.isfinite(self._state.failure_count):
                self._state.state = CircuitState.OPEN
                logger.warning(
                    "Circuit %s opened due to state corruption (NaN/Inf failures)",
                    self.name,
                )
                return (CircuitState.CLOSED, CircuitState.OPEN)
        except TypeError:
            self._state.state = CircuitState.OPEN
            logger.warning(
                "Circuit %s opened due to type corruption in failure_count",
                self.name,
            )
            return (CircuitState.CLOSED, CircuitState.OPEN)

        if self._state.failure_count >= self.config.failure_threshold:
            self._state.state = CircuitState.OPEN
            logger.warning(
                "Circuit %s opened after %d failures (threshold=%d)",
                self.name,
                self._state.failure_count,
                self.config.failure_threshold,
            )
            return (CircuitState.CLOSED, CircuitState.OPEN)

        return None

    def _update_failure_metrics(self) -> None:
        try:
            if math.isfinite(self._state.failure_count):
                self._state.failure_count += 1
        except TypeError:
            # Handle type mutation (e.g. failure_count became string)
            # Safe degradation: reset to max so it opens immediately
            self._state.failure_count = self.config.failure_threshold

        now = time.monotonic()
        if math.isfinite(now):
            self._state.last_failure_time = now

    def _record_failure(self, exc: Exception) -> None:
        """Record a failed call."""
        # Check if exception should be excluded
        if isinstance(exc, self.config.excluded_exceptions):
            return

        state_change: tuple[CircuitState, CircuitState] | None = None

        with self._state.lock:
            self._update_failure_metrics()

            match self._state.state:
                case CircuitState.HALF_OPEN:
                    state_change = self._handle_failure_half_open()
                case CircuitState.CLOSED:
                    state_change = self._handle_failure_closed()
                case CircuitState.OPEN:  # pragma: no branch
                    pass  # Already open, nothing to do

        if state_change:
            self._notify_state_change(*state_change)

    def reset(self) -> None:
        """Reset circuit breaker to closed state."""
        with self._state.lock:
            self._state.state = CircuitState.CLOSED
            self._state.failure_count = 0
            self._state.success_count = 0
            self._state.half_open_attempts = 0
            logger.info("Circuit %s manually reset", self.name)

    def _process_result(self, result: R) -> R:
        """Process Result outcome and record success/failure.

        Args:
            result: The result to process.

        Returns:
            The original result.

        """
        if isinstance(result, Err):
            err_val = result.unwrap_err()
            if isinstance(err_val, self.config.failure_exceptions):
                self._record_failure(err_val)
                return result
            # Ignored exception in Result monad
            return result
        self._record_success()
        return result

    def _decrement_half_open(self, is_half_open: bool) -> None:
        """Decrement half-open attempt count if applicable.

        Args:
            is_half_open: Whether the circuit was half-open before attempt.

        """
        if is_half_open:
            with self._state.lock:
                try:
                    if (
                        self._state.state == CircuitState.HALF_OPEN
                        and math.isfinite(self._state.half_open_attempts)
                        and self._state.half_open_attempts > 0
                    ):
                        self._state.half_open_attempts -= 1
                except TypeError:
                    # Reset if state is corrupted to prevent crash
                    self._state.half_open_attempts = 0

    def __call__(
        self, func: Callable[P, R] | Callable[P, Awaitable[R]]
    ) -> Callable[P, R] | Callable[P, Awaitable[R]]:
        """Decorate a sync or async function with circuit breaker protection."""
        if inspect.iscoroutinefunction(func):
            func_coro = cast(Callable[P, Awaitable[R]], func)

            @functools.wraps(func_coro)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                if not self._should_attempt():
                    raise CircuitBreakerError(
                        f"Circuit {self.name} is open",
                        state=self._state.state,
                    )

                is_half_open = self._state.state == CircuitState.HALF_OPEN

                try:
                    result = await func_coro(*args, **kwargs)
                    return self._process_result(result)
                except self.config.failure_exceptions as e:
                    self._record_failure(e)
                    raise
                finally:
                    self._decrement_half_open(is_half_open)

            return async_wrapper

        func_sync = cast(Callable[P, R], func)

        @functools.wraps(func_sync)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            if not self._should_attempt():
                raise CircuitBreakerError(
                    f"Circuit {self.name} is open",
                    state=self._state.state,
                )

            is_half_open = self._state.state == CircuitState.HALF_OPEN

            try:
                result = func_sync(*args, **kwargs)
                return self._process_result(result)
            except self.config.failure_exceptions as e:
                self._record_failure(e)
                raise
            finally:
                self._decrement_half_open(is_half_open)

        return wrapper


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
            name=name or func.__name__,
            on_state_change=on_state_change,
        )
        return breaker(func)

    return cast(CircuitBreakerDecorator, decorator)
