"""Tests for the resilience module."""

import asyncio
import time

import pytest

from taipanstack.core.result import Err, Ok, Result
from taipanstack.utils.resilience import fallback, timeout


def test_fallback_sync() -> None:
    """Test standard fallback."""

    @fallback(fallback_value="safe")
    def sync_fail(should_fail: bool) -> Result[str, ValueError]:
        if should_fail:
            return Err(ValueError("oops"))
        return Ok("success")

    assert sync_fail(True) == Ok("safe")
    assert sync_fail(False) == Ok("success")

    @fallback(fallback_value="safe", exceptions=(RuntimeError,))
    def sync_raise() -> Result[str, ValueError]:
        raise RuntimeError("crashed")

    assert sync_raise() == Ok("safe")

    @fallback(fallback_value="safe", exceptions=(RuntimeError,))
    def sync_raise_unhandled() -> Result[str, ValueError]:
        raise ValueError("unhandled")

    with pytest.raises(ValueError, match="unhandled"):
        sync_raise_unhandled()


@pytest.mark.asyncio
async def test_fallback_async() -> None:
    """Test async fallback."""

    @fallback(fallback_value="safe_async")
    async def async_fail(should_fail: bool) -> Result[str, ValueError]:
        await asyncio.sleep(0.01)
        if should_fail:
            return Err(ValueError("oops"))
        return Ok("success")

    assert await async_fail(True) == Ok("safe_async")
    assert await async_fail(False) == Ok("success")

    @fallback(fallback_value="safe_async", exceptions=(RuntimeError,))
    async def async_raise() -> Result[str, ValueError]:
        raise RuntimeError("crashed")

    assert await async_raise() == Ok("safe_async")

    @fallback(fallback_value="safe_async", exceptions=(ValueError,))
    async def async_raise_handled() -> Result[str, ValueError]:
        raise ValueError("crashed")

    assert await async_raise_handled() == Ok("safe_async")


def test_timeout_sync() -> None:
    """Test standard timeout."""

    @timeout(0.1)
    def sync_sleep(delay: float) -> Result[str, Exception]:
        time.sleep(delay)
        return Ok("done")

    res_ok = sync_sleep(0.01)
    assert res_ok == Ok("done")

    res_err = sync_sleep(0.2)
    assert isinstance(res_err, Err)
    res_err_instance = res_err.err()
    assert isinstance(res_err_instance, TimeoutError)

    # Test exception propagation
    @timeout(0.1)
    def sync_raise() -> Result[str, ValueError]:
        raise ValueError("crashed")

    with pytest.raises(ValueError, match="crashed"):
        sync_raise()


@pytest.mark.asyncio
async def test_timeout_async() -> None:
    """Test async timeout."""

    @timeout(0.1)
    async def async_sleep(delay: float) -> Result[str, Exception]:
        await asyncio.sleep(delay)
        return Ok("done")

    res_ok = await async_sleep(0.01)
    assert res_ok == Ok("done")

    res_err = await async_sleep(0.2)
    assert isinstance(res_err, Err)
    res_err_instance = res_err.err()
    assert isinstance(res_err_instance, TimeoutError)
