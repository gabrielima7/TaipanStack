"""
Resilience decorators.

Provides tools for graceful fallback and timeouts using the Result monad.
"""

import asyncio
import functools
import inspect
import math
import threading
from collections.abc import Awaitable, Callable
from typing import ParamSpec, Protocol, TypeAlias, TypeVar, cast, overload

from taipanstack.core.result import Err, Ok, Result

P = ParamSpec("P")
T = TypeVar("T")
E = TypeVar("E", bound=Exception)

ResultFunc: TypeAlias = Callable[P, Result[T, E]]
AsyncResultFunc: TypeAlias = Callable[P, Awaitable[Result[T, E]]]


class FallbackDecorator(Protocol):
    """Protocol for the fallback decorator."""

    @overload
    def __call__(self, func: ResultFunc[P, T, E]) -> ResultFunc[P, T, E]: ...

    @overload
    def __call__(self, func: AsyncResultFunc[P, T, E]) -> AsyncResultFunc[P, T, E]: ...


def _handle_fallback_exception(
    e: Exception,
    exceptions: tuple[type[Exception], ...],
    fallback_value: T,
) -> Result[T, E] | None:
    try:
        if isinstance(e, exceptions):
            return Ok(fallback_value)
    except TypeError:
        pass
    return None


def _process_fallback_result(
    result: Result[T, E], fallback_value: T
) -> Result[T, E] | None:
    if isinstance(result, Err):
        return Ok(fallback_value)
    if isinstance(result, Ok):
        return result
    return None  # type: ignore[unreachable]


def _execute_fallback_async_wrapper(
    func_coro: AsyncResultFunc[P, T, E],
    fallback_value: T,
    exceptions: tuple[type[Exception], ...],
) -> AsyncResultFunc[P, T, E]:
    @functools.wraps(func_coro)
    async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, E]:
        try:
            result = await func_coro(*args, **kwargs)
            processed_res: Result[T, E] | None = _process_fallback_result(
                result, fallback_value
            )
            if processed_res is not None:
                return processed_res
        except Exception as e:
            fallback_res: Result[T, E] | None = _handle_fallback_exception(
                e, exceptions, fallback_value
            )
            if fallback_res is not None:
                return fallback_res
            raise
        return Err(cast(E, RuntimeError("Unreachable")))

    return async_wrapper  # type: ignore[misc]


def _execute_fallback_sync_wrapper(
    func_sync: ResultFunc[P, T, E],
    fallback_value: T,
    exceptions: tuple[type[Exception], ...],
) -> ResultFunc[P, T, E]:
    @functools.wraps(func_sync)
    def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, E]:
        try:
            result = func_sync(*args, **kwargs)
            processed_res: Result[T, E] | None = _process_fallback_result(
                result, fallback_value
            )
            if processed_res is not None:
                return processed_res
        except Exception as e:
            fallback_res: Result[T, E] | None = _handle_fallback_exception(
                e, exceptions, fallback_value
            )
            if fallback_res is not None:
                return fallback_res
            raise
        return Err(cast(E, RuntimeError("Unreachable")))

    return sync_wrapper


def fallback(
    fallback_value: T,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> FallbackDecorator:
    """Provide a fallback value on failures.

    If the wrapped function returns an Err() or raises a specified exception,
    the fallback value is returned wrapped in an Ok().

    Args:
        fallback_value: The value to return on failure.
        exceptions: Exceptions to catch.

    Returns:
        Decorator function.

    """

    def decorator(
        func: ResultFunc[P, T, E] | AsyncResultFunc[P, T, E],
    ) -> ResultFunc[P, T, E] | AsyncResultFunc[P, T, E]:
        if inspect.iscoroutinefunction(func):
            func_coro = cast(AsyncResultFunc[P, T, E], func)
            return _execute_fallback_async_wrapper(
                func_coro, fallback_value, exceptions
            )

        func_sync = cast(ResultFunc[P, T, E], func)
        return _execute_fallback_sync_wrapper(func_sync, fallback_value, exceptions)

    return cast(FallbackDecorator, decorator)


class TimeoutDecorator(Protocol):
    """Protocol for the timeout decorator."""

    @overload
    def __call__(
        self,
        func: ResultFunc[P, T, E],
    ) -> Callable[P, Result[T, TimeoutError | E]]: ...

    @overload
    def __call__(
        self,
        func: AsyncResultFunc[P, T, E],
    ) -> Callable[P, Awaitable[Result[T, TimeoutError | E]]]: ...


def _handle_timeout_exception(
    e: BaseException, context: str
) -> Result[T, TimeoutError | E]:
    if isinstance(e, (SystemExit, KeyboardInterrupt, GeneratorExit)):
        raise e
    if isinstance(e, MemoryError):
        return Err(cast(E, RuntimeError(f"Memory exhaustion: {e!s}")))
    if isinstance(e, (OSError, OverflowError)):
        return Err(cast(E, RuntimeError(f"Resource exhaustion: {e!s}")))
    return Err(cast(E, RuntimeError(f"{context} exhaustion: {e!s}")))


def _validate_timeout(seconds: float) -> Result[None, E] | None:
    if (
        not isinstance(seconds, (int, float))
        or not math.isfinite(seconds)
        or seconds < 0
    ):
        return Err(
            cast(
                E,
                ValueError("Timeout must be a finite non-negative number"),
            ),
        )
    return None


async def _execute_timeout_async_inner(
    func_coro: Callable[P, Awaitable[Result[T, TimeoutError | E]]],
    seconds: float,
    *args: P.args,
    **kwargs: P.kwargs,
) -> Result[T, TimeoutError | E]:
    val_err: Result[None, E] | None = _validate_timeout(seconds)
    if val_err is not None:
        return cast(Result[T, TimeoutError | E], val_err)
    try:
        return await asyncio.wait_for(
            func_coro(*args, **kwargs),
            timeout=seconds,
        )
    except TimeoutError:
        return Err(TimeoutError(f"Execution timed out after {seconds} seconds."))
    except asyncio.CancelledError:
        raise
    except BaseException as e:
        return _handle_timeout_exception(e, "Task")


def _execute_timeout_async_wrapper(
    func_coro: Callable[P, Awaitable[Result[T, TimeoutError | E]]],
    seconds: float,
) -> Callable[P, Awaitable[Result[T, TimeoutError | E]]]:
    @functools.wraps(func_coro)
    async def async_wrapper(
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[T, TimeoutError | E]:
        return await _execute_timeout_async_inner(
            func_coro, seconds, *args, **kwargs
        )

    return async_wrapper  # type: ignore[misc]


def _check_timeout_thread_result(
    thread: threading.Thread,
    seconds: float,
    exception: list[BaseException],
    result: list[Result[T, TimeoutError | E]],
) -> Result[T, TimeoutError | E]:
    if thread.is_alive():
        return Err(TimeoutError(f"Execution timed out after {seconds} seconds."))

    if exception:
        raise exception[0]

    return result[0]


def _execute_timeout_sync_inner(
    func_sync: Callable[P, Result[T, TimeoutError | E]],
    seconds: float,
    *args: P.args,
    **kwargs: P.kwargs,
) -> Result[T, TimeoutError | E]:
    val_err: Result[None, E] | None = _validate_timeout(seconds)
    if val_err is not None:
        return cast(Result[T, TimeoutError | E], val_err)

    result: list[Result[T, TimeoutError | E]] = []
    exception: list[BaseException] = []

    def worker() -> None:
        try:
            result.append(func_sync(*args, **kwargs))
        except BaseException as e:
            exception.append(e)

    thread = threading.Thread(target=worker, daemon=True)
    try:
        thread.start()
        thread.join(timeout=seconds)
    except BaseException as e:
        return _handle_timeout_exception(e, "Thread")

    return _check_timeout_thread_result(thread, seconds, exception, result)


def _execute_timeout_sync_wrapper(
    func_sync: Callable[P, Result[T, TimeoutError | E]],
    seconds: float,
) -> Callable[P, Result[T, TimeoutError | E]]:
    @functools.wraps(func_sync)
    def sync_wrapper(
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[T, TimeoutError | E]:
        return _execute_timeout_sync_inner(func_sync, seconds, *args, **kwargs)

    return sync_wrapper


def timeout(seconds: float) -> TimeoutDecorator:
    """Enforce a maximum execution time.

    If the execution time exceeds the specified limit, returns Err(TimeoutError).

    Args:
        seconds: Maximum allowed execution time in seconds.

    Returns:
        Decorator function.

    """

    def decorator(
        func: ResultFunc[P, T, E] | AsyncResultFunc[P, T, E],
    ) -> (
        Callable[P, Result[T, TimeoutError | E]]
        | Callable[P, Awaitable[Result[T, TimeoutError | E]]]
    ):
        if inspect.iscoroutinefunction(func):
            func_coro = cast(Callable[P, Awaitable[Result[T, TimeoutError | E]]], func)
            return _execute_timeout_async_wrapper(func_coro, seconds)

        func_sync = cast(Callable[P, Result[T, TimeoutError | E]], func)
        return _execute_timeout_sync_wrapper(func_sync, seconds)

    return cast(TimeoutDecorator, decorator)
