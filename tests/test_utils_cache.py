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

    assert compute(5) == Ok(10)
    assert call_count == 1
    assert compute(5) == Ok(10)
    assert call_count == 1
    assert compute(6) == Ok(12)
    assert call_count == 2
    assert isinstance(compute(7, should_fail=True), Err)
    assert call_count == 3
    assert isinstance(compute(7, should_fail=True), Err)
    assert call_count == 4
    time.sleep(0.15)
    assert compute(5) == Ok(10)
    assert call_count == 5


@pytest.mark.asyncio
async def test_utils_cache_cached_async_expected() -> None:
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
    assert isinstance(await compute_async(5, should_fail=True), Err)
    assert call_count == 2
    await asyncio.sleep(0.15)
    assert await compute_async(5) == Ok(10)
    assert call_count == 3


def test_cached_sync_err_branch_expected() -> None:
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
async def test_cached_async_err_branch_expected() -> None:
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
