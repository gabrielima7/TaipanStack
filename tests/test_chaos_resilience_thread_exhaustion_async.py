from unittest import mock

import pytest

from taipanstack.core.result import Err, Ok
from taipanstack.resilience.resilience import timeout


@pytest.mark.asyncio
async def test_chaos_resilience_thread_exhaustion_async_timeout():
    @timeout(1.0)
    async def my_func():
        return Ok("done")

    async def side_effect(aw, timeout=None):
        aw.close() # cleanup coroutine
        raise RuntimeError("can't start new task")

    with mock.patch(
        "asyncio.wait_for", side_effect=side_effect
    ):
        result = await my_func()
        assert isinstance(result, Err)
        assert "Task exhaustion: can't start new task" in str(result.unwrap_err())
