import asyncio
from unittest.mock import patch

import pytest

from taipanstack.core.result import Err, Ok
from taipanstack.resilience.resilience import timeout
from taipanstack.resilience.retry import RetryError, retry


def test_sync_timeout_thread_start_generic_exhaustion():
    @timeout(1.0)
    def my_func():
        return Ok("success")

    with patch("threading.Thread.start", side_effect=Exception("OS thread error")):
        res = my_func()
        assert isinstance(res, Err)
        assert "Thread exhaustion" in str(res.unwrap_err()) or "OS thread error" in str(res.unwrap_err())

def test_sync_timeout_thread_start_system_exit():
    @timeout(1.0)
    def my_func():
        return Ok("success")

    with patch("threading.Thread.start", side_effect=SystemExit(1)):
        with pytest.raises(SystemExit):
            my_func()

@pytest.mark.asyncio
async def test_async_timeout_wait_for_generic_exhaustion():
    @timeout(1.0)
    async def my_func():
        return Ok("success")

    with patch("asyncio.wait_for", side_effect=Exception("mocked task exhaustion")):
        res = await my_func()
        assert isinstance(res, Err)
        assert "Task exhaustion" in str(res.unwrap_err()) or "mocked task exhaustion" in str(res.unwrap_err())

@pytest.mark.asyncio
async def test_async_timeout_wait_for_cancelled_error():
    @timeout(1.0)
    async def my_func():
        return Ok("success")

    with patch("asyncio.wait_for", side_effect=asyncio.CancelledError()):
        with pytest.raises(asyncio.CancelledError):
            await my_func()


def test_sync_retry_sleep_generic_exhaustion():
    @retry(max_attempts=3, initial_delay=0.1)
    def my_func():
        raise ValueError("initial fail")

    with patch("time.sleep", side_effect=Exception("mocked sleep failure")):
        with pytest.raises(RetryError) as exc_info:
            my_func()
        assert "All 3 attempts failed" in str(exc_info.value)
        assert hasattr(exc_info.value, "last_exception")
        assert "mocked sleep failure" in str(exc_info.value.last_exception)

def test_sync_retry_sleep_system_exit():
    @retry(max_attempts=3, initial_delay=0.1)
    def my_func():
        raise ValueError("initial fail")

    with patch("time.sleep", side_effect=SystemExit(1)):
        with pytest.raises(SystemExit):
            my_func()

@pytest.mark.asyncio
async def test_async_retry_sleep_generic_exhaustion():
    @retry(max_attempts=3, initial_delay=0.1)
    async def my_func():
        raise ValueError("initial fail")

    with patch("asyncio.sleep", side_effect=Exception("mocked async sleep failure")):
        with pytest.raises(RetryError) as exc_info:
            await my_func()
        assert "All 3 attempts failed" in str(exc_info.value)
        assert hasattr(exc_info.value, "last_exception")
        assert "mocked async sleep failure" in str(exc_info.value.last_exception)


@pytest.mark.asyncio
async def test_async_retry_sleep_cancelled_error():
    @retry(max_attempts=3, initial_delay=0.1)
    async def my_func():
        raise ValueError("initial fail")

    with patch("asyncio.sleep", side_effect=asyncio.CancelledError()):
        with pytest.raises(asyncio.CancelledError):
            await my_func()
