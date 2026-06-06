"""
Rate limiting utilities.

Provides an in-memory token-bucket based rate limiting decorator
for both synchronous and asynchronous functions. The decorator
returns a ``Result`` type encapsulating the original return value
or a ``RateLimitError`` error.
"""

import functools
import inspect
import math
import threading
import time
from collections.abc import Awaitable, Callable
from typing import ParamSpec, Protocol, TypeVar, cast, overload

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
        if not math.isfinite(max_calls) or not math.isfinite(time_window):
            raise ValueError("max_calls and time_window must be finite numbers")
        if max_calls <= 0 or time_window <= 0:
            raise ValueError("max_calls and time_window must be > 0.0")
        self.capacity: float = float(max_calls)
        self.time_window: float = float(time_window)
        self.tokens: float = self.capacity
        self.last_update: float = time.monotonic()
        self._lock = threading.Lock()

    def _is_valid_time_window(self) -> bool:
        """Check if time window is valid."""
        if not isinstance(self.time_window, (int, float)):
            return False  # type: ignore[unreachable]
        return math.isfinite(self.time_window) and self.time_window > 0.0

    def _is_valid_capacity(self) -> bool:
        """Check if capacity is valid."""
        if not isinstance(self.capacity, (int, float)):
            return False  # type: ignore[unreachable]
        return math.isfinite(self.capacity) and self.capacity > 0.0

    def _is_valid_bucket_state(self) -> bool:
        """Check if the bucket's time window and capacity are in a valid state."""
        return self._is_valid_time_window() and self._is_valid_capacity()

    def _calculate_new_tokens(self, elapsed: float) -> float | None:
        """Calculate new tokens based on elapsed time."""
        new_tokens = elapsed * (self.capacity / self.time_window)
        return new_tokens if math.isfinite(new_tokens) else None

    def _apply_new_tokens(self, new_tokens: float) -> bool:
        """Apply new tokens to the bucket."""
        if not isinstance(self.tokens, (int, float)):
            self.tokens = self.capacity  # type: ignore[unreachable]
            return False
        if not isinstance(new_tokens, (int, float)):
            return False  # type: ignore[unreachable]
        self.tokens += new_tokens
        if not math.isfinite(self.tokens):
            # Reset to previous state or capacity if corrupted
            self.tokens = self.capacity
            return False
        self.tokens = min(self.tokens, self.capacity)
        return True

    def _add_tokens(self, now: float) -> bool:
        """Calculate and add new tokens to the bucket based on elapsed time.

        Args:
            now: Current monotonic time.

        Returns:
            True if token update succeeds, False if state corruption is detected.

        """
        if not isinstance(self.last_update, (int, float)):
            return False  # type: ignore[unreachable]
        raw_elapsed = now - self.last_update
        if not math.isfinite(raw_elapsed):
            return False
        elapsed = max(0.0, raw_elapsed)
        self.last_update = now

        # Prevent state corruption or infinite elapsed time
        if not self._is_valid_bucket_state():
            return False

        new_tokens = self._calculate_new_tokens(elapsed)
        if new_tokens is None:
            return False

        return self._apply_new_tokens(new_tokens)

    def _try_consume(self, tokens: float) -> bool:
        """Attempt to consume the tokens from the bucket if available."""
        if not isinstance(self.tokens, (int, float)):
            return False  # type: ignore[unreachable]
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def _process_consumption(self, tokens: float) -> bool:
        """Process token consumption inside the lock."""
        try:
            now = time.monotonic()
        except Exception:
            return False

        # Prevent time corruption from poisoning the bucket state.
        # Only try to add tokens if time is finite.
        if not isinstance(now, (int, float)) or (
            math.isfinite(now) and not self._add_tokens(now)
        ):
            return False

        return self._try_consume(tokens)

    def consume(self, tokens: float = 1.0) -> bool:
        """Try to consume tokens.

        Args:
            tokens: Number of tokens to consume. Defaults to 1.0.

        Returns:
            True if tokens were consumed (allow), False otherwise (limit exceeded).

        """
        if not isinstance(tokens, (int, float)) or not math.isfinite(tokens):
            return False
        if tokens <= 0:
            return True

        with self._lock:
            return self._process_consumption(tokens)


class RateLimitDecorator(Protocol):
    """Protocol for the rate limit decorator."""

    @overload
    def __call__(
        self,
        func: Callable[P, T],
    ) -> Callable[P, Result[T, RateLimitError]]: ...

    @overload
    def __call__(
        self,
        func: Callable[P, Awaitable[T]],
    ) -> Callable[P, Awaitable[Result[T, RateLimitError]]]: ...


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
        func: Callable[P, T] | Callable[P, Awaitable[T]],
    ) -> (
        Callable[P, Result[T, RateLimitError]]
        | Callable[P, Awaitable[Result[T, RateLimitError]]]
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
            func_sync = cast(Callable[P, T], func)
            return Ok(func_sync(*args, **kwargs))

        return wrapper

    return cast(RateLimitDecorator, decorator)
