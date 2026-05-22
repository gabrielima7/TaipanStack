"""Chaos tests for resilience components."""

import pytest

from taipanstack.core.result import Err, Ok, Result
from taipanstack.resilience.resilience import timeout


def test_utils_resilience_chaos_timeout_sync_chaos_nan() -> None:
    """Test chaos: NaN timeout causes system crash rather than safe degradation."""

    @timeout(float("nan"))
    def sync_sleep(delay: float) -> Result[str, Exception]:
        return Ok("done")

    res = sync_sleep(0.01)
    assert isinstance(res, Err)
    assert isinstance(res.err_value, ValueError)
    assert "finite non-negative" in str(res.err_value).lower()


def test_utils_resilience_chaos_timeout_sync_chaos_negative() -> None:
    """Test chaos: Negative timeout causes system crash."""

    @timeout(-1.0)
    def sync_sleep(delay: float) -> Result[str, Exception]:
        return Ok("done")

    res = sync_sleep(0.01)
    assert isinstance(res, Err)
    assert isinstance(res.err_value, ValueError)
    assert "finite non-negative" in str(res.err_value).lower()


@pytest.mark.asyncio
async def test_utils_resilience_chaos_timeout_async_chaos_nan() -> None:
    """Test chaos: NaN timeout causes unhandled cancellation in async code."""

    @timeout(float("nan"))
    async def async_sleep(delay: float) -> Result[str, Exception]:
        return Ok("done")

    res = await async_sleep(0.01)
    assert isinstance(res, Err)
    assert isinstance(res.err_value, ValueError)
    assert "finite non-negative" in str(res.err_value).lower()


@pytest.mark.asyncio
async def test_utils_resilience_chaos_timeout_async_chaos_negative() -> None:
    """Test chaos: Negative timeout on async."""

    @timeout(-1.0)
    async def async_sleep(delay: float) -> Result[str, Exception]:
        return Ok("done")

    res = await async_sleep(0.01)
    assert isinstance(res, Err)
    assert isinstance(res.err_value, ValueError)
    assert "finite non-negative" in str(res.err_value).lower()
