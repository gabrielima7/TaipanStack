import pytest

from taipanstack.core.result import Err, Ok, Result
from taipanstack.resilience.circuit_breaker import CircuitBreakerError, circuit_breaker


def test_circuit_breaker_with_err_monad_expected():
    @circuit_breaker(failure_threshold=2, failure_exceptions=(ValueError,))
    def flaky_function(fail: bool) -> Result[str, Exception]:
        if fail:
            return Err(ValueError("Chaos failure"))
        return Ok("success")

    res1 = flaky_function(True)
    assert isinstance(res1, Err)
    res2 = flaky_function(True)
    assert isinstance(res2, Err)

    with pytest.raises(CircuitBreakerError, match="is open"):
        flaky_function(True)

@pytest.mark.asyncio
async def test_async_circuit_breaker_with_err_monad_expected():
    @circuit_breaker(failure_threshold=2, failure_exceptions=(ValueError,))
    async def async_flaky_function(fail: bool) -> Result[str, Exception]:
        if fail:
            return Err(ValueError("Chaos failure"))
        return Ok("success")

    res1 = await async_flaky_function(True)
    assert isinstance(res1, Err)
    res2 = await async_flaky_function(True)
    assert isinstance(res2, Err)

    with pytest.raises(CircuitBreakerError, match="is open"):
        await async_flaky_function(True)

def test_circuit_breaker_with_err_monad_not_in_exceptions_expected():
    @circuit_breaker(failure_threshold=2, failure_exceptions=(ValueError,))
    def flaky_function(fail: bool) -> Result[str, Exception]:
        if fail:
            return Err(KeyError("Not tracked"))
        return Ok("success")

    res1 = flaky_function(True)
    assert isinstance(res1, Err)
    res2 = flaky_function(True)
    assert isinstance(res2, Err)

    # Should not open because KeyError is not in failure_exceptions
    res3 = flaky_function(True)
    assert isinstance(res3, Err)

@pytest.mark.asyncio
async def test_async_circuit_breaker_with_err_monad_not_in_exceptions_expected():
    @circuit_breaker(failure_threshold=2, failure_exceptions=(ValueError,))
    async def async_flaky_function(fail: bool) -> Result[str, Exception]:
        if fail:
            return Err(KeyError("Not tracked"))
        return Ok("success")

    res1 = await async_flaky_function(True)
    assert isinstance(res1, Err)
    res2 = await async_flaky_function(True)
    assert isinstance(res2, Err)

    res3 = await async_flaky_function(True)
    assert isinstance(res3, Err)
