from unittest import mock

import pytest

from taipanstack.core.result import Err, Ok
from taipanstack.resilience.resilience import timeout


@pytest.mark.asyncio
async def test_chaos_resilience_memory_exhaustion_async_timeout_execution_success():
    @timeout(1.0)
    async def my_func():
        return Ok("done")

    async def side_effect(aw, timeout=None):
        aw.close()  # cleanup coroutine
        raise MemoryError("out of memory")

    with mock.patch("asyncio.wait_for", side_effect=side_effect):
        result = await my_func()
        assert isinstance(result, Err)
        assert "Memory exhaustion: out of memory" in str(result.unwrap_err())


@pytest.mark.asyncio
async def test_chaos_resilience_resource_exhaustion_async_timeout_execution_success():
    @timeout(1.0)
    async def my_func():
        return Ok("done")

    async def side_effect(aw, timeout=None):
        aw.close()  # cleanup coroutine
        raise OSError("too many open files")

    with mock.patch("asyncio.wait_for", side_effect=side_effect):
        result = await my_func()
        assert isinstance(result, Err)
        assert "Resource exhaustion: too many open files" in str(result.unwrap_err())
