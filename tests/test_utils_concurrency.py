"""Tests for concurrency utilities."""

import asyncio
import time

import pytest

from taipanstack.utils.concurrency import OverloadError, limit_concurrency


class TestConcurrencyLimiter:
    """Tests for the bulkheading concurrency limiter."""

    def test_invalid_initialization(self) -> None:
        """Test invalid args to limit_concurrency."""
        with pytest.raises(ValueError, match="must be > 0"):
            limit_concurrency(max_tasks=0)
        with pytest.raises(ValueError, match="must be >= 0"):
            limit_concurrency(max_tasks=1, timeout=-1.0)

    def test_sync_limit_concurrency_no_timeout_success(self) -> None:
        """Test sync limit_concurrency with no timeout."""

        @limit_concurrency(max_tasks=1)
        def process() -> int:
            return 42

        res = process()
        assert res.is_ok()
        assert res.ok() == 42

    def test_sync_limit_concurrency_timeout_success(self) -> None:
        """Test sync limit_concurrency with timeout."""

        @limit_concurrency(max_tasks=1, timeout=0.1)
        def process() -> int:
            return 42

        res = process()
        assert res.is_ok()
        assert res.ok() == 42

    def test_sync_limit_concurrency_no_timeout_failure(self) -> None:
        """Test sync limit_concurrency blocking immediately (no timeout)."""
        import threading

        start_event = threading.Event()

        @limit_concurrency(max_tasks=1)
        def slow_process() -> str:
            start_event.set()
            time.sleep(0.1)
            return "done"

        # Start a thread that holds the lock
        t = threading.Thread(target=slow_process)
        t.start()

        # Wait for the thread to actually enter slow_process and acquire the semaphore
        if not start_event.wait(timeout=2.0):
            pytest.fail("Thread failed to start in time")

        # This should fail immediately because max_tasks is 1 and no timeout is set
        res = slow_process()

        # Then we wait for thread to finish
        t.join()

        assert res.is_err()
        assert isinstance(res.err(), OverloadError)

    def test_sync_limit_concurrency_with_timeout_failure(self) -> None:
        """Test sync limit_concurrency blocking and failing after timeout."""
        import threading

        start_event = threading.Event()

        @limit_concurrency(max_tasks=1, timeout=0.05)
        def slow_process() -> str:
            start_event.set()
            time.sleep(0.2)
            return "done"

        t = threading.Thread(target=slow_process)
        t.start()

        # Wait for the thread to actually enter slow_process and acquire the semaphore
        if not start_event.wait(timeout=2.0):
            pytest.fail("Thread failed to start in time")

        res = slow_process()
        t.join()

        assert res.is_err()
        assert isinstance(res.err(), OverloadError)

    @pytest.mark.asyncio
    async def test_async_limit_concurrency_no_timeout_success(self) -> None:
        """Test async limit_concurrency without timeout."""

        @limit_concurrency(max_tasks=1)
        async def fetch_data() -> str:
            return "async data"

        res = await fetch_data()
        assert res.is_ok()
        assert res.ok() == "async data"

    @pytest.mark.asyncio
    async def test_async_limit_concurrency_timeout_success(self) -> None:
        """Test async limit_concurrency with timeout."""

        @limit_concurrency(max_tasks=1, timeout=0.1)
        async def fetch_data() -> str:
            return "async data"

        res = await fetch_data()
        assert res.is_ok()
        assert res.ok() == "async data"

    @pytest.mark.asyncio
    async def test_async_limit_concurrency_no_timeout_failure(self) -> None:
        """Test async limit_concurrency failure without timeout."""

        @limit_concurrency(max_tasks=1)
        async def slow_fetch() -> str:
            await asyncio.sleep(0.1)
            return "done"

        # Start a task that holds the semaphore
        task = asyncio.create_task(slow_fetch())
        await asyncio.sleep(0.01)

        # This should fail immediately since the lock is held
        res = await slow_fetch()
        await task

        assert res.is_err()
        assert isinstance(res.err(), OverloadError)

    @pytest.mark.asyncio
    async def test_async_limit_concurrency_with_timeout_failure(self) -> None:
        """Test async limit_concurrency failure with timeout."""

        @limit_concurrency(max_tasks=1, timeout=0.05)
        async def slow_fetch() -> str:
            await asyncio.sleep(0.2)
            return "done"

        task = asyncio.create_task(slow_fetch())
        await asyncio.sleep(0.01)

        res = await slow_fetch()
        await task

        assert res.is_err()
        assert isinstance(res.err(), OverloadError)
