"""Tests for the Bulkhead concurrency limiter."""

import asyncio

import pytest

from taipanstack.core.result import Err, Ok
from taipanstack.resilience.adaptive.bulkhead import (
    Bulkhead,
    BulkheadFullError,
)


class TestBulkhead:
    """Tests for the Bulkhead pattern."""

    @pytest.mark.asyncio
    async def test_bulkhead_execute_success(self) -> None:
        """Successful execution returns Ok."""
        bulk = Bulkhead("test", max_concurrent=5)

        async def task() -> str:
            return "done"

        result = await bulk.execute(task)
        assert isinstance(result, Ok)
        assert result.ok_value == "done"

    @pytest.mark.asyncio
    async def test_bulkhead_execute_failure(self) -> None:
        """Failed execution returns Err."""
        bulk = Bulkhead("test")

        async def failing() -> str:
            msg = "boom"
            raise RuntimeError(msg)

        result = await bulk.execute(failing)
        assert isinstance(result, Err)

    @pytest.mark.asyncio
    async def test_bulkhead_concurrency_limit(self) -> None:
        """Only max_concurrent tasks run simultaneously."""
        max_seen = 0
        current = 0
        lock = asyncio.Lock()

        bulk = Bulkhead("test", max_concurrent=2, max_queue=10)

        async def tracked_task() -> int:
            nonlocal max_seen, current
            async with lock:
                current += 1
                max_seen = max(max_seen, current)
            await asyncio.sleep(0.05)
            async with lock:
                current -= 1
            return 1

        tasks = [bulk.execute(tracked_task) for _ in range(5)]
        results = await asyncio.gather(*tasks)

        assert all(isinstance(r, Ok) for r in results)
        assert max_seen <= 2

    @pytest.mark.asyncio
    async def test_bulkhead_queue_overflow(self) -> None:
        """Returns Err when queue is full."""
        # max_concurrent=1 + max_queue=1 means: 1 running + 1 waiting = full
        bulk = Bulkhead("test", max_concurrent=1, max_queue=1, timeout=1.0)
        gate = asyncio.Event()

        async def blocking() -> None:
            await gate.wait()

        # Task 1: acquires the semaphore and blocks
        t1 = asyncio.create_task(bulk.execute(blocking))
        await asyncio.sleep(0.05)

        # Task 2: queues waiting for the semaphore (fills queue)
        t2 = asyncio.create_task(bulk.execute(blocking))
        await asyncio.sleep(0.05)

        # Task 3: queue is full → should fail immediately
        result = await bulk.execute(blocking)
        assert isinstance(result, Err)
        assert isinstance(result.err_value, BulkheadFullError)

        # Cleanup
        gate.set()
        t1.cancel()
        t2.cancel()
        raised_t1 = False
        try:
            await t1
        except asyncio.CancelledError:
            raised_t1 = True
        assert raised_t1

        raised_t2 = False
        try:
            await t2
        except (asyncio.CancelledError, TimeoutError):
            raised_t2 = True
        assert raised_t2

    @pytest.mark.asyncio
    async def test_bulkhead_timeout_ok(self) -> None:
        """Returns Err on permit acquisition timeout."""
        bulk = Bulkhead("test", max_concurrent=1, max_queue=5, timeout=0.05)

        async def blocking() -> None:
            await asyncio.sleep(10)

        # Acquire the only permit
        task = asyncio.create_task(bulk.execute(blocking))
        await asyncio.sleep(0.01)

        # This should timeout waiting for a permit
        result = await bulk.execute(blocking)
        assert isinstance(result, Err)
        assert "timed out" in str(result.err_value)

        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

    @pytest.mark.asyncio
    async def test_bulkhead_permits_tracking(self) -> None:
        """Permits are correctly tracked."""
        bulk = Bulkhead("test", max_concurrent=5)
        assert bulk.available_permits == 5
        assert bulk.queued == 0
        assert bulk.active == 0

    @pytest.mark.asyncio
    async def test_bulkhead_with_arguments(self) -> None:
        """Execute passes args/kwargs correctly."""
        bulk = Bulkhead("test")

        async def add(a: int, b: int) -> int:
            return a + b

        result = await bulk.execute(add, 3, b=4)
        assert isinstance(result, Ok)
        assert result.ok_value == 7

    def test_bulkhead_full_error(self) -> None:
        """BulkheadFullError contains metadata."""
        err = BulkheadFullError("api", 10, 50)
        assert err.bulkhead_name == "api"
        assert err.max_concurrent == 10
        assert "full" in str(err).lower()

    @pytest.mark.asyncio
    async def test_bulkhead_cancellation_release(self) -> None:
        """Test that semaphore is released if task is cancelled after permit acquisition."""
        from unittest.mock import patch

        bulk = Bulkhead("test", max_concurrent=1, max_queue=5, timeout=0.1)

        async def mock_wait_for(fut, timeout):
            await fut
            raise asyncio.CancelledError()

        with patch("asyncio.wait_for", mock_wait_for):
            with pytest.raises(asyncio.CancelledError):
                await bulk.execute(asyncio.sleep, 1)

        assert bulk._semaphore._value == 1

    @pytest.mark.asyncio
    async def test_bulkhead_queued_cancellation(self) -> None:
        """Test that a queued task can be cancelled while waiting, and cleans up its acquire task."""
        bulk = Bulkhead("test", max_concurrent=1, max_queue=5)
        gate = asyncio.Event()

        async def blocking():
            await gate.wait()

        t1 = asyncio.create_task(bulk.execute(blocking))
        await asyncio.sleep(0.01)

        t2 = asyncio.create_task(bulk.execute(blocking))
        await asyncio.sleep(0.01)

        # Cancel t2 while it is waiting in the queue
        t2.cancel()
        with pytest.raises(asyncio.CancelledError):
            await t2

        # Cleanup t1
        gate.set()
        await t1

    @pytest.mark.asyncio
    async def test_bulkhead_timeout_release_on_race(self) -> None:
        """Test that semaphore is released if TimeoutError occurs but permit was acquired."""
        from unittest.mock import patch

        bulk = Bulkhead("test", max_concurrent=1, max_queue=5, timeout=0.1)

        async def mock_wait_for(fut, timeout):
            await fut
            raise TimeoutError()

        with patch("asyncio.wait_for", mock_wait_for):
            result = await bulk.execute(asyncio.sleep, 0.01)
            assert isinstance(result, Err)
            assert isinstance(result.err_value, TimeoutError)

        assert bulk._semaphore._value == 1
