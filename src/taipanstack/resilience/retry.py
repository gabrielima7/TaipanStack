"""
Retry logic with exponential backoff.

Provides decorators for automatic retry of failing operations
with configurable backoff strategies. Compatible with any
Python framework (sync and async).
"""

import asyncio
import functools
import inspect
import logging
import math
import secrets
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from types import TracebackType
from typing import NoReturn, ParamSpec, Protocol, TypeVar, cast, overload

from taipanstack.core.result import Err

P = ParamSpec("P")
R = TypeVar("R")


class RetryDecorator(Protocol):
    """Protocol for the retry decorator."""

    @overload
    def __call__(self, func: Callable[P, R]) -> Callable[P, R]: ...

    @overload
    def __call__(
        self, func: Callable[P, Awaitable[R]]
    ) -> Callable[P, Awaitable[R]]: ...


logger = logging.getLogger("taipanstack.resilience.retry")

try:
    import structlog as _structlog

    _structlog_logger = _structlog.get_logger("taipanstack.resilience.retry")
    _HAS_STRUCTLOG = True
except ImportError:
    _structlog_logger = None
    _HAS_STRUCTLOG = False


def _validate_finite_or_default(
    obj: object, attr_name: str, default_val: float | int
) -> None:
    """Validate that an attribute is finite, falling back to a default."""
    try:
        val = cast(float | int, getattr(obj, attr_name))
        if not math.isfinite(val):
            raise ValueError(f"{attr_name} must be a finite number")
    except TypeError:
        object.__setattr__(obj, attr_name, default_val)


@dataclass(frozen=True)
class RetryConfig:
    """Configuration for retry behavior.

    Attributes:
        max_attempts: Maximum number of retry attempts.
        initial_delay: Initial delay between retries in seconds.
        max_delay: Maximum delay between retries.
        exponential_base: Base for exponential backoff (2 = double each time).
        jitter: Whether to add random jitter to delays.
        jitter_factor: Maximum jitter as fraction of delay (0.1 = 10%).
        log_retries: Whether to emit standard log messages.
        on_retry: Optional callback invoked on each retry.

    """

    max_attempts: int = 3
    initial_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True
    jitter_factor: float = 0.1
    log_retries: bool = True
    on_retry: Callable[[int, int, Exception, float], None] | None = None

    def __post_init__(self) -> None:
        """Validate configuration parameters."""
        _validate_finite_or_default(self, "max_attempts", 3)
        _validate_finite_or_default(self, "initial_delay", 1.0)
        _validate_finite_or_default(self, "max_delay", 60.0)
        _validate_finite_or_default(self, "exponential_base", 2.0)
        _validate_finite_or_default(self, "jitter_factor", 0.1)


class RetryError(Exception):
    """Raised when all retry attempts have failed."""

    def __init__(
        self,
        message: str,
        attempts: int,
        last_exception: Exception | None = None,
    ) -> None:
        """Initialize RetryError.

        Args:
            message: Description of the retry failure.
            attempts: Number of attempts made.
            last_exception: The last exception that was raised.

        """
        self.attempts = attempts
        self.last_exception = last_exception
        super().__init__(message)


def _calculate_base_delay(attempt: int, config: RetryConfig) -> float:
    """Calculate base delay with exponential backoff."""
    safe_attempt = max(1, attempt)
    try:
        delay = config.initial_delay * (config.exponential_base ** (safe_attempt - 1))
        if not math.isfinite(delay):
            delay = config.max_delay
    except (OverflowError, TypeError):
        delay = config.max_delay

    try:
        if not math.isfinite(delay):
            delay = 0.0
        return min(delay, config.max_delay)
    except TypeError:
        return 0.0


def _compute_jitter_amount(delay: float, factor: float) -> float | None:
    """Compute jitter amount safely."""
    try:
        amount = delay * factor
        if math.isfinite(amount):
            return amount
    except (TypeError, OverflowError, ValueError, Exception) as e:
        logger.warning("Failed to add jitter to delay due to mutation: %s", str(e))
    return None


def _apply_jitter(delay: float, config: RetryConfig) -> float:
    """Apply jitter to delay."""
    if not config.jitter or not math.isfinite(delay):
        return delay

    jitter_amount = _compute_jitter_amount(delay, config.jitter_factor)
    if jitter_amount is not None:
        try:
            delay += secrets.SystemRandom().uniform(-jitter_amount, jitter_amount)
        except Exception as e:
            logger.warning("Failed to add jitter to delay: %s", str(e))

    return delay


def calculate_delay(
    attempt: int,
    config: RetryConfig,
) -> float:
    """Calculate delay before next retry.

    Args:
        attempt: Current attempt number (1-indexed).
        config: Retry configuration.

    Returns:
        Delay in seconds before next retry.

    """
    delay = _calculate_base_delay(attempt, config)
    delay = _apply_jitter(delay, config)

    if not math.isfinite(delay) or delay < 0:
        return 0.0

    return delay


def _log_retry_callback_failure(func_name: str, e: Exception) -> None:
    """Log a failure during the retry callback execution."""
    if _HAS_STRUCTLOG and _structlog_logger is not None:
        _structlog_logger.error(
            "retry_callback_failed",
            function=func_name,
            error=str(e),
        )
    else:
        logger.error(
            "Retry callback failed for %s: %s",
            func_name,
            str(e),
        )


def _log_retry_attempt_fallback(
    func_name: str,
    attempt: int,
    exc: Exception,
    delay: float,
    config: RetryConfig,
) -> None:
    """Log the retry attempt if no callback is provided."""
    if _HAS_STRUCTLOG and _structlog_logger is not None:
        _structlog_logger.warning(
            "retry_attempted",
            function=func_name,
            attempt=attempt,
            max_attempts=config.max_attempts,
            error=str(exc),
            delay_seconds=round(delay, 3),
        )


def _invoke_retry_callback(
    func_name: str,
    attempt: int,
    exc: Exception,
    delay: float,
    config: RetryConfig,
) -> None:
    """Invoke the retry callback if set, or emit structured log.

    Args:
        func_name: Name of the retried function.
        attempt: Current attempt number.
        exc: The exception that triggered the retry.
        delay: Delay in seconds before the next attempt.
        config: Retry configuration.

    """
    if config.on_retry is not None:
        try:
            config.on_retry(attempt, config.max_attempts, exc, delay)
        except Exception as e:
            _log_retry_callback_failure(func_name, e)
    else:
        _log_retry_attempt_fallback(func_name, attempt, exc, delay, config)


def _log_retry_attempt(
    func_name: str,
    attempt: int,
    exc: Exception,
    delay: float,
    config: RetryConfig,
) -> None:
    """Log a retry attempt via callback, structlog, or stdlib logger.

    Args:
        func_name: Name of the retried function.
        attempt: Current attempt number.
        exc: The exception that triggered the retry.
        delay: Delay in seconds before the next attempt.
        config: Retry configuration.

    """
    if config.log_retries:
        logger.info(
            "Attempt %d/%d failed for %s: %s. Retrying in %.2f seconds...",
            attempt,
            config.max_attempts,
            func_name,
            str(exc),
            delay,
        )

    _invoke_retry_callback(func_name, attempt, exc, delay, config)


def _log_all_failed(
    func_name: str,
    exc: Exception,
    config: RetryConfig,
) -> None:
    """Log when all retry attempts have been exhausted.

    Args:
        func_name: Name of the retried function.
        exc: The last exception raised.
        config: Retry configuration.

    """
    if config.log_retries:
        logger.warning(
            "All %d attempts failed for %s: %s",
            config.max_attempts,
            func_name,
            str(exc),
        )


def _raise_retry_error(
    func_name: str,
    max_attempts: int,
    reraise: bool,
    last_exception: Exception | None,
) -> NoReturn:
    """Raise a RetryError after all attempts fail.

    Args:
        func_name: Name of the retried function.
        max_attempts: Number of attempts made.
        reraise: Whether to reraise the original exception.
        last_exception: The last exception that was raised.

    Raises:
        RetryError: The wrapped or unwrapped exception.

    """
    if reraise and last_exception is not None:
        raise RetryError(
            f"All {max_attempts} attempts failed for {func_name}",
            attempts=max_attempts,
            last_exception=last_exception,
        ) from last_exception

    raise RetryError(
        f"All {max_attempts} attempts failed for {func_name}",
        attempts=max_attempts,
        last_exception=last_exception,
    )


def retry(  # noqa: PLR0915
    *,
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    on: tuple[type[Exception], ...] = (Exception,),
    reraise: bool = True,
    log_retries: bool = True,
    on_retry: Callable[[int, int, Exception, float], None] | None = None,
) -> RetryDecorator:
    """Retry a sync or async function with exponential backoff.

    Automatically retries the decorated function when specified
    exceptions are raised, with configurable backoff strategy.
    Detects coroutine functions and preserves their async nature.

    Args:
        max_attempts: Maximum number of retry attempts.
        initial_delay: Initial delay between retries in seconds.
        max_delay: Maximum delay between retries.
        exponential_base: Base for exponential backoff.
        jitter: Whether to add random jitter to delays.
        on: Exception types to retry on.
        reraise: Whether to reraise the last exception on failure.
        log_retries: Whether to log retry attempts.
        on_retry: Optional callback invoked on each retry with
            (attempt, max_attempts, exception, delay). Useful for
            custom monitoring or metrics collection.

    Returns:
        Decorated function with retry logic.

    Example:
        >>> @retry(max_attempts=3, on=(ConnectionError, TimeoutError))
        ... def fetch_data(url: str) -> dict:
        ...     return requests.get(url, timeout=10).json()

        >>> @retry(max_attempts=3, on_retry=lambda a, m, e, d: print(f"Retry {a}/{m}"))
        ... def fragile_operation() -> str:
        ...     return do_something()

    """
    config = RetryConfig(
        max_attempts=max_attempts,
        initial_delay=initial_delay,
        max_delay=max_delay,
        exponential_base=exponential_base,
        jitter=jitter,
        log_retries=log_retries,
        on_retry=on_retry,
    )

    def decorator(  # noqa: PLR0915
        func: Callable[P, R] | Callable[P, Awaitable[R]],
    ) -> Callable[P, R] | Callable[P, Awaitable[R]]:
        if inspect.iscoroutinefunction(func):
            func_coro = cast(Callable[P, Awaitable[R]], func)

            @functools.wraps(func_coro)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                last_exception: Exception | None = None
                last_result: R | None = None

                for attempt in range(1, max_attempts + 1):
                    last_result = None
                    try:
                        last_result = await func_coro(*args, **kwargs)
                        if isinstance(last_result, Err):
                            err_val = last_result.unwrap_err()
                            try:
                                if isinstance(err_val, on):
                                    raise err_val
                            except TypeError:
                                pass
                        return last_result
                    except BaseException as e:
                        try:
                            if not isinstance(e, on):
                                raise
                        except TypeError:
                            raise e from None
                        last_exception = e if isinstance(e, Exception) else None

                        if attempt == max_attempts:
                            _log_all_failed(
                                func_coro.__name__,
                                e,
                                config,
                            )
                            break

                        delay = calculate_delay(attempt, config)
                        _log_retry_attempt(
                            func_coro.__name__,
                            attempt,
                            e,
                            delay,
                            config,
                        )
                        await asyncio.sleep(min(delay, 3600.0))

                if last_result is not None and isinstance(last_result, Err):
                    return cast(R, last_result)
                _raise_retry_error(
                    func_coro.__name__,
                    max_attempts,
                    reraise,
                    last_exception,
                )

            return async_wrapper

        func_sync = cast(Callable[P, R], func)

        @functools.wraps(func_sync)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exception: Exception | None = None
            last_result: R | None = None

            for attempt in range(1, max_attempts + 1):
                last_result = None
                try:
                    last_result = func_sync(*args, **kwargs)
                    if isinstance(last_result, Err):
                        err_val = last_result.unwrap_err()
                        try:
                            if isinstance(err_val, on):
                                raise err_val
                        except TypeError:
                            pass
                    return last_result
                except BaseException as e:
                    try:
                        if not isinstance(e, on):
                            raise
                    except TypeError:
                        raise e from None
                    last_exception = e if isinstance(e, Exception) else None

                    if attempt == max_attempts:
                        _log_all_failed(
                            func_sync.__name__,
                            e,
                            config,
                        )
                        break

                    # Calculate delay and wait
                    delay = calculate_delay(attempt, config)
                    _log_retry_attempt(
                        func_sync.__name__,
                        attempt,
                        e,
                        delay,
                        config,
                    )
                    time.sleep(min(delay, 3600.0))

            if last_result is not None and isinstance(last_result, Err):
                return cast(R, last_result)
            _raise_retry_error(
                func_sync.__name__,
                max_attempts,
                reraise,
                last_exception,
            )

        return wrapper

    return cast(RetryDecorator, decorator)


def retry_on_exception(
    exception_types: tuple[type[Exception], ...],
    max_attempts: int = 3,
) -> RetryDecorator:
    """Retry on specific exceptions.

    A simpler alternative to the full retry decorator when you
    just need basic retry functionality.

    Args:
        exception_types: Exception types to retry on.
        max_attempts: Maximum number of attempts.

    Returns:
        Decorated function with retry logic.

    Example:
        >>> @retry_on_exception((ValueError,), max_attempts=2)
        ... def parse_data(data: str) -> dict:
        ...     return json.loads(data)

    """
    return retry(
        max_attempts=max_attempts,
        on=exception_types,
        jitter=False,
        log_retries=False,
    )


class Retrier:
    """Context manager for retry logic.

    Provides a context manager interface for retry logic when
    decorators are not suitable.

    Example:
        >>> retrier = Retrier(max_attempts=3, on=(ConnectionError,))
        >>> with retrier:
        ...     result = some_operation()

    """

    def __init__(
        self,
        *,
        max_attempts: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        on: tuple[type[Exception], ...] = (Exception,),
    ) -> None:
        """Initialize Retrier.

        Args:
            max_attempts: Maximum retry attempts.
            initial_delay: Initial delay between retries.
            max_delay: Maximum delay between retries.
            on: Exception types to retry on.

        """
        self.config = RetryConfig(
            max_attempts=max_attempts,
            initial_delay=initial_delay,
            max_delay=max_delay,
        )
        self.exception_types = on
        self.attempt = 0
        self.last_exception: Exception | None = None

    def __enter__(self) -> "Retrier":
        """Enter the retry context."""
        return self

    def _increment_attempt(self) -> bool:
        """Increment attempt counter safely."""
        if (
            not isinstance(self.attempt, (int, float))
            or not math.isfinite(self.attempt)
            or self.attempt < 0
        ):
            return False

        self.attempt += 1
        return True

    def _should_retry(self, exc_type: type[BaseException] | None) -> bool:
        """Determine if an exception should trigger a retry."""
        if exc_type is None:
            return False
        try:
            if not issubclass(exc_type, self.exception_types):
                return False
        except TypeError:
            return False

        if not self._increment_attempt():
            return False

        return self.attempt < self.config.max_attempts

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        _exc_tb: TracebackType | None,
    ) -> bool:
        """Exit the retry context.

        Returns True to suppress the exception if we should retry,
        False to let it propagate.
        """
        # Safe cast: check inside _should_retry ensures we handle it right
        if exc_val is not None:
            self.last_exception = exc_val if isinstance(exc_val, Exception) else None

        if not self._should_retry(exc_type):
            return False

        # Calculate delay and wait
        delay = calculate_delay(self.attempt, self.config)
        time.sleep(min(delay, 3600.0))

        return True  # Suppress exception and retry
