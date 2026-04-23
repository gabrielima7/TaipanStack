"""
Intelligent Cache decorator.

Provides in-memory caching that respects the Result monad and TTL,
ignoring caching for Err() results.
"""

import asyncio
import functools
import inspect
import time
from collections.abc import Awaitable, Callable
from typing import ParamSpec, Protocol, TypeAlias, TypeVar, cast, overload

from taipanstack.core.result import Err, Ok, Result

P = ParamSpec("P")
T = TypeVar("T")
E = TypeVar("E", bound=Exception)

CacheKey: TypeAlias = tuple[object, ...]
CacheValue: TypeAlias = tuple[float, object]
CacheDict: TypeAlias = dict[CacheKey, CacheValue]


class CacheDecorator(Protocol):
    """Protocol for the cache decorator."""

    @overload
    def __call__(
        self, func: Callable[P, Result[T, E]]
    ) -> Callable[P, Result[T, E]]: ...

    @overload
    def __call__(
        self, func: Callable[P, Awaitable[Result[T, E]]]
    ) -> Callable[P, Awaitable[Result[T, E]]]: ...


def cached(ttl: float) -> CacheDecorator:  # noqa: PLR0915
    """Cache the Ok() results of a function for a given TTL.

    Err() results are not cached. Supports both async and sync functions.

    Args:
        ttl: Time to live in seconds.

    Returns:
        Decorator function.

    """
    _cache: CacheDict = {}
    _locks: dict[CacheKey, asyncio.Lock] = {}
    _lock_waiters: dict[CacheKey, int] = {}

    def get_cache_key(
        func_name: str, args: tuple[object, ...], kwargs: dict[str, object]
    ) -> CacheKey:
        def _make_hashable(val: object) -> object:
            match val:
                case tuple() | list():
                    return tuple(_make_hashable(item) for item in val)
                case dict():
                    return tuple(sorted((k, _make_hashable(v)) for k, v in val.items()))
                case set():
                    return frozenset(_make_hashable(item) for item in val)
                case _:
                    hash(val)
                    return val

        hashable_args = tuple(_make_hashable(arg) for arg in args)
        hashable_kwargs = tuple(
            sorted((k, _make_hashable(v)) for k, v in kwargs.items())
        )
        return (func_name, hashable_args, hashable_kwargs)

    def decorator(
        func: Callable[P, Result[T, E]] | Callable[P, Awaitable[Result[T, E]]],
    ) -> Callable[P, Result[T, E]] | Callable[P, Awaitable[Result[T, E]]]:
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, E]:
                cache_key = get_cache_key(
                    func.__name__,
                    cast(tuple[object, ...], args),
                    cast(dict[str, object], kwargs),
                )

                # Check cache before acquiring lock
                now = time.monotonic()
                if cache_key in _cache:
                    expiry, value = _cache[cache_key]
                    if now < expiry:
                        return Ok(cast(T, value))

                if cache_key not in _locks:
                    _locks[cache_key] = asyncio.Lock()
                    _lock_waiters[cache_key] = 0

                _lock_waiters[cache_key] += 1
                lock = _locks[cache_key]

                try:
                    async with lock:
                        # Double-check cache after acquiring lock
                        now = time.monotonic()
                        if cache_key in _cache:
                            expiry, value = _cache[cache_key]
                            if now < expiry:
                                return Ok(cast(T, value))
                            del _cache[cache_key]

                        func_coro = cast(Callable[P, Awaitable[Result[T, E]]], func)
                        result = await func_coro(*args, **kwargs)

                        match result:
                            case Ok(value):
                                _cache[cache_key] = (now + ttl, value)
                            case Err(_):
                                pass

                        return result
                finally:
                    _lock_waiters[cache_key] -= 1
                    if _lock_waiters[cache_key] == 0:
                        _locks.pop(cache_key, None)
                        _lock_waiters.pop(cache_key, None)

            return async_wrapper

        @functools.wraps(func)
        def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, E]:
            cache_key = get_cache_key(
                func.__name__,
                cast(tuple[object, ...], args),
                cast(dict[str, object], kwargs),
            )
            now = time.monotonic()

            if cache_key in _cache:
                expiry, value = _cache[cache_key]
                if now < expiry:
                    return Ok(cast(T, value))
                del _cache[cache_key]

            func_sync = cast(Callable[P, Result[T, E]], func)
            result = func_sync(*args, **kwargs)

            match result:
                case Ok(value):
                    _cache[cache_key] = (now + ttl, value)
                case Err(_):
                    pass

            return result

        return sync_wrapper

    return cast(CacheDecorator, decorator)
