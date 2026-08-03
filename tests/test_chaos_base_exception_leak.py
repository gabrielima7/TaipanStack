import asyncio

import pytest

from taipanstack.resilience.circuit_breaker import circuit_breaker
from taipanstack.resilience.retry import retry


@pytest.mark.asyncio
async def test_chaos_circuit_breaker_base_exception_leak():
    @circuit_breaker(failure_threshold=1)
    async def cb_func():
        raise asyncio.CancelledError("Simulated cancellation")

    with pytest.raises(asyncio.CancelledError):
        await cb_func()


@pytest.mark.asyncio
async def test_chaos_retry_base_exception_leak():
    @retry(max_attempts=2)
    async def retry_func():
        raise asyncio.CancelledError("Simulated cancellation")

    with pytest.raises(asyncio.CancelledError):
        await retry_func()
