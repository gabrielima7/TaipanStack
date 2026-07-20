import asyncio
from unittest.mock import patch

import pytest

from taipanstack.core.result import Err, Ok
from taipanstack.resilience.resilience import timeout


@timeout(1.0)
async def my_async_func():
    return Ok("success")


@timeout(1.0)
def my_sync_func():
    return Ok("success")


@pytest.mark.asyncio
async def test_chaos_resilience_timeout_exceptions_chaos_timeout_async_cancelled_error():
    def side_effect(*args, **kwargs):
        # Prevent "coroutine was never awaited" warning
        args[0].close()
        raise asyncio.CancelledError("mocked cancellation")

    with patch("asyncio.wait_for", side_effect=side_effect):
        with pytest.raises(asyncio.CancelledError) as exc_info:
            await my_async_func()
        assert "mocked cancellation" in str(exc_info.value)


@pytest.mark.asyncio
async def test_chaos_resilience_timeout_exceptions_chaos_timeout_async_overflow_error():
    def side_effect(*args, **kwargs):
        # Prevent "coroutine was never awaited" warning
        args[0].close()
        raise OverflowError("timeout value is too large")

    with patch("asyncio.wait_for", side_effect=side_effect):
        result = await my_async_func()
        assert isinstance(result, Err)
        assert isinstance(result.unwrap_err(), RuntimeError)
        assert "Resource exhaustion" in str(result.unwrap_err())


def test_chaos_resilience_timeout_exceptions_chaos_timeout_sync_overflow_error():
    with patch(
        "threading.Thread.join", side_effect=OverflowError("timeout value is too large")
    ):
        result = my_sync_func()
        assert isinstance(result, Err)
        assert isinstance(result.unwrap_err(), RuntimeError)
        assert "Resource exhaustion" in str(result.unwrap_err())
