"""
Concurrency utilities.

Provides a bulkhead pattern concurrency limiter decorator for both
synchronous and asynchronous functions. Uses an `OverloadError` and
returns a `Result` type.
"""

import asyncio
import functools
import inspect
import math
import threading
from collections.abc import Awaitable, Callable
from typing import ParamSpec, Protocol, TypeVar, cast, overload

from taipanstack.core.result import Err, Ok, Result

__all__ = ["OverloadError", "limit_concurrency"]

P = ParamSpec("P")
T = TypeVar("T")


class OverloadError(Exception):
    """Exception raised when a concurrency limit is exceeded or timed out."""

    def __init__(self, message: str = "Concurrency limit reached") -> None:
        """Initialize the OverloadError.

        Args:
            message: The error message to display.
                Defaults to "Concurrency limit reached".

        """
        super().__init__(message)


class ConcurrencyLimitDecorator(Protocol):
    """Protocol for the concurrency limit decorator."""

    @overload
    def __call__(
        self,
        func: Callable[P, T],
    ) -> Callable[P, Result[T, OverloadError]]: ...

    @overload
    def __call__(
        self,
        func: Callable[P, Awaitable[T]],
    ) -> Callable[P, Awaitable[Result[T, OverloadError]]]: ...


async def _acquire_async_semaphore(
    async_semaphore: asyncio.Semaphore,
    timeout: float,
) -> Result[None, OverloadError]:
    """Acquire async semaphore with optional timeout."""
    try:
        if timeout <= 0.0:
            if async_semaphore.locked():
                return Err(OverloadError())
            await async_semaphore.acquire()
            return Ok(None)

        try:
            async with asyncio.timeout(timeout):
                await async_semaphore.acquire()
                return Ok(None)
        except TimeoutError:
            return Err(OverloadError())
    except asyncio.CancelledError:
        raise
    except Exception as e:
        return Err(OverloadError(f"Resource exhaustion: {e!s}"))


def _handle_async_concurrency(
    func: Callable[P, Awaitable[T]],
    max_tasks: int,
    timeout: float,
) -> Callable[P, Awaitable[Result[T, OverloadError]]]:
    """Handle asynchronous concurrency limiting."""
    async_semaphore = asyncio.Semaphore(max_tasks)

    @functools.wraps(func)
    async def async_wrapper(
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[T, OverloadError]:
        acquire_result = await _acquire_async_semaphore(async_semaphore, timeout)
        if isinstance(acquire_result, Err):
            return acquire_result

        try:
            return Ok(await func(*args, **kwargs))
        finally:
            async_semaphore.release()

    return async_wrapper


def _acquire_sync_semaphore(
    sync_semaphore: threading.Semaphore,
    timeout: float,
) -> Result[None, OverloadError]:
    """Acquire sync semaphore with optional timeout."""
    try:
        if timeout <= 0.0:
            acquired = sync_semaphore.acquire(blocking=False)
        else:
            acquired = sync_semaphore.acquire(timeout=timeout)

        if not acquired:
            return Err(OverloadError())
        return Ok(None)
    except Exception as e:
        return Err(OverloadError(f"Resource exhaustion: {e!s}"))


def _handle_sync_concurrency(
    func: Callable[P, T],
    max_tasks: int,
    timeout: float,
) -> Callable[P, Result[T, OverloadError]]:
    """Handle synchronous concurrency limiting."""
    sync_semaphore = threading.Semaphore(max_tasks)

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, OverloadError]:
        acquire_result = _acquire_sync_semaphore(sync_semaphore, timeout)
        if isinstance(acquire_result, Err):
            return acquire_result

        try:
            return Ok(func(*args, **kwargs))
        finally:
            sync_semaphore.release()

    return wrapper


def _validate_max_tasks(max_tasks: int) -> None:
    """Validate max_tasks argument."""
    if not isinstance(max_tasks, int) or max_tasks <= 0:
        raise ValueError("max_tasks must be > 0")


def _validate_timeout(timeout: float) -> None:
    """Validate timeout argument."""
    if (
        not isinstance(timeout, (int, float))
        or not math.isfinite(timeout)
        or timeout < 0.0
    ):
        raise ValueError("timeout must be a finite non-negative number")


def _validate_limit_concurrency_args(max_tasks: int, timeout: float) -> None:
    """Validate arguments for limit_concurrency."""
    _validate_max_tasks(max_tasks)
    _validate_timeout(timeout)


def limit_concurrency(
    max_tasks: int,
    timeout: float = 0.0,
) -> ConcurrencyLimitDecorator:
    """Decorate a function to apply the bulkhead concurrency limit pattern.

    If the maximum concurrent executions are reached, the wrapper will wait up
    to `timeout` seconds to acquire a execution slot. If it fails, it returns
    an ``Err(OverloadError)``.

    Args:
        max_tasks: Maximum concurrent function executions allowed.
        timeout: Maximum time in seconds to wait for a slot if limit is reached.

    Returns:
        Decorated function returning a ``Result[T, OverloadError]``.

    Example:
        >>> @limit_concurrency(max_tasks=2, timeout=0.1)
        ... def process_data() -> str:
        ...     return "data"
        >>> process_data()
        Ok('data')

    """
    _validate_limit_concurrency_args(max_tasks, timeout)

    def decorator(
        func: Callable[P, T] | Callable[P, Awaitable[T]],
    ) -> (
        Callable[P, Result[T, OverloadError]]
        | Callable[P, Awaitable[Result[T, OverloadError]]]
    ):
        if inspect.iscoroutinefunction(func):
            return _handle_async_concurrency(
                func,
                max_tasks,
                timeout,
            )

        return _handle_sync_concurrency(
            cast(Callable[P, T], func),
            max_tasks,
            timeout,
        )

    return cast(ConcurrencyLimitDecorator, decorator)
