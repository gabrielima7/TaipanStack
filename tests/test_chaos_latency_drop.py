import asyncio

import pytest

from taipanstack.resilience.circuit_breaker import CircuitBreakerError, circuit_breaker
from taipanstack.resilience.retry import RetryError, retry


@pytest.mark.asyncio
async def test_chaos_extreme_latency():

    # We want to test that retry handles TimeoutError if the function itself times out
    @retry(max_attempts=2, on=TimeoutError, initial_delay=0.01)
    async def hung_function():
        # Wrap our own sleep in a timeout so it actually raises TimeoutError internally
        await asyncio.wait_for(asyncio.sleep(86400 * 365 * 10), timeout=0.1)
        return "success"

    with pytest.raises(RetryError):
        await hung_function()


@pytest.mark.asyncio
async def test_chaos_intermittent_connection_drops():
    attempts = 0

    @retry(max_attempts=3, on=ConnectionError, initial_delay=0.01)
    async def flaky_connection():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ConnectionError("Connection dropped")
        return "success"

    result = await flaky_connection()
    assert result == "success"
    assert attempts == 3


def test_chaos_resource_exhaustion_circuit_breaker():
    @circuit_breaker(failure_threshold=2)
    def exhaustible_function():
        raise MemoryError("Out of memory")

    with pytest.raises(MemoryError):
        exhaustible_function()

    with pytest.raises(MemoryError):
        exhaustible_function()

    # Circuit should now be open
    with pytest.raises(CircuitBreakerError):
        exhaustible_function()
