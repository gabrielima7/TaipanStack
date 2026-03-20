"""
Rate limiting utilities.

Provides an in-memory token-bucket based rate limiting decorator
for both synchronous and asynchronous functions. The decorator
returns a ``Result`` type encapsulating the original return value
or a ``RateLimitError`` error.
"""

import functools
import inspect
import threading
import time
from collections.abc import Callable, Coroutine
from typing import Any, ParamSpec, Protocol, TypeVar, overload

from taipanstack.core.result import Err, Ok, Result

__all__ = ["RateLimitError", "RateLimiter", "rate_limit"]

P = ParamSpec("P")
T = TypeVar("T")


class RateLimitError(Exception):
    """Exception raised when a rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded") -> None:
        """Initialize the RateLimitError.

        Args:
            message: The error message to display.Defaults to "Rate limit exceeded".

        """
        super().__init__(message)


class RateLimiter:
    """Token bucket rate limiter logic."""

    def __init__(self, max_calls: int, time_window: float) -> None:
        """Initialize the token bucket.

        Args:
            max_calls: The maximum number of calls allowed in the time window.
            time_window: The time window in seconds.

        """
        if max_calls <= 0 or time_window <= 0:
            raise ValueError("max_calls and time_window must be > 0.0")
        self.capacity: float = float(max_calls)
        self.time_window: float = float(time_window)
        self.tokens: float = self.capacity
        self.last_update: float = time.monotonic()
        self._lock = threading.Lock()

    def consume(self) -> bool:
        """Try to consume a single token.

        Returns:
            True if a token was consumed (allow), False otherwise (limit exceeded).

        """
        with self._lock:
            now = time.monotonic()
            elapsed = max(0.0, now - self.last_update)
            self.last_update = now

            # Add tokens for elapsed time based on fill rate
            self.tokens += elapsed * (self.capacity / self.time_window)
            self.tokens = min(self.tokens, self.capacity)

            if self.tokens >= 1.0:
                self.tokens -= 1.0
                return True
            return False


class RateLimitDecorator(Protocol):
    """Protocol for the rate limit decorator."""

    @overload
    def __call__(
        self, func: Callable[P, T]
    ) -> Callable[P, Result[T, RateLimitError]]: ...  # pragma: no cover

    @overload
    def __call__(
        self, func: Callable[P, Coroutine[Any, Any, T]]
    ) -> Callable[
        P, Coroutine[Any, Any, Result[T, RateLimitError]]
    ]: ...  # pragma: no cover


def rate_limit(
    max_calls: int,
    time_window: float,
) -> RateLimitDecorator:
    """Decorate a function to apply rate limiting.

    If the rate limit is exceeded, the wrapped function immediately returns
    an ``Err(RateLimitError)``. Uses an in-memory token bucket strategy.

    Args:
        max_calls: Maximum function executions allowed in the defined window.
        time_window: Time window size in seconds.

    Returns:
        Decorated function returning a ``Result[T, RateLimitError]``.

    Example:
        >>> @rate_limit(max_calls=2, time_window=1.0)
        ... def fetch_data() -> str:
        ...     return "data"
        >>> fetch_data()
        Ok('data')
        >>> fetch_data()
        Ok('data')
        >>> fetch_data()
        Err(RateLimitError('Rate limit exceeded'))

    """

    def decorator(
        func: Callable[P, T] | Callable[P, Coroutine[Any, Any, T]],
    ) -> (
        Callable[P, Result[T, RateLimitError]]
        | Callable[P, Coroutine[Any, Any, Result[T, RateLimitError]]]
    ):
        limiter = RateLimiter(max_calls, time_window)

        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(
                *args: P.args,
                **kwargs: P.kwargs,
            ) -> Result[T, RateLimitError]:
                if not limiter.consume():
                    return Err(RateLimitError())
                return Ok(await func(*args, **kwargs))

            return async_wrapper

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, RateLimitError]:
            if not limiter.consume():
                return Err(RateLimitError())
            return Ok(func(*args, **kwargs))  # type: ignore[arg-type]

        return wrapper

    return decorator  # type: ignore[return-value]
