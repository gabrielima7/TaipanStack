
import pytest

from taipanstack.core.result import Err
from taipanstack.utils.rate_limit import RateLimiter, RateLimitError, rate_limit


def test_chaos_rate_limit_decorator_exception():
    @rate_limit(max_calls=1, time_window=1.0)
    def my_func():
        return "success"

    orig_consume = RateLimiter.consume
    def mock_consume(*args, **kwargs):
        return False
    RateLimiter.consume = mock_consume

    res = my_func()
    assert isinstance(res, Err)
    assert isinstance(res.unwrap_err(), RateLimitError)
    RateLimiter.consume = orig_consume

@pytest.mark.asyncio
async def test_chaos_rate_limit_decorator_exception_async():
    @rate_limit(max_calls=1, time_window=1.0)
    async def my_func():
        return "success"

    orig_consume = RateLimiter.consume
    def mock_consume(*args, **kwargs):
        return False
    RateLimiter.consume = mock_consume

    res = await my_func()
    assert isinstance(res, Err)
    assert isinstance(res.unwrap_err(), RateLimitError)
    RateLimiter.consume = orig_consume

def test_chaos_rate_limit_decorator_success_exception():
    @rate_limit(max_calls=1, time_window=1.0)
    def my_func():
        raise RuntimeError("Fail func")

    with pytest.raises(RuntimeError):
        my_func()

@pytest.mark.asyncio
async def test_chaos_rate_limit_decorator_success_exception_async():
    @rate_limit(max_calls=1, time_window=1.0)
    async def my_func():
        raise RuntimeError("Fail func async")

    with pytest.raises(RuntimeError):
        await my_func()
