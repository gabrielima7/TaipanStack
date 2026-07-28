import pytest

from taipanstack.core.result import Err, Ok
from taipanstack.utils.rate_limit import RateLimiter, rate_limit


def test_rate_limit_deadlock_chaos_returns_false():
    limiter = RateLimiter(10, 1.0)

    # Simulate contention/deadlock
    limiter._lock.acquire()

    # Should not block indefinitely, should timeout and return False
    result = limiter.consume()
    assert result is False

    # Clean up so test doesn't hang if it failed
    limiter._lock.release()

@pytest.mark.asyncio
async def test_rate_limit_deadlock_chaos_async_decorator():
    @rate_limit(10, 1.0)
    async def my_func():
        return "success"

    limiter = None
    if hasattr(my_func, "__closure__") and my_func.__closure__:
        for cell in my_func.__closure__:
            if isinstance(cell.cell_contents, RateLimiter):
                limiter = cell.cell_contents
                break

    assert limiter is not None
    limiter._lock.acquire()

    result = await my_func()
    assert isinstance(result, Err)
    assert "Rate limit exceeded" in str(result.unwrap_err())

    limiter._lock.release()

def test_rate_limit_deadlock_chaos_sync_decorator():
    @rate_limit(10, 1.0)
    def my_func():
        return "success"

    limiter = None
    if hasattr(my_func, "__closure__") and my_func.__closure__:
        for cell in my_func.__closure__:
            if isinstance(cell.cell_contents, RateLimiter):
                limiter = cell.cell_contents
                break

    assert limiter is not None
    limiter._lock.acquire()

    result = my_func()
    assert isinstance(result, Err)
    assert "Rate limit exceeded" in str(result.unwrap_err())

    limiter._lock.release()
