from unittest.mock import patch

import pytest

from taipanstack.core.result import Err, Ok
from taipanstack.utils.rate_limit import RateLimiter, rate_limit


def test_chaos_rate_limit_lock_exhaustion_chaos_rate_limit_lock_acquire_exception():
    limiter = RateLimiter(10, 1.0)

    class BrokenLock:
        def __enter__(self):
            raise MemoryError("Out of memory")

        def __exit__(self, _exc_type, _exc_val, _exc_tb):
            raise AssertionError("Should not be reached")

    limiter._lock = BrokenLock()

    result = limiter.consume()
    assert result is False


@pytest.mark.asyncio
async def test_chaos_rate_limit_lock_exhaustion_chaos_rate_limit_decorator_lock_acquire_exception_async():
    @rate_limit(10, 1.0)
    async def my_func():
        return "success"

    with patch(
        "taipanstack.utils.rate_limit.RateLimiter.consume",
        side_effect=MemoryError("Out of memory"),
    ):
        result = await my_func()
        assert isinstance(result, Err)
        assert "Rate limit exceeded" in str(result.unwrap_err())

    # Also test the success path coverage
    result2 = await my_func()
    assert isinstance(result2, Ok)
    assert result2.unwrap() == "success"


def test_chaos_rate_limit_lock_exhaustion_chaos_rate_limit_decorator_lock_acquire_exception_sync():
    @rate_limit(10, 1.0)
    def my_func():
        return "success"

    with patch(
        "taipanstack.utils.rate_limit.RateLimiter.consume",
        side_effect=MemoryError("Out of memory"),
    ):
        result = my_func()
        assert isinstance(result, Err)
        assert "Rate limit exceeded" in str(result.unwrap_err())

    # Also test the success path coverage
    result2 = my_func()
    assert isinstance(result2, Ok)
    assert result2.unwrap() == "success"
