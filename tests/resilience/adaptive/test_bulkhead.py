"""Tests for the Bulkhead concurrency limiter."""

import asyncio
import contextlib

import pytest

from taipanstack.core.result import Err, Ok
from taipanstack.resilience.adaptive.bulkhead import Bulkhead, BulkheadFullError


class TestBulkhead:
    """Tests for the Bulkhead pattern."""

    @pytest.mark.asyncio
    async def test_execute_success(self) -> None:
        """Successful execution returns Ok."""
        bulk = Bulkhead("test", max_concurrent=5)

        async def task() -> str:
            return "done"

        result = await bulk.execute(task)
        assert isinstance(result, Ok)
        assert result.ok_value == "done"

    @pytest.mark.asyncio
    async def test_execute_failure(self) -> None:
        """Failed execution returns Err."""
        bulk = Bulkhead("test")

        async def failing() -> str:
            msg = "boom"
            raise RuntimeError(msg)

        result = await bulk.execute(failing)
        assert isinstance(result, Err)

    @pytest.mark.asyncio
    async def test_concurrency_limit(self) -> None:
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
    async def test_queue_overflow(self) -> None:
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
        with contextlib.suppress(asyncio.CancelledError):
            await t1
        with contextlib.suppress(asyncio.CancelledError, TimeoutError):
            await t2

    @pytest.mark.asyncio
    async def test_timeout(self) -> None:
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
        with contextlib.suppress(asyncio.CancelledError):
            await task

    @pytest.mark.asyncio
    async def test_permits_tracking(self) -> None:
        """Permits are correctly tracked."""
        bulk = Bulkhead("test", max_concurrent=5)
        assert bulk.available_permits == 5
        assert bulk.queued == 0
        assert bulk.active == 0

    @pytest.mark.asyncio
    async def test_with_arguments(self) -> None:
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
