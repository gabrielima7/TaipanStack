"""Tests for the cache module."""

import asyncio
import time

import pytest

from taipanstack.core.result import Err, Ok, Result
from taipanstack.utils.cache import cached


def test_cached_sync() -> None:
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
async def test_cached_async() -> None:
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

    # Test error bypass
    assert isinstance(await compute_async(5, should_fail=True), Err)
    assert call_count == 2

    # TTL expiration
    await asyncio.sleep(0.15)
    assert await compute_async(5) == Ok(10)
    assert call_count == 3
