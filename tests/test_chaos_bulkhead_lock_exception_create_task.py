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
