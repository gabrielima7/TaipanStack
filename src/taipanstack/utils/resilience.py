"""
Resilience decorators.

Provides tools for graceful fallback and timeouts using the Result monad.
"""

import asyncio
import concurrent.futures
import functools
import inspect
from collections.abc import Callable, Coroutine
from typing import Any, ParamSpec, Protocol, TypeVar, cast, overload

from taipanstack.core.result import Err, Ok, Result

P = ParamSpec("P")
T = TypeVar("T")
E = TypeVar("E", bound=Exception)


class FallbackDecorator(Protocol):
    """Protocol for the fallback decorator."""

    @overload
    def __call__(
        self, func: Callable[P, Result[T, E]]
    ) -> Callable[P, Result[T, E]]: ...  # pragma: no cover

    @overload
    def __call__(
        self, func: Callable[P, Coroutine[Any, Any, Result[T, E]]]
    ) -> Callable[
        P, Coroutine[Any, Any, Result[T, E]]
    ]: ...  # pragma: no cover


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
        func: (
            Callable[P, Result[T, E]]
            | Callable[P, Coroutine[Any, Any, Result[T, E]]]
        ),
    ) -> (
        Callable[P, Result[T, E]]
        | Callable[P, Coroutine[Any, Any, Result[T, E]]]
    ):
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, E]:
                try:
                    # func is a coroutine function here
                    func_coro = cast(
                        Callable[P, Coroutine[Any, Any, Result[T, E]]], func
                    )
                    result = await func_coro(*args, **kwargs)
                    match result:
                        case Err():
                            return Ok(fallback_value)
                        case Ok():
                            return result
                except exceptions:
                    return Ok(fallback_value)
                return Err(cast(E, RuntimeError("Unreachable")))  # pragma: no cover

            return async_wrapper

        @functools.wraps(func)
        def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, E]:
            try:
                # func is a normal function here
                func_sync = cast(Callable[P, Result[T, E]], func)
                result = func_sync(*args, **kwargs)
                match result:
                    case Err():
                        return Ok(fallback_value)
                    case Ok():
                        return result
            except exceptions:
                return Ok(fallback_value)
            return Err(cast(E, RuntimeError("Unreachable")))  # pragma: no cover

        return sync_wrapper

    return decorator  # type: ignore[return-value]


class TimeoutDecorator(Protocol):
    """Protocol for the timeout decorator."""

    @overload
    def __call__(
        self, func: Callable[P, Result[T, E]]
    ) -> Callable[P, Result[T, TimeoutError | E]]: ...  # pragma: no cover

    @overload
    def __call__(
        self, func: Callable[P, Coroutine[Any, Any, Result[T, E]]]
    ) -> Callable[
        P, Coroutine[Any, Any, Result[T, TimeoutError | E]]
    ]: ...  # pragma: no cover


def timeout(seconds: float) -> TimeoutDecorator:
    """Enforce a maximum execution time.

    If the execution time exceeds the specified limit, returns Err(TimeoutError).

    Args:
        seconds: Maximum allowed execution time in seconds.

    Returns:
        Decorator function.

    """

    def decorator(
        func: (
            Callable[P, Result[T, E]]
            | Callable[P, Coroutine[Any, Any, Result[T, E]]]
        ),
    ) -> (
        Callable[P, Result[T, TimeoutError | E]]
        | Callable[P, Coroutine[Any, Any, Result[T, TimeoutError | E]]]
    ):
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(
                *args: P.args, **kwargs: P.kwargs
            ) -> Result[T, TimeoutError | E]:
                try:
                    func_coro = cast(
                        Callable[P, Coroutine[Any, Any, Result[T, TimeoutError | E]]],
                        func,
                    )
                    return await asyncio.wait_for(
                        func_coro(*args, **kwargs),
                        timeout=seconds,
                    )
                except TimeoutError:
                    return Err(
                        TimeoutError(f"Execution timed out after {seconds} seconds.")
                    )

            return async_wrapper

        @functools.wraps(func)
        def sync_wrapper(
            *args: P.args, **kwargs: P.kwargs
        ) -> Result[T, TimeoutError | E]:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                func_sync = cast(Callable[P, Result[T, TimeoutError | E]], func)
                future = executor.submit(func_sync, *args, **kwargs)
                try:
                    return future.result(timeout=seconds)
                except concurrent.futures.TimeoutError:
                    return Err(
                        TimeoutError(f"Execution timed out after {seconds} seconds.")
                    )

        return sync_wrapper

    return decorator  # type: ignore[return-value]
