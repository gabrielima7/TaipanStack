import asyncio
import contextlib

import pytest

from taipanstack.core.result import Err
from taipanstack.resilience.adaptive.bulkhead import Bulkhead, BulkheadFullError


@pytest.mark.asyncio
async def test_bulkhead_wait_for_permit_timeout():
    bulk = Bulkhead("test", max_concurrent=1, timeout=0.01)

    async def blocking():
        await asyncio.sleep(0.1)

    t1 = asyncio.create_task(bulk.execute(blocking))
    await asyncio.sleep(0.005)

    result = await bulk.execute(blocking)
    assert isinstance(result, Err)

    t1.cancel()
    with contextlib.suppress(Exception, asyncio.CancelledError):
        await t1

@pytest.mark.asyncio
async def test_bulkhead_wait_for_permit_cancelled():
    bulk = Bulkhead("test", max_concurrent=1, timeout=0.01)

    async def _test():
        task = asyncio.create_task(bulk._semaphore.acquire())
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await bulk._wait_for_permit(task)

    await _test()

@pytest.mark.asyncio
async def test_bulkhead_wait_for_permit_timeout_branch():
    bulk = Bulkhead("test", max_concurrent=1, timeout=0.01)

    async def _test():
        task = asyncio.create_task(bulk._semaphore.acquire())
        # Let it acquire
        await asyncio.sleep(0)
        # Manually inject a TimeoutError during wait

        # We need a custom wait_for wrapper to throw
        async def fake_wait_for(*args, **kwargs):
            raise TimeoutError("fake timeout")

        original_wait = asyncio.wait_for
        asyncio.wait_for = fake_wait_for
        try:
            result = await bulk._wait_for_permit(task)
            assert isinstance(result, Err)
            assert isinstance(result.unwrap_err(), TimeoutError)
        finally:
            asyncio.wait_for = original_wait

    await _test()

@pytest.mark.asyncio
async def test_bulkhead_acquire_permit_resource_exhaustion():
    bulk = Bulkhead("test", max_concurrent=1, timeout=0.01)

    async def _test():
        # Inject an OSError when trying to create a task for semaphore acquire
        original_create_task = asyncio.create_task

        def fake_create_task(*args, **kwargs):
            if args and hasattr(args[0], "close"):
                args[0].close()
            raise OSError("fake OS error")

        asyncio.create_task = fake_create_task
        try:
            result = await bulk._acquire_permit()
            assert isinstance(result, Err)
            assert isinstance(result.unwrap_err(), RuntimeError)
            assert "fake OS error" in str(result.unwrap_err())
        finally:
            asyncio.create_task = original_create_task

    await _test()

@pytest.mark.asyncio
async def test_bulkhead_safe_cancel_task_success_branch():
    bulk = Bulkhead("test", max_concurrent=1, timeout=0.01)

    async def _test():
        task = asyncio.create_task(bulk._semaphore.acquire())
        # Let it acquire
        await asyncio.sleep(0.01)

        # Now call safe_cancel_task on the acquired task
        # It's already completed successfully.
        await bulk._safe_cancel_task(task)
        assert bulk._semaphore._value == 1

    await _test()

@pytest.mark.asyncio
async def test_bulkhead_safe_cancel_task_caught_cancelled():
    bulk = Bulkhead("test", max_concurrent=1, timeout=0.01)

    async def _test():
        # Create a task that will raise CancelledError when awaited inside _safe_cancel_task
        async def dummy():
            raise asyncio.CancelledError()

        task = asyncio.create_task(dummy())
        # Yield to let it start and immediately raise
        await asyncio.sleep(0)

        # It's technically already done with an exception, but _safe_cancel_task should handle it
        await bulk._safe_cancel_task(task)

    await _test()

def test_bulkhead_available_permits_coverage():
    bulk = Bulkhead("test", max_concurrent=5)
    assert bulk.available_permits == 5
    bulk._active = 2
    assert bulk.available_permits == 3

@pytest.mark.asyncio
async def test_bulkhead_queued_property():
    bulk = Bulkhead("test", max_concurrent=1, max_queue=2)
    assert bulk.queued == 0
    bulk._queued = 1
    assert bulk.queued == 1

@pytest.mark.asyncio
async def test_bulkhead_execute_exception_branch():
    bulk = Bulkhead("test", max_concurrent=1)

    async def throwing():
        raise ValueError("test exception")

    result = await bulk.execute(throwing)
    assert isinstance(result, Err)
    assert isinstance(result.unwrap_err(), ValueError)

@pytest.mark.asyncio
async def test_bulkhead_wait_for_permit_cancelled_branch_coverage():
    bulk = Bulkhead("test", max_concurrent=1, timeout=0.01)

    async def _test():
        task = asyncio.create_task(bulk._semaphore.acquire())
        # To simulate cancelation during _wait_for_permit specifically testing the CancelledError path
        async def fake_wait_for(*args, **kwargs):
            raise asyncio.CancelledError()

        original_wait = asyncio.wait_for
        asyncio.wait_for = fake_wait_for
        try:
            with pytest.raises(asyncio.CancelledError):
                await bulk._wait_for_permit(task)
        finally:
            asyncio.wait_for = original_wait

    await _test()



def test_bulkhead_full_error_coverage():
    err = BulkheadFullError("test_name", 10, 20)
    assert err.bulkhead_name == "test_name"
    assert err.max_concurrent == 10
    assert err.max_queue == 20
    assert str(err) == "Bulkhead 'test_name' is full (max_concurrent=10, max_queue=20)"

@pytest.mark.asyncio
async def test_bulkhead_active_property():
    bulk = Bulkhead("test", max_concurrent=2)
    assert bulk.active == 0
    bulk._active = 1
    assert bulk.active == 1

def test_bulkhead_invalid_timeout():
    with pytest.raises(ValueError, match="timeout must be a finite non-negative number"):
        Bulkhead("test", timeout=-1.0)
    with pytest.raises(ValueError, match="timeout must be a finite non-negative number"):
        import math
        Bulkhead("test", timeout=math.nan)

@pytest.mark.asyncio
async def test_bulkhead_queue_full():
    bulk = Bulkhead("test", max_concurrent=1, max_queue=1)
    bulk._queued = 1

    async def _test():
        return True

    result = await bulk.execute(_test)
    assert isinstance(result, Err)
    assert isinstance(result.unwrap_err(), BulkheadFullError)

@pytest.mark.asyncio
async def test_bulkhead_execute_success():
    bulk = Bulkhead("test", max_concurrent=1)

    async def _test():
        return 42

    result = await bulk.execute(_test)
    assert result.is_ok()
    assert result.unwrap() == 42
