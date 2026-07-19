"""
Intelligent Cache decorator.

Provides in-memory caching that respects the Result monad and TTL,
ignoring caching for Err() results.
"""

import asyncio
import functools
import inspect
import math
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


def _check_cache(
    cache_key: CacheKey,
    cache: CacheDict,
    now: float,
) -> tuple[bool, object]:
    if cache_key in cache:
        expiry, value = cache[cache_key]
        if now < expiry:
            # Move to end to mark as recently used
            cache[cache_key] = cache.pop(cache_key)
            return True, value
        del cache[cache_key]
    return False, None


def _update_cache(
    cache_key: CacheKey,
    result: Result[T, E],
    cache: CacheDict,
    max_size: int,
    now: float,
    ttl: float,
) -> None:
    if isinstance(result, Ok):
        if len(cache) >= max_size:
            # Evict least recently used (first item)
            lru_key = next(iter(cache))
            del cache[lru_key]
        cache[cache_key] = (now + ttl, result.ok_value)


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


def _get_cache_key(
    func_name: str,
    args: tuple[object, ...],
    kwargs: dict[str, object],
) -> CacheKey:
    hashable_args = tuple(_make_hashable(arg) for arg in args)
    hashable_kwargs = tuple(
        sorted((k, _make_hashable(v)) for k, v in kwargs.items()),
    )
    return (func_name, hashable_args, hashable_kwargs)


def _validate_ttl_max_size(ttl: float, max_size: int) -> None:
    if (
        not isinstance(ttl, (int, float))
        or isinstance(ttl, bool)
        or not math.isfinite(ttl)
        or ttl < 0
    ):
        raise ValueError("ttl must be a finite non-negative number")

    if not isinstance(max_size, int) or isinstance(max_size, bool) or max_size <= 0:
        raise ValueError("max_size must be a positive integer")


def _get_or_create_lock(
    cache_key: CacheKey,
    locks: dict[CacheKey, asyncio.Lock],
    lock_waiters: dict[CacheKey, int],
) -> asyncio.Lock:
    if cache_key not in locks:
        locks[cache_key] = asyncio.Lock()
        lock_waiters[cache_key] = 0

    lock_waiters[cache_key] += 1
    return locks[cache_key]


def _release_lock(
    cache_key: CacheKey,
    locks: dict[CacheKey, asyncio.Lock],
    lock_waiters: dict[CacheKey, int],
) -> None:
    lock_waiters[cache_key] -= 1
    if lock_waiters[cache_key] == 0:
        locks.pop(cache_key, None)
        lock_waiters.pop(cache_key, None)


class CacheDecorator(Protocol):
    """Protocol for the cache decorator."""

    @overload
    def __call__(
        self,
        func: Callable[P, Result[T, E]],
    ) -> Callable[P, Result[T, E]]: ...

    @overload
    def __call__(
        self,
        func: Callable[P, Awaitable[Result[T, E]]],
    ) -> Callable[P, Awaitable[Result[T, E]]]: ...


def cached(ttl: float, max_size: int = 1024) -> CacheDecorator:
    """Cache the Ok() results of a function for a given TTL.

    Err() results are not cached. Supports both async and sync functions.
    Implements LRU (Least Recently Used) eviction when max_size is reached.

    Args:
        ttl: Time to live in seconds.
        max_size: Maximum number of elements to store in the cache.

    Returns:
        Decorator function.

    """
    _validate_ttl_max_size(ttl, max_size)

    _cache: CacheDict = {}
    _locks: dict[CacheKey, asyncio.Lock] = {}
    _lock_waiters: dict[CacheKey, int] = {}

    def decorator(
        func: Callable[P, Result[T, E]] | Callable[P, Awaitable[Result[T, E]]],
    ) -> Callable[P, Result[T, E]] | Callable[P, Awaitable[Result[T, E]]]:
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, E]:
                cache_key = _get_cache_key(
                    cast(str, getattr(func, "__name__", "unknown")),
                    cast(tuple[object, ...], args),
                    cast(dict[str, object], kwargs),
                )

                # Check cache before acquiring lock
                now = time.monotonic()
                hit, value = _check_cache(cache_key, _cache, now)
                if hit:
                    return Ok(cast(T, value))

                lock = _get_or_create_lock(cache_key, _locks, _lock_waiters)

                try:
                    async with lock:
                        # Double-check cache after acquiring lock
                        now = time.monotonic()
                        hit, value = _check_cache(cache_key, _cache, now)
                        if hit:
                            return Ok(cast(T, value))

                        func_coro = cast(Callable[P, Awaitable[Result[T, E]]], func)
                        result = await func_coro(*args, **kwargs)

                        _update_cache(cache_key, result, _cache, max_size, now, ttl)
                        return result
                finally:
                    _release_lock(cache_key, _locks, _lock_waiters)

            return async_wrapper

        @functools.wraps(func)
        def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, E]:
            cache_key = _get_cache_key(
                cast(str, getattr(func, "__name__", "unknown")),
                cast(tuple[object, ...], args),
                cast(dict[str, object], kwargs),
            )
            now = time.monotonic()

            hit, value = _check_cache(cache_key, _cache, now)
            if hit:
                return Ok(cast(T, value))

            func_sync = cast(Callable[P, Result[T, E]], func)
            result = func_sync(*args, **kwargs)

            _update_cache(cache_key, result, _cache, max_size, now, ttl)
            return result

        return sync_wrapper

    return cast(CacheDecorator, decorator)
