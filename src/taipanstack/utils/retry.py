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
import secrets
import time
from collections.abc import Callable
from dataclasses import dataclass
from types import TracebackType
from typing import Any, NoReturn, ParamSpec, TypeVar, cast

P = ParamSpec("P")
R = TypeVar("R")
F = TypeVar("F", bound=Callable[..., Any])

logger = logging.getLogger("taipanstack.utils.retry")

try:
    import structlog as _structlog

    _structlog_logger = _structlog.get_logger("taipanstack.utils.retry")
    _HAS_STRUCTLOG = True
except ImportError:  # pragma: no cover — structlog is optional
    _structlog_logger = None
    _HAS_STRUCTLOG = False


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
    # Exponential backoff
    delay = config.initial_delay * (config.exponential_base ** (attempt - 1))

    # Cap at max delay
    delay = min(delay, config.max_delay)

    # Add jitter if enabled
    # Note: Using random for jitter is intentionally non-cryptographic.
    # However, to maintain a clean security baseline and satisfy Bandit,
    # we use secrets.SystemRandom() which provides cryptographically
    # secure random numbers.
    if config.jitter:
        jitter_amount = delay * config.jitter_factor
        delay += secrets.SystemRandom().uniform(-jitter_amount, jitter_amount)

    return max(0, delay)


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

    # Invoke callback or emit structured log if no callback set
    if config.on_retry is not None:
        config.on_retry(attempt, config.max_attempts, exc, delay)
    elif _HAS_STRUCTLOG and _structlog_logger is not None:  # pragma: no branch
        _structlog_logger.warning(
            "retry_attempted",
            function=func_name,
            attempt=attempt,
            max_attempts=config.max_attempts,
            error=str(exc),
            delay_seconds=round(delay, 3),
        )


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


def retry(
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
) -> Callable[[F], F]:
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

    def decorator(func: F) -> F:
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                last_exception: Exception | None = None

                for attempt in range(1, max_attempts + 1):  # pragma: no branch
                    try:
                        return await func(*args, **kwargs)
                    except on as e:
                        last_exception = e

                        if attempt == max_attempts:
                            _log_all_failed(
                                func.__name__,
                                e,
                                config,
                            )
                            break

                        delay = calculate_delay(attempt, config)
                        _log_retry_attempt(
                            func.__name__,
                            attempt,
                            e,
                            delay,
                            config,
                        )
                        await asyncio.sleep(delay)

                _raise_retry_error(
                    func.__name__,
                    max_attempts,
                    reraise,
                    last_exception,
                )

            return cast(F, async_wrapper)

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception: Exception | None = None

            for attempt in range(1, max_attempts + 1):  # pragma: no branch
                try:
                    return func(*args, **kwargs)
                except on as e:
                    last_exception = e

                    if attempt == max_attempts:
                        _log_all_failed(
                            func.__name__,
                            e,
                            config,
                        )
                        break

                    # Calculate delay and wait
                    delay = calculate_delay(attempt, config)
                    _log_retry_attempt(
                        func.__name__,
                        attempt,
                        e,
                        delay,
                        config,
                    )
                    time.sleep(delay)

            _raise_retry_error(
                func.__name__,
                max_attempts,
                reraise,
                last_exception,
            )

        return cast(F, wrapper)

    return decorator


def retry_on_exception(
    exception_types: tuple[type[Exception], ...],
    max_attempts: int = 3,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
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
        self.attempt = 0
        self.last_exception = None
        return self

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
        if exc_type is None:
            return False  # No exception, exit normally

        if not issubclass(exc_type, self.exception_types):
            return False  # Exception type not in retry list

        # Safe cast: issubclass guard above ensures exc_val is Exception
        self.last_exception = exc_val if isinstance(exc_val, Exception) else None
        self.attempt += 1

        if self.attempt >= self.config.max_attempts:
            return False  # Max attempts reached, propagate exception

        # Calculate delay and wait
        delay = calculate_delay(self.attempt, self.config)
        time.sleep(delay)

        return True  # Suppress exception and retry
