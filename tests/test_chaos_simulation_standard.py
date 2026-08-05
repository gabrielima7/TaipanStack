import asyncio

import pytest

from taipanstack.core.result import Err, Ok
from taipanstack.resilience import (
    CircuitBreaker,
    ResilienceOrchestrator,
    RetryConfig,
)


@pytest.mark.asyncio
async def test_chaos_simulation():
    breaker = CircuitBreaker(failure_threshold=3, timeout=0.1)
    orch = (
        ResilienceOrchestrator("unreliable")
        .with_circuit_breaker(breaker)
        .with_retry(RetryConfig(max_attempts=3))
        .with_timeout(10.0)
    )

    async def unreliable_task(success: bool):
        if not success:
            raise ValueError("Chaos!")
        return "Success"

    tasks = []
    for _ in range(10):
        tasks.append(orch.execute(unreliable_task, False))

    for _ in range(10):
        tasks.append(orch.execute(unreliable_task, True))

    results = await asyncio.gather(*tasks, return_exceptions=True)
    assert len(results) == 20

    for r in results:
        assert isinstance(r, (Ok, Err)), f"Expected Result monad, got: {type(r)}"
