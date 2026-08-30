import asyncio
from unittest.mock import patch

import pytest

from taipanstack.resilience.adaptive.bulkhead import Bulkhead


@pytest.mark.asyncio
async def test_chaos_bulkhead_create_task_exception_uncovered_branch():
    bulkhead = Bulkhead(max_concurrent=1, max_queue=1)

    async def dummy():
        return True

    class UnrelatedError(Exception): ...

    with patch(
        "asyncio.create_task", side_effect=UnrelatedError("Chaos create_task error")
    ):
        result = await bulkhead.execute(dummy)
        assert result.is_err()
        assert "Resource exhaustion" in str(result.unwrap_err())

    # ensure no dangling coroutines
    if hasattr(bulkhead._semaphore, "acquire"):
        coro = bulkhead._semaphore.acquire()
        if asyncio.iscoroutine(coro):
            coro.close()
