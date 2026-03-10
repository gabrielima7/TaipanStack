"""
Concurrency utilities.

Provides a bulkhead pattern concurrency limiter decorator for both
synchronous and asynchronous functions. Uses an `OverloadError` and
returns a `Result` type.
"""

import asyncio
import functools
import inspect
import threading
from collections.abc import Callable, Coroutine
from typing import Any, ParamSpec, Protocol, TypeVar, overload

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
        self, func: Callable[P, T]
    ) -> Callable[P, Result[T, OverloadError]]: ...  # pragma: no cover

    @overload
    def __call__(
        self, func: Callable[P, Coroutine[Any, Any, T]]
    ) -> Callable[
        P, Coroutine[Any, Any, Result[T, OverloadError]]
    ]: ...  # pragma: no cover


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
    if max_tasks <= 0:
        raise ValueError("max_tasks must be > 0")
    if timeout < 0.0:
        raise ValueError("timeout must be >= 0.0")

    def decorator(
        func: Callable[P, T] | Callable[P, Coroutine[Any, Any, T]],
    ) -> (
        Callable[P, Result[T, OverloadError]]
        | Callable[P, Coroutine[Any, Any, Result[T, OverloadError]]]
    ):
        if inspect.iscoroutinefunction(func):
            async_semaphore = asyncio.Semaphore(max_tasks)

            @functools.wraps(func)
            async def async_wrapper(
                *args: P.args,
                **kwargs: P.kwargs,
            ) -> Result[T, OverloadError]:
                if timeout > 0.0:
                    try:
                        async with asyncio.timeout(timeout):
                            await async_semaphore.acquire()
                    except TimeoutError:
                        return Err(OverloadError())
                else:
                    if async_semaphore.locked():
                        return Err(OverloadError())
                    await async_semaphore.acquire()

                try:
                    return Ok(await func(*args, **kwargs))
                finally:
                    async_semaphore.release()

            return async_wrapper

        sync_semaphore = threading.Semaphore(max_tasks)

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, OverloadError]:
            if timeout > 0.0:
                acquired = sync_semaphore.acquire(timeout=timeout)
                if not acquired:
                    return Err(OverloadError())
            else:
                acquired = sync_semaphore.acquire(blocking=False)
                if not acquired:
                    return Err(OverloadError())

            try:
                return Ok(func(*args, **kwargs))  # type: ignore[arg-type]
            finally:
                sync_semaphore.release()

        return wrapper

    return decorator  # type: ignore[return-value]
