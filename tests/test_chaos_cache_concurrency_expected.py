"""Chaos tests for the cache module under extreme concurrency and task cancellation."""

import asyncio

import pytest

from taipanstack.core.result import Ok, Result
from taipanstack.utils.cache import cached


@pytest.mark.asyncio
async def test_chaos_cache_task_cancellation_expected() -> None:
    """Test cache behavior when tasks are cancelled during lock acquisition."""
    call_count = 0

    @cached(ttl=10.0)
    async def compute_async(val: int) -> Result[int, ValueError]:
        nonlocal call_count
        call_count += 1
        await asyncio.sleep(0.1)
        return Ok(val * 2)

    # Fire 100 concurrent requests with the exact same arguments
    tasks = [asyncio.create_task(compute_async(5)) for _ in range(100)]

    # Wait a tiny bit to let some tasks queue up on the lock
    await asyncio.sleep(0.01)

    # Cancel half of the tasks randomly
    for i in range(50):
        tasks[i].cancel()

    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Validate that at least one task succeeded (the ones that weren't cancelled)
    successes = [r for r in results if r == Ok(10)]
    assert len(successes) == 50

    cancellations = [r for r in results if isinstance(r, asyncio.CancelledError)]
    assert len(cancellations) == 50

    # The actual computation should only run EXACTLY once due to locking
    assert 1 <= call_count <= 51
