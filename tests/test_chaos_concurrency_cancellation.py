import asyncio

import pytest

from taipanstack.utils.concurrency import limit_concurrency


@pytest.mark.asyncio
async def test_limit_concurrency_cancellation():
    started_event = asyncio.Event()
    release_event = asyncio.Event()

    @limit_concurrency(max_tasks=1, timeout=2.0)
    async def task_func():
        if not started_event.is_set():
            started_event.set()
            await release_event.wait()
        return "done"

    # Queue a task to occupy the semaphore
    slow_task = asyncio.create_task(task_func())
    await started_event.wait()  # Ensure semaphore is acquired deterministically

    # Queue another task which should block waiting for the same semaphore
    blocked_task = asyncio.create_task(task_func())
    await asyncio.sleep(0.05)  # Yield control to let blocked_task attempt acquire

    # Cancel the blocked task while it's waiting
    blocked_task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await blocked_task

    # Release the first task
    release_event.set()
    await slow_task
