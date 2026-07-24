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

    def _validate_finite(self, max_calls: int, time_window: float) -> None:
        """Check if parameters are finite numbers."""
        if not isinstance(max_calls, (int, float)) or not math.isfinite(max_calls):
            raise ValueError("max_calls and time_window must be finite numbers")
        if not isinstance(time_window, (int, float)) or not math.isfinite(time_window):
            raise ValueError("max_calls and time_window must be finite numbers")

    def _validate_positive(self, max_calls: int, time_window: float) -> None:
        """Check if parameters are positive."""
        if max_calls <= 0:
            raise ValueError("max_calls and time_window must be > 0.0")
        if time_window <= 0:
            raise ValueError("max_calls and time_window must be > 0.0")

    def _validate_init_params(self, max_calls: int, time_window: float) -> None:
        """Validate initialization parameters."""
        self._validate_finite(max_calls, time_window)
        self._validate_positive(max_calls, time_window)

    def __init__(self, max_calls: int, time_window: float) -> None:
        """Initialize the token bucket.

        Args:
            max_calls: The maximum number of calls allowed in the time window.
            time_window: The time window in seconds.

        """
        self._validate_init_params(max_calls, time_window)
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

    def _calculate_elapsed(self, now: float) -> float | None:
        """Calculate the elapsed time since the last update."""
        if not isinstance(self.last_update, (int, float)):
            return None  # type: ignore[unreachable]
        raw_elapsed = now - self.last_update
        if not math.isfinite(raw_elapsed):
            return None
        return max(0.0, raw_elapsed)

    def _add_tokens(self, now: float) -> bool:
        """Calculate and add new tokens to the bucket based on elapsed time.

        Args:
            now: Current monotonic time.

        Returns:
            True if token update succeeds, False if state corruption is detected.

        """
        elapsed = self._calculate_elapsed(now)
        if elapsed is None:
            return False

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
        if not math.isfinite(self.tokens):
            # Reset to capacity if state is corrupted to inf/nan
            self.tokens = self.capacity
            return False
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def _get_current_time(self) -> float | None:
        """Get current monotonic time safely."""
        try:
            return time.monotonic()
        except Exception:
            return None

    def _validate_and_add_tokens(self, now: float | None) -> bool:
        """Validate time and add tokens.

        Returns True if tokens were added successfully, False otherwise.
        """
        if now is None:
            return False
        if not isinstance(now, (int, float)):
            return False  # type: ignore[unreachable]
        if not math.isfinite(now):
            # If not finite, we can't add tokens, but we shouldn't fail
            # the consumption if there are already tokens.
            return True
        return self._add_tokens(now)

    def _process_consumption(self, tokens: float) -> bool:
        """Process token consumption inside the lock."""
        now = self._get_current_time()

        # Prevent time corruption from poisoning the bucket state.
        # Only try to add tokens if time is finite.
        if not self._validate_and_add_tokens(now):
            return False

        return self._try_consume(tokens)

    def _is_valid_token_amount(self, tokens: float) -> bool:
        """Check if requested token amount is valid."""
        if not isinstance(tokens, (int, float)):
            return False  # type: ignore[unreachable]
        return math.isfinite(tokens)

    def consume(self, tokens: float = 1.0) -> bool:
        """Try to consume tokens.

        Args:
            tokens: Number of tokens to consume. Defaults to 1.0.

        Returns:
            True if tokens were consumed (allow), False otherwise (limit exceeded).

        """
        if not self._is_valid_token_amount(tokens):
            return False
        if tokens <= 0:
            return True

        try:
            with self._lock:
                return self._process_consumption(tokens)
        except Exception:
            return False


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

            @functools.wraps(func)  # type: ignore[misc]
            async def async_wrapper(
                *args: P.args,
                **kwargs: P.kwargs,
            ) -> Result[T, RateLimitError]:
                try:
                    if not limiter.consume():
                        return Err(RateLimitError())
                except Exception:
                    return Err(RateLimitError())
                return Ok(await func(*args, **kwargs))  # type: ignore[misc]

            return async_wrapper  # type: ignore[misc]

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, RateLimitError]:
            try:
                if not limiter.consume():
                    return Err(RateLimitError())
            except Exception:
                return Err(RateLimitError())
            func_sync = cast(Callable[P, T], func)
            return Ok(func_sync(*args, **kwargs))

        return wrapper

    return cast(RateLimitDecorator, decorator)
