import pytest

from taipanstack.core.result import Err, Ok
from taipanstack.resilience.retry import retry


def test_retry_result_monad_chaos():
    attempts = 0

    @retry(max_attempts=3, on=(ValueError,))
    def failing_func():
        nonlocal attempts
        attempts += 1
        return Err(ValueError("Chaos failure wrapped in Result"))

    _ = failing_func()

    # If retry handles Result monads correctly, it should have retried 3 times
    assert attempts == 3, f"Expected 3 attempts, got {attempts}"


def test_retry_result_monad_chaos_coverage():
    attempts = 0

    @retry(max_attempts=1, on=(ValueError,))
    def failing_func():
        nonlocal attempts
        attempts += 1
        return Ok("success")

    _ = failing_func()
    assert attempts == 1

    @retry(max_attempts=1, on=(ValueError,))
    def fail_with_exception():
        raise ValueError("failure")

    with pytest.raises(Exception, match="All 1 attempts failed"):
        fail_with_exception()


@pytest.mark.asyncio
async def test_retry_result_monad_chaos_coverage_async():
    attempts = 0

    @retry(max_attempts=1, on=(ValueError,))
    async def failing_func():
        nonlocal attempts
        attempts += 1
        return Ok("success")

    _ = await failing_func()
    assert attempts == 1

    @retry(max_attempts=1, on=(ValueError,))
    async def fail_with_exception():
        raise ValueError("failure")

    with pytest.raises(Exception, match="All 1 attempts failed"):
        await fail_with_exception()


def test_retry_result_monad_chaos_sync_not_on():
    @retry(max_attempts=3, on=(ValueError,))
    def failing_func():
        return Err(TypeError("Not on"))

    result = failing_func()
    assert isinstance(result, Err)


@pytest.mark.asyncio
async def test_retry_result_monad_chaos_async_not_on():
    @retry(max_attempts=3, on=(ValueError,))
    async def failing_func():
        return Err(TypeError("Not on"))

    result = await failing_func()
    assert isinstance(result, Err)


@pytest.mark.asyncio
async def test_retry_result_monad_chaos_exhaust_async():
    @retry(max_attempts=2, on=(ValueError,))
    async def failing_func():
        return Err(ValueError("Chaos failure wrapped in Result"))

    result = await failing_func()
    assert isinstance(result, Err)


def test_retry_result_monad_chaos_exhaust_sync():
    @retry(max_attempts=2, on=(ValueError,))
    def failing_func():
        return Err(ValueError("Chaos failure wrapped in Result"))

    result = failing_func()
    assert isinstance(result, Err)
