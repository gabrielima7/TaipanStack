"""
Intelligent Cache decorator.

Provides in-memory caching that respects the Result monad and TTL,
ignoring caching for Err() results.
"""

import functools
import inspect
import time
from collections.abc import Callable, Coroutine
from typing import Any, ParamSpec, Protocol, TypeVar, cast, overload

from taipanstack.core.result import Err, Ok, Result

P = ParamSpec("P")
T = TypeVar("T")
E = TypeVar("E", bound=Exception)


class CacheDecorator(Protocol):
    """Protocol for the cache decorator."""

    @overload
    def __call__(
        self, func: Callable[P, Result[T, E]]
    ) -> Callable[P, Result[T, E]]: ...  # pragma: no cover

    @overload
    def __call__(
        self, func: Callable[P, Coroutine[Any, Any, Result[T, E]]]
    ) -> Callable[P, Coroutine[Any, Any, Result[T, E]]]: ...  # pragma: no cover


def cached(ttl: float) -> CacheDecorator:
    """Cache the Ok() results of a function for a given TTL.

    Err() results are not cached. Supports both async and sync functions.

    Args:
        ttl: Time to live in seconds.

    Returns:
        Decorator function.

    """
    _cache: dict[tuple[Any, ...], tuple[float, Any]] = {}

    def get_cache_key(
        func_name: str, args: tuple[Any, ...], kwargs: dict[str, Any]
    ) -> tuple[Any, ...]:
        kwargs_tuple = tuple(sorted(kwargs.items()))
        return (func_name, args, kwargs_tuple)

    def decorator(
        func: (
            Callable[P, Result[T, E]] | Callable[P, Coroutine[Any, Any, Result[T, E]]]
        ),
    ) -> Callable[P, Result[T, E]] | Callable[P, Coroutine[Any, Any, Result[T, E]]]:
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, E]:
                cache_key = get_cache_key(
                    func.__name__, args, cast(dict[str, Any], kwargs)
                )
                now = time.monotonic()

                if cache_key in _cache:
                    expiry, value = _cache[cache_key]
                    if now < expiry:
                        return Ok(value)
                    del _cache[cache_key]

                func_coro = cast(Callable[P, Coroutine[Any, Any, Result[T, E]]], func)
                result = await func_coro(*args, **kwargs)

                match result:
                    case Ok(ok_value):
                        _cache[cache_key] = (now + ttl, ok_value)
                    case Err(_):
                        pass

                return result

            return async_wrapper

        @functools.wraps(func)
        def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, E]:
            cache_key = get_cache_key(func.__name__, args, cast(dict[str, Any], kwargs))
            now = time.monotonic()

            if cache_key in _cache:
                expiry, value = _cache[cache_key]
                if now < expiry:
                    return Ok(value)
                del _cache[cache_key]

            func_sync = cast(Callable[P, Result[T, E]], func)
            result = func_sync(*args, **kwargs)

            match result:
                case Ok(ok_value):
                    _cache[cache_key] = (now + ttl, ok_value)
                case Err(_):
                    pass

            return result

        return sync_wrapper

    return decorator  # type: ignore[return-value]
