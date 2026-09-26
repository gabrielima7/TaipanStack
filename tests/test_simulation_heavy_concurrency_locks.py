import asyncio

import pytest

from taipanstack.resilience.adaptive.adaptive_breaker import AdaptiveCircuitBreaker
from taipanstack.resilience.adaptive.adaptive_retry import AdaptiveRetry


@pytest.mark.asyncio
async def test_adaptive_breaker_concurrency():
    breaker = AdaptiveCircuitBreaker(window_size=1000)

    async def worker():
        await asyncio.to_thread(breaker.record_success)

    tasks = [worker() for _ in range(1000)]
    await asyncio.gather(*tasks)

    assert len(breaker._window) == 1000


@pytest.mark.asyncio
async def test_adaptive_retry_concurrency():
    retry = AdaptiveRetry(window_size=1000)

    async def worker():
        await asyncio.to_thread(retry.record_outcome, 1, True, 0.1)

    tasks = [worker() for _ in range(1000)]
    await asyncio.gather(*tasks)

    assert len(retry._outcomes) == 1000
