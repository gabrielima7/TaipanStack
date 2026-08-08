import asyncio
from unittest.mock import patch

import pytest

from taipanstack.resilience.adaptive.bulkhead import Bulkhead


@pytest.mark.asyncio
async def test_chaos_bulkhead_create_task_exception():
    bulkhead = Bulkhead(max_concurrent=1, max_queue=1)

    async def dummy():
        pass

    with patch(
        "asyncio.create_task", side_effect=RuntimeError("Chaos create_task error")
    ):
        result = await bulkhead.execute(dummy)
        assert result.is_err()
        assert "Resource exhaustion" in str(result.unwrap_err())

        # Clean up the dangling coroutine explicitly
        try:
            coro = bulkhead._semaphore.acquire()
            if asyncio.iscoroutine(coro):
                coro.close()
        except RuntimeError:
            pass

    class CustomGenericError(Exception):
        pass

    with patch(
        "asyncio.create_task",
        side_effect=CustomGenericError("Chaos create_task error"),
    ):
        result = await bulkhead.execute(dummy)
        assert result.is_err()
        assert "Resource exhaustion" in str(result.unwrap_err())

        # Clean up the dangling coroutine explicitly
        try:
            coro = bulkhead._semaphore.acquire()
            if asyncio.iscoroutine(coro):
                coro.close()
        except RuntimeError:
            pass


@pytest.mark.asyncio
async def test_chaos_bulkhead_semaphore_acquire_not_awaited():
    bulkhead = Bulkhead(max_concurrent=1, max_queue=1)

    coro_to_close = None

    class BadSemaphore:
        def acquire(self):
            # Act like an un-awaited coroutine to trigger the warning
            async def never_await_me():
                pass

            nonlocal coro_to_close
            coro_to_close = never_await_me()
            return coro_to_close

    bulkhead._semaphore = BadSemaphore()

    async def dummy():
        pass

    # We patch asyncio.create_task to fail immediately so that the
    # mock unawaited coro is never awaited by asyncio
    with patch("asyncio.create_task", side_effect=RuntimeError("mock fail")):
        result = await bulkhead.execute(dummy)
        assert result.is_err()
        assert "mock fail" in str(result.unwrap_err())

        # Manually close it to fix coverage runtime warning
        if coro_to_close is not None:
            coro_to_close.close()


@pytest.mark.asyncio
async def test_chaos_bulkhead_semaphore_acquire_coverage_fallback():
    bulkhead = Bulkhead(max_concurrent=1, max_queue=1)

    class BadSemaphore:
        def acquire(self):
            raise RuntimeError("Fallback coverage")

    bulkhead._semaphore = BadSemaphore()

    async def dummy():
        pass

    result = await bulkhead.execute(dummy)
    assert result.is_err()
    assert "Fallback coverage" in str(result.unwrap_err())


@pytest.mark.asyncio
async def test_chaos_bulkhead_acquire_permit_timeout():
    bulkhead = Bulkhead("test_timeout", max_concurrent=1, max_queue=1, timeout=0.01)

    # Actually trigger the full queue and concurrency to test timeout
    # First, occupy the concurrent slot
    async def dummy_blocker():
        await asyncio.sleep(0.5)

    # We use a timeout of 0.01 for the bulkhead limit
    # The first one takes the permit and blocks
    blocker_task = asyncio.create_task(bulkhead.execute(dummy_blocker))

    # Wait for blocker to start
    await asyncio.sleep(0.05)

    # Now the semaphore is empty and the queue has room (max_queue=1).
    # The second execution will wait for a permit in _acquire_permit,
    # but the timeout is 0.01 and blocker takes 0.5s.
    async def dummy_waiter():
        pass

    # Execute another dummy task which should wait and eventually timeout
    result = await bulkhead.execute(dummy_waiter)
    assert result.is_err()
    assert isinstance(result.unwrap_err(), TimeoutError)

    # Wait for blocker to finish so it cleans up
    await asyncio.wait_for(blocker_task, timeout=1.0)


@pytest.mark.asyncio
async def test_chaos_bulkhead_acquire_permit_cancelled():
    bulkhead = Bulkhead("test_cancelled", max_concurrent=1, max_queue=1)

    async def dummy_blocker():
        await asyncio.sleep(0.5)

    # Occupy the permit
    blocker_task = asyncio.create_task(bulkhead.execute(dummy_blocker))

    # Wait for blocker to start
    await asyncio.sleep(0.05)

    async def dummy_waiter():
        pass

    # Create a task that will wait for the permit
    task = asyncio.create_task(bulkhead.execute(dummy_waiter))

    # Wait a bit for the task to start waiting for the permit
    await asyncio.sleep(0.01)

    # Cancel the task
    task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await task

    # Cleanup the blocker
    await asyncio.wait_for(blocker_task, timeout=1.0)


@pytest.mark.asyncio
async def test_chaos_bulkhead_execute_exception_logged():
    bulkhead = Bulkhead("test_exception", max_concurrent=1, max_queue=1)

    async def dummy_raises():
        raise ValueError("Simulated task error")

    result = await bulkhead.execute(dummy_raises)
    assert result.is_err()
    assert isinstance(result.unwrap_err(), ValueError)
    assert str(result.unwrap_err()) == "Simulated task error"


@pytest.mark.asyncio
async def test_chaos_bulkhead_execute_success():
    bulkhead = Bulkhead("test_success", max_concurrent=1, max_queue=1)

    async def dummy_success():
        return 42

    result = await bulkhead.execute(dummy_success)
    assert result.is_ok()
    assert result.unwrap() == 42


@pytest.mark.asyncio
async def test_chaos_bulkhead_full_queue_error():
    bulkhead = Bulkhead("test_full_queue", max_concurrent=1, max_queue=0)

    async def dummy_blocker():
        await asyncio.sleep(0.5)

    # Occupy the permit
    blocker_task = asyncio.create_task(bulkhead.execute(dummy_blocker))

    # Wait for blocker to start
    await asyncio.sleep(0.05)

    async def dummy():
        return 42

    result = await bulkhead.execute(dummy)
    assert result.is_err()
    assert "is full" in str(result.unwrap_err())
    assert isinstance(result.unwrap_err(), Exception)

    # Cleanup the blocker
    await asyncio.wait_for(blocker_task, timeout=1.0)


@pytest.mark.asyncio
async def test_chaos_bulkhead_properties_and_validation():
    bulkhead = Bulkhead("test_props", max_concurrent=2, max_queue=3, timeout=1.5)

    assert bulkhead.available_permits == 2
    assert bulkhead.queued == 0
    assert bulkhead.active == 0

    with pytest.raises(ValueError, match="max_concurrent"):
        Bulkhead(max_concurrent=0)
    with pytest.raises(ValueError, match="max_concurrent"):
        Bulkhead(max_concurrent=True)

    with pytest.raises(ValueError, match="max_queue"):
        Bulkhead(max_queue=-1)
    with pytest.raises(ValueError, match="max_queue"):
        Bulkhead(max_queue=False)

    with pytest.raises(ValueError, match="timeout"):
        Bulkhead(timeout=-1.0)
    with pytest.raises(ValueError, match="timeout"):
        Bulkhead(timeout=float("inf"))


@pytest.mark.asyncio
async def test_chaos_bulkhead_cleanup_task_suppress_release():
    bulkhead = Bulkhead("test_cleanup", max_concurrent=1, max_queue=1)

    async def dummy():
        pass

    task = asyncio.create_task(dummy())
    # Cancel it immediately
    task.cancel()

    # This should internally attempt to await it and suppress CancelledError,
    # then call _semaphore.release()
    await bulkhead._cleanup_acquire_task(task)

    assert bulkhead.available_permits == 1  # semaphore is released


@pytest.mark.asyncio
async def test_chaos_bulkhead_acquire_permit_cancelled_suppress():
    bulkhead = Bulkhead("test_cancelled", max_concurrent=1, max_queue=1)

    async def dummy():
        pass

    with patch("asyncio.wait_for", side_effect=asyncio.CancelledError):
        # We need it to run the acquire_task inside _acquire_permit,
        # wait_for gets cancelled, it calls _cleanup_acquire_task and re-raises CancelledError
        with pytest.raises(asyncio.CancelledError):
            await bulkhead._acquire_permit()


@pytest.mark.asyncio
async def test_chaos_bulkhead_cleanup_acquire_task_actually_acquires():
    bulkhead = Bulkhead("test_cleanup", max_concurrent=1, max_queue=1)

    # We patch acquire to immediately return True to mock successfully acquiring the lock
    # but the task gets cancelled, so the cleanup has to release it
    # We will do this by simply letting the acquire_task run and finish but simulating CancelledError from the wait_for
    async def fast_acquire():
        await asyncio.sleep(0.001)
        return True

    coro = fast_acquire()
    acquire_task = asyncio.create_task(coro)
    await asyncio.sleep(0.005)  # let it finish and "acquire"

    # The lock was not really acquired since we replaced the task, but wait,
    # _cleanup_acquire_task does `await acquire_task` which will finish now
    # and then calls `self._semaphore.release()`
    # First acquire the real semaphore so it goes to 0
    await bulkhead._semaphore.acquire()

    await bulkhead._cleanup_acquire_task(acquire_task)

    # It should have released the semaphore
    # We can safely test this by calling `locked()` which is standard across Python versions
    assert not bulkhead._semaphore.locked()


@pytest.mark.asyncio
async def test_chaos_bulkhead_coroutine_close_coverage():
    bulkhead = Bulkhead("test_close", max_concurrent=1, max_queue=1)

    async def dummy():
        pass

    with patch("asyncio.create_task", side_effect=RuntimeError("foo")):
        res = await bulkhead.execute(dummy)
        assert res.is_err()
        assert "Resource exhaustion" in str(res.unwrap_err())

    with patch("asyncio.create_task", side_effect=Exception("foo")):
        res = await bulkhead.execute(dummy)
        assert res.is_err()
        assert "Resource exhaustion" in str(res.unwrap_err())


@pytest.mark.asyncio
async def test_chaos_bulkhead_coroutine_close_coverage_not_coro():
    bulkhead = Bulkhead("test_close_not_coro", max_concurrent=1, max_queue=1)

    class BadSemaphoreNotCoro:
        def acquire(self):
            return "not a coroutine"

    bulkhead._semaphore = BadSemaphoreNotCoro()

    async def dummy():
        pass

    with patch("asyncio.create_task", side_effect=RuntimeError("foo")):
        res = await bulkhead.execute(dummy)
        assert res.is_err()
        assert "Resource exhaustion" in str(res.unwrap_err())

    with patch("asyncio.create_task", side_effect=Exception("foo")):
        res = await bulkhead.execute(dummy)
        assert res.is_err()
        assert "Resource exhaustion" in str(res.unwrap_err())
