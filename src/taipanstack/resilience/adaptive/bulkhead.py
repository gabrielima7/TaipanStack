"""
Bulkhead pattern — concurrency isolation via semaphore.

Limits the number of concurrent executions to prevent a single
failing dependency from consuming all available resources.
"""

from __future__ import annotations

import asyncio
import logging
import math
from collections.abc import Awaitable, Callable
from typing import ParamSpec, TypeVar

from taipanstack.core.result import Err, Ok, Result

logger = logging.getLogger("taipanstack.resilience.adaptive.bulkhead")

T = TypeVar("T")
P = ParamSpec("P")


class BulkheadFullError(Exception):
    """Raised when the bulkhead queue is at capacity."""

    def __init__(self, name: str, max_concurrent: int, max_queue: int) -> None:
        """Initialize BulkheadFullError.

        Args:
            name: Bulkhead name.
            max_concurrent: Concurrency limit.
            max_queue: Queue limit.

        """
        self.bulkhead_name = name
        self.max_concurrent = max_concurrent
        self.max_queue = max_queue
        super().__init__(
            f"Bulkhead '{name}' is full "
            f"(max_concurrent={max_concurrent}, max_queue={max_queue})",
        )


class Bulkhead:
    """Concurrency limiter using ``asyncio.Semaphore``.

    Limits the number of concurrent executions of a callable.
    Excess callers are queued up to ``max_queue``; beyond that
    a ``BulkheadFullError`` is returned.

    Args:
        name: Identifier for logging.
        max_concurrent: Maximum concurrent executions.
        max_queue: Maximum queued callers beyond concurrent limit.
        timeout: Seconds to wait for a permit before timing out.

    Example:
        >>> bulk = Bulkhead("db", max_concurrent=5, max_queue=10)
        >>> result = await bulk.execute(fetch_data, user_id)

    """

    def __init__(
        self,
        name: str = "default",
        *,
        max_concurrent: int = 10,
        max_queue: int = 50,
        timeout: float = 30.0,
    ) -> None:
        """Initialize the bulkhead.

        Args:
            name: Bulkhead name.
            max_concurrent: Concurrency limit.
            max_queue: Queue limit.
            timeout: Permit acquisition timeout.

        """
        self.name = name
        self._max_concurrent = max_concurrent
        self._max_queue = max_queue
        if (
            not isinstance(timeout, (int, float))
            or not math.isfinite(timeout)
            or timeout < 0
        ):
            raise ValueError("timeout must be a finite non-negative number")
        self._timeout = timeout
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._queued = 0
        self._active = 0

    @property
    def available_permits(self) -> int:
        """Number of available concurrency permits."""
        return self._max_concurrent - self._active

    @property
    def queued(self) -> int:
        """Number of callers currently waiting in the queue."""
        return self._queued

    @property
    def active(self) -> int:
        """Number of currently executing tasks."""
        return self._active

    async def execute(
        self,
        fn: Callable[P, Awaitable[T]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[T, Exception]:
        """Execute a callable within bulkhead limits.

        Args:
            fn: Async callable to execute.
            *args: Positional arguments for fn.
            **kwargs: Keyword arguments for fn.

        Returns:
            ``Ok(result)`` on success, ``Err`` on failure.

        """
        # Check queue capacity
        if self._queued >= self._max_queue:
            return Err(
                BulkheadFullError(
                    self.name,
                    self._max_concurrent,
                    self._max_queue,
                ),
            )

        self._queued += 1
        try:
            # Wait for a permit
            try:
                await asyncio.wait_for(
                    self._semaphore.acquire(),
                    timeout=self._timeout,
                )
            except TimeoutError:
                return Err(
                    TimeoutError(
                        f"Bulkhead '{self.name}' timed out "
                        f"after {self._timeout}s waiting for permit",
                    ),
                )
            except (RuntimeError, OSError, MemoryError) as e:
                return Err(RuntimeError(f"Resource exhaustion: {e!s}"))
        finally:
            self._queued -= 1

        # Execute within the permit
        self._active += 1
        try:
            result = await fn(*args, **kwargs)
            return Ok(result)
        except Exception as exc:
            logger.warning(
                "Bulkhead '%s' execution failed: %s",
                self.name,
                exc,
            )
            return Err(exc)
        finally:
            self._active -= 1
            self._semaphore.release()
