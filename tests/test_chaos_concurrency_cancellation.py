import asyncio

import pytest

from taipanstack.utils.concurrency import limit_concurrency


@pytest.mark.asyncio
async def test_limit_concurrency_cancellation():
    @limit_concurrency(max_tasks=1, timeout=2.0)
    async def task_func(delay: float):
        await asyncio.sleep(delay)
        return "done"

    # Queue a slow task to occupy the semaphore
    slow_future = asyncio.create_task(task_func(0.5))
    await asyncio.sleep(0.1)  # Let it acquire the semaphore

    # Queue another task which should block and wait
    blocked_future = asyncio.create_task(task_func(0.1))
    await asyncio.sleep(0.1)

    # Cancel the blocked task while it's waiting
    blocked_future.cancel()

    with pytest.raises(asyncio.CancelledError):
        await blocked_future

    await slow_future
