"""
Adaptive Timeout — auto-tunes latency thresholds based on recent performance.

Calculates an Exponential Moving Average (EMA) of successful request
latencies and dynamic scales the timeout.
"""

from __future__ import annotations

import asyncio
import logging
import threading
import time
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import TypeVar

from taipanstack.core.result import Err, Ok, Result

logger = logging.getLogger("taipanstack.resilience.adaptive.timeout")

T = TypeVar("T")


class AdaptiveTimeoutError(Exception):
    """Raised when an operation exceeds the dynamically calculated timeout."""


class AdaptiveTimeout:
    """Dynamically scales call timeouts based on historical latency.

    Uses an Exponential Moving Average (EMA) of successful calls to
    adjust the timeout for the next call. The new timeout is:
    `EMA * tolerance_multiplier`, strictly bounded between `min_timeout`
    and `max_timeout`.

    Args:
        name: Identifier for logging.
        initial_timeout: Starting timeout until enough history is gathered.
        min_timeout: Absolute floor for the dynamic timeout.
        max_timeout: Absolute ceiling for the dynamic timeout.
        tolerance_multiplier: Factor to multiply the EMA by for the timeout.
        ema_alpha: Smoothing factor for EMA (0.0 to 1.0). Higher alpha
            discounts older observations faster.

    Example:
        >>> timeout = AdaptiveTimeout(
        ...     "api",
        ...     min_timeout=0.1,
        ...     max_timeout=5.0,
        ... )
        >>> @timeout.wrap
        ... async def call_api() -> Result[dict, Exception]:
        ...     return Ok(await get_data())

    """

    def __init__(
        self,
        name: str = "default",
        *,
        initial_timeout: float = 1.0,
        min_timeout: float = 0.05,
        max_timeout: float = 10.0,
        tolerance_multiplier: float = 3.0,
        ema_alpha: float = 0.2,
    ) -> None:
        """Initialize the adaptive timeout.

        Args:
            name: Timeout identifier.
            initial_timeout: Starting timeout before enough history exists.
            min_timeout: Minimum absolute timeout boundary.
            max_timeout: Maximum absolute timeout boundary.
            tolerance_multiplier: Multiplier applied to average latency.
            ema_alpha: Weight for newer samples in EMA.

        """
        self.name = name
        self._min_timeout = min_timeout
        self._max_timeout = max_timeout
        self._tolerance_multiplier = tolerance_multiplier
        self._ema_alpha = ema_alpha

        self._lock = threading.Lock()
        self._current_ema: float | None = None
        self._current_timeout = max(min_timeout, min(initial_timeout, max_timeout))

    @property
    def current_timeout(self) -> float:
        """The dynamically computed timeout for the next call."""
        with self._lock:
            return self._current_timeout

    @property
    def current_ema(self) -> float | None:
        """The current exponential moving average of latency."""
        with self._lock:
            return self._current_ema

    def record_latency(self, latency: float) -> None:
        """Update the EMA with a new latency sample.

        Args:
            latency: Time taken for the successful call.

        """
        with self._lock:
            if self._current_ema is None:
                self._current_ema = latency
            else:
                self._current_ema = (
                    self._ema_alpha * latency
                    + (1.0 - self._ema_alpha) * self._current_ema
                )

            computed_timeout = self._current_ema * self._tolerance_multiplier
            self._current_timeout = max(
                self._min_timeout, min(computed_timeout, self._max_timeout)
            )

    def evaluate_result(
        self, result: Result[T, Exception], duration: float
    ) -> Result[T, Exception]:
        """Evaluate a Result and update EMA if successful.

        Args:
            result: The `Result` returned from the wrapped function.
            duration: The time taken to execute the function.

        Returns:
            The original Result.

        """
        if isinstance(result, Ok):
            self.record_latency(duration)
        return result

    def wrap(
        self,
        func: Callable[..., Awaitable[Result[T, Exception]]],
    ) -> Callable[..., Awaitable[Result[T, Exception]]]:
        """Wrap an async function to enforce the adaptive timeout.

        Args:
            func: Async function returning a ``Result``.

        Returns:
            Wrapped async function returning a ``Result``.

        """

        @wraps(func)
        async def wrapper(*args: object, **kwargs: object) -> Result[T, Exception]:
            timeout = self.current_timeout
            start = time.monotonic()
            try:
                # We do not use asyncio.timeout because it's Python 3.11+,
                # using wait_for for broader compatibility.
                # To align with timeout util, wait_for is fine.
                coro = func(*args, **kwargs)
                result = await asyncio.wait_for(coro, timeout=timeout)
                duration = time.monotonic() - start
                return self.evaluate_result(result, duration)
            except TimeoutError:
                logger.warning(
                    "AdaptiveTimeout '%s' exceeded threshold %.3fs",
                    self.name,
                    timeout,
                )
                return Err(
                    AdaptiveTimeoutError(f"Operation timed out after {timeout:.3f}s")
                )
            except Exception as exc:
                return Err(exc)

        return wrapper
