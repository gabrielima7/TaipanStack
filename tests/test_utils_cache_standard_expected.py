"""Tests for the cache module."""

import asyncio
import time

import pytest

from taipanstack.core.result import Err, Ok, Result
from taipanstack.utils.cache import cached


def test_utils_cache_cached_sync_expected() -> None:
    """Test standard sync cache."""
    call_count = 0

    @cached(ttl=0.1)
    def compute(val: int, should_fail: bool = False) -> Result[int, ValueError]:
        nonlocal call_count
        call_count += 1
        if should_fail:
            return Err(ValueError("failed"))
        return Ok(val * 2)

    # First call, computes
    assert compute(5) == Ok(10)
    assert call_count == 1

    # Second call, cached
    assert compute(5) == Ok(10)
    assert call_count == 1

    # Different args, computes
    assert compute(6) == Ok(12)
    assert call_count == 2

    # Fails, not cached
    assert isinstance(compute(7, should_fail=True), Err)
    assert call_count == 3
    assert isinstance(compute(7, should_fail=True), Err)
    assert call_count == 4

    # TTL expiration
    time.sleep(0.15)
    assert compute(5) == Ok(10)
    assert call_count == 5


@pytest.mark.asyncio
async def test_utils_cache_cached_async() -> None:
    """Test async cache."""
    call_count = 0

    @cached(ttl=0.1)
    async def compute_async(
        val: int, should_fail: bool = False
    ) -> Result[int, ValueError]:
        nonlocal call_count
        call_count += 1
        await asyncio.sleep(0.01)
        if should_fail:
            return Err(ValueError("failed"))
        return Ok(val * 2)

    assert await compute_async(5) == Ok(10)
    assert call_count == 1

    assert await compute_async(5) == Ok(10)
    assert call_count == 1

    # Test error is not cached and correctly bypasses
    assert isinstance(await compute_async(5, should_fail=True), Err)
    assert call_count == 2

    # TTL expiration
    await asyncio.sleep(0.15)
    assert await compute_async(5) == Ok(10)
    assert call_count == 3


def test_utils_cache_cached_sync_err_branch_expected() -> None:
    call_count = 0

    @cached(ttl=0.1)
    def compute() -> Result[int, ValueError]:
        nonlocal call_count
        call_count += 1
        return Err(ValueError("err"))

    assert isinstance(compute(), Err)
    assert call_count == 1
    assert isinstance(compute(), Err)
    assert call_count == 2


@pytest.mark.asyncio
async def test_utils_cache_cached_async_err_branch_expected() -> None:
    call_count = 0

    @cached(ttl=0.1)
    async def compute() -> Result[int, ValueError]:
        nonlocal call_count
        call_count += 1
        return Err(ValueError("err"))

    assert isinstance(await compute(), Err)
    assert call_count == 1
    assert isinstance(await compute(), Err)
    assert call_count == 2


@pytest.mark.asyncio
async def test_utils_cache_async_cache_stampede_prevention_expected() -> None:
    """Test that multiple concurrent requests for the same key don't stampede."""
    call_count = 0

    @cached(ttl=1.0)
    async def compute_async(val: int) -> Result[int, ValueError]:
        nonlocal call_count
        call_count += 1
        await asyncio.sleep(0.1)
        return Ok(val * 2)

    # Fire 100 concurrent requests with the exact same arguments
    results = await asyncio.gather(*(compute_async(5) for _ in range(100)))

    # All should return Ok(10)
    for result in results:
        assert result == Ok(10)

    # The actual computation should only run EXACTLY once due to locking
    assert call_count == 1


def test_utils_cache_cached_sync_lru_eviction_expected() -> None:
    """Test LRU eviction for sync cache."""
    call_count = 0

    @cached(ttl=60.0, max_size=2)
    def compute(val: int) -> Result[int, ValueError]:
        nonlocal call_count
        call_count += 1
        return Ok(val * 2)

    # Fill cache
    assert compute(1) == Ok(2)
    assert call_count == 1
    assert compute(2) == Ok(4)
    assert call_count == 2

    # Access 1 so 2 becomes least recently used
    assert compute(1) == Ok(2)
    assert call_count == 2

    # Add 3, which should evict 2
    assert compute(3) == Ok(6)
    assert call_count == 3

    # Access 2, should be recomputed
    assert compute(2) == Ok(4)
    assert call_count == 4


@pytest.mark.asyncio
async def test_utils_cache_cached_async_lru_eviction_expected() -> None:
    """Test LRU eviction for async cache."""
    call_count = 0

    @cached(ttl=60.0, max_size=2)
    async def compute_async(val: int) -> Result[int, ValueError]:
        nonlocal call_count
        call_count += 1
        return Ok(val * 2)

    # Fill cache
    assert await compute_async(1) == Ok(2)
    assert call_count == 1
    assert await compute_async(2) == Ok(4)
    assert call_count == 2

    # Access 1 so 2 becomes least recently used
    assert await compute_async(1) == Ok(2)
    assert call_count == 2

    # Add 3, which should evict 2
    assert await compute_async(3) == Ok(6)
    assert call_count == 3

    # Access 2, should be recomputed
    assert await compute_async(2) == Ok(4)
    assert call_count == 4


def test_utils_cache_invalid_max_size_expected() -> None:
    """Test invalid max_size raises ValueError."""
    with pytest.raises(ValueError, match="max_size must be a positive integer"):

        @cached(ttl=1.0, max_size=0)
        def compute_sync(val: int) -> Result[int, ValueError]:
            return Ok(val * 2)

    with pytest.raises(ValueError, match="max_size must be a positive integer"):

        @cached(ttl=1.0, max_size=-1)
        def compute_sync_negative(val: int) -> Result[int, ValueError]:
            return Ok(val * 2)

    with pytest.raises(ValueError, match="max_size must be a positive integer"):

        @cached(ttl=1.0, max_size=1.5)  # type: ignore
        def compute_sync_float(val: int) -> Result[int, ValueError]:
            return Ok(val * 2)

    with pytest.raises(ValueError, match="max_size must be a positive integer"):

        @cached(ttl=1.0, max_size=False)  # type: ignore
        def compute_sync_bool(val: int) -> Result[int, ValueError]:
            return Ok(val * 2)
