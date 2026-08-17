import asyncio
from unittest.mock import patch

import pytest

from taipanstack.resilience.adaptive.bulkhead import Bulkhead


@pytest.mark.asyncio
async def test_chaos_bulkhead_create_task_exception():
    bulkhead = Bulkhead(max_concurrent=1, max_queue=1)

    async def dummy():
        return True

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
            return None

    class CustomGenericError(Exception):
        """Mock class for testing."""

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
            return None


@pytest.mark.asyncio
async def test_chaos_bulkhead_semaphore_acquire_not_awaited():
    bulkhead = Bulkhead(max_concurrent=1, max_queue=1)

    coro_to_close = None

    class BadSemaphore:
        def acquire(self):
            # Act like an un-awaited coroutine to trigger the warning
            async def never_await_me():
                return True

            nonlocal coro_to_close
            coro_to_close = never_await_me()
            return coro_to_close

    bulkhead._semaphore = BadSemaphore()

    async def dummy():
        return True

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
        return True

    result = await bulkhead.execute(dummy)
    assert result.is_err()
    assert "Fallback coverage" in str(result.unwrap_err())


@pytest.mark.asyncio
async def test_chaos_bulkhead_acquire_permit_timeout():
    bulkhead = Bulkhead("test_timeout", max_concurrent=1, max_queue=1, timeout=0.05)
    started_event = asyncio.Event()
    release_event = asyncio.Event()

    async def dummy_blocker():
        started_event.set()
        await release_event.wait()

    blocker_task = asyncio.create_task(bulkhead.execute(dummy_blocker))
    await started_event.wait()

    async def dummy_waiter():
        return True

    result = await bulkhead.execute(dummy_waiter)
    assert result.is_err()
    assert isinstance(result.unwrap_err(), TimeoutError)

    release_event.set()
    await asyncio.wait_for(blocker_task, timeout=1.0)


@pytest.mark.asyncio
async def test_chaos_bulkhead_acquire_permit_cancelled():
    bulkhead = Bulkhead("test_cancelled", max_concurrent=1, max_queue=1)
    started_event = asyncio.Event()
    release_event = asyncio.Event()

    async def dummy_blocker():
        started_event.set()
        await release_event.wait()

    blocker_task = asyncio.create_task(bulkhead.execute(dummy_blocker))
    await started_event.wait()

    async def dummy_waiter():
        return True

    task = asyncio.create_task(bulkhead.execute(dummy_waiter))
    await asyncio.sleep(0.01)

    task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await task

    release_event.set()
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
    bulkhead = Bulkhead("test_full_queue", max_concurrent=1, max_queue=1)
    started_event = asyncio.Event()
    release_event = asyncio.Event()

    async def dummy_blocker():
        started_event.set()
        await release_event.wait()

    blocker_task = asyncio.create_task(bulkhead.execute(dummy_blocker))
    await started_event.wait()

    async def dummy_waiter():
        await release_event.wait()

    waiter_task = asyncio.create_task(bulkhead.execute(dummy_waiter))
    await asyncio.sleep(0.01)

    async def dummy():
        return 42

    result = await bulkhead.execute(dummy)
    assert result.is_err()
    assert "is full" in str(result.unwrap_err())
    assert isinstance(result.unwrap_err(), Exception)

    release_event.set()
    await asyncio.wait_for(blocker_task, timeout=1.0)
    await asyncio.wait_for(waiter_task, timeout=1.0)


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
        return True

    task = asyncio.create_task(dummy())
    task.cancel()

    await bulkhead._cleanup_acquire_task(task)

    assert bulkhead.available_permits == 1


@pytest.mark.asyncio
async def test_chaos_bulkhead_acquire_permit_cancelled_suppress():
    bulkhead = Bulkhead("test_cancelled", max_concurrent=1, max_queue=1)

    async def dummy():
        return True

    with patch("asyncio.wait_for", side_effect=asyncio.CancelledError):
        with pytest.raises(asyncio.CancelledError):
            await bulkhead._acquire_permit()


@pytest.mark.asyncio
async def test_chaos_bulkhead_cleanup_acquire_task_actually_acquires():
    bulkhead = Bulkhead("test_cleanup", max_concurrent=1, max_queue=1)

    finish_event = asyncio.Event()

    async def fast_acquire():
        finish_event.set()
        return True

    coro = fast_acquire()
    acquire_task = asyncio.create_task(coro)
    await finish_event.wait()

    await bulkhead._semaphore.acquire()
    await bulkhead._cleanup_acquire_task(acquire_task)

    assert not bulkhead._semaphore.locked()


@pytest.mark.asyncio
async def test_chaos_bulkhead_coroutine_close_coverage():
    bulkhead = Bulkhead("test_close", max_concurrent=1, max_queue=1)

    async def dummy():
        return True

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
        return True

    with patch("asyncio.create_task", side_effect=RuntimeError("foo")):
        res = await bulkhead.execute(dummy)
        assert res.is_err()
        assert "Resource exhaustion" in str(res.unwrap_err())

    with patch("asyncio.create_task", side_effect=Exception("foo")):
        res = await bulkhead.execute(dummy)
        assert res.is_err()
        assert "Resource exhaustion" in str(res.unwrap_err())
