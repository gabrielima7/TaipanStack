from unittest.mock import patch

import pytest

from taipanstack.core.result import Err
from taipanstack.utils.concurrency import OverloadError, limit_concurrency


def test_chaos_concurrency_resource_exhaustion_sync_concurrency_memoryerror_chaos_returns_err_execution_success():
    @limit_concurrency(max_tasks=1)
    def dummy_task():
        return "success"

    with patch("threading.Semaphore.acquire", side_effect=MemoryError("Out of memory")):
        result = dummy_task()
        assert isinstance(result, Err)
        assert isinstance(result.unwrap_err(), OverloadError)
        assert "Resource exhaustion" in str(result.unwrap_err())


@pytest.mark.asyncio
async def test_chaos_concurrency_resource_exhaustion_async_concurrency_oserror_chaos_returns_err_execution_success():
    @limit_concurrency(max_tasks=1)
    async def dummy_task():
        return "success"

    with patch("asyncio.Semaphore.acquire", side_effect=OSError("Too many open files")):
        result = await dummy_task()
        assert isinstance(result, Err)
        assert isinstance(result.unwrap_err(), OverloadError)
        assert "Resource exhaustion" in str(result.unwrap_err())
