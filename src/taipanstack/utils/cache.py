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

from taipanstack.core.result import Ok, Result

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


def cached(ttl: float, max_size: int = 1024) -> CacheDecorator:  # noqa: PLR0915
    """Cache the Ok() results of a function for a given TTL.

    Err() results are not cached. Supports both async and sync functions.
    Implements LRU (Least Recently Used) eviction when max_size is reached.

    Args:
        ttl: Time to live in seconds.
        max_size: Maximum number of elements to store in the cache.

    Returns:
        Decorator function.

    """
    if not isinstance(max_size, int) or isinstance(max_size, bool) or max_size <= 0:
        raise ValueError("max_size must be a positive integer")

    _cache: CacheDict = {}
    _locks: dict[CacheKey, asyncio.Lock] = {}
    _lock_waiters: dict[CacheKey, int] = {}

    def get_cache_key(
        func_name: str, args: tuple[object, ...], kwargs: dict[str, object]
    ) -> CacheKey:
        def _make_hashable(val: object) -> object:
            if isinstance(val, (tuple, list)):
                return tuple(_make_hashable(item) for item in val)
            elif isinstance(val, dict):
                return tuple(sorted((k, _make_hashable(v)) for k, v in val.items()))
            elif isinstance(val, set):
                return frozenset(_make_hashable(item) for item in val)
            else:
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
                        # Move to end to mark as recently used
                        _cache[cache_key] = _cache.pop(cache_key)
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
                                # Move to end to mark as recently used
                                _cache[cache_key] = _cache.pop(cache_key)
                                return Ok(cast(T, value))
                            del _cache[cache_key]

                        func_coro = cast(Callable[P, Awaitable[Result[T, E]]], func)
                        result = await func_coro(*args, **kwargs)

                        if isinstance(result, Ok):
                            if len(_cache) >= max_size:
                                # Evict least recently used (first item)
                                lru_key = next(iter(_cache))
                                del _cache[lru_key]
                            _cache[cache_key] = (now + ttl, result.ok_value)

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
                    # Move to end to mark as recently used
                    _cache[cache_key] = _cache.pop(cache_key)
                    return Ok(cast(T, value))
                del _cache[cache_key]

            func_sync = cast(Callable[P, Result[T, E]], func)
            result = func_sync(*args, **kwargs)

            if isinstance(result, Ok):
                if len(_cache) >= max_size:
                    # Evict least recently used (first item)
                    lru_key = next(iter(_cache))
                    del _cache[lru_key]
                _cache[cache_key] = (now + ttl, result.ok_value)

            return result

        return sync_wrapper

    return cast(CacheDecorator, decorator)
