import asyncio
import threading

import pytest

from taipanstack.core.result import Err, Ok, Result
from taipanstack.resilience.resilience import timeout


def test_chaos_resilience_exhaustion_chaos_resilience_timeout_thread_exhaustion_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    @timeout(1.0)
    def dummy_func() -> Result[str, Exception]:
        return Ok("success")

    def mock_start(*args, **kwargs):
        raise RuntimeError("Thread limit reached")

    monkeypatch.setattr(threading.Thread, "start", mock_start)

    result = dummy_func()
    assert isinstance(result, Err)
    assert isinstance(result.err_value, RuntimeError)
    assert "Thread exhaustion:" in str(result.err_value)


def test_chaos_resilience_exhaustion_chaos_resilience_timeout_thread_exhaustion_memory_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    @timeout(1.0)
    def dummy_func() -> Result[str, Exception]:
        return Ok("success")

    def mock_start(*args, **kwargs):
        raise MemoryError("Out of memory")

    monkeypatch.setattr(threading.Thread, "start", mock_start)

    result = dummy_func()
    assert isinstance(result, Err)
    assert isinstance(result.err_value, RuntimeError)
    assert "Memory exhaustion:" in str(result.err_value)


def test_chaos_resilience_exhaustion_chaos_resilience_timeout_thread_exhaustion_os_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    @timeout(1.0)
    def dummy_func() -> Result[str, Exception]:
        return Ok("success")

    def mock_start(*args, **kwargs):
        raise OSError("Too many files")

    monkeypatch.setattr(threading.Thread, "start", mock_start)

    result = dummy_func()
    assert isinstance(result, Err)
    assert isinstance(result.err_value, RuntimeError)
    assert "Resource exhaustion:" in str(result.err_value)


@pytest.mark.asyncio
async def test_chaos_resilience_timeout_async_exhaustion_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    @timeout(1.0)
    async def dummy_func() -> Result[str, Exception]:
        return Ok("success")

    async def mock_wait_for(*args, **kwargs):
        # Explicitly close the coroutine to avoid RuntimeWarning: coroutine was never awaited
        if args and hasattr(args[0], "close"):
            args[0].close()
        raise RuntimeError("Task exhaustion")

    monkeypatch.setattr(asyncio, "wait_for", mock_wait_for)

    result = await dummy_func()
    assert isinstance(result, Err)
    assert isinstance(result.err_value, RuntimeError)
    assert "Task exhaustion:" in str(result.err_value)


@pytest.mark.asyncio
async def test_chaos_resilience_timeout_async_exhaustion_memory_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    @timeout(1.0)
    async def dummy_func() -> Result[str, Exception]:
        return Ok("success")

    async def mock_wait_for(*args, **kwargs):
        if args and hasattr(args[0], "close"):
            args[0].close()
        raise MemoryError("Memory exhaustion")

    monkeypatch.setattr(asyncio, "wait_for", mock_wait_for)

    result = await dummy_func()
    assert isinstance(result, Err)
    assert isinstance(result.err_value, RuntimeError)
    assert "Memory exhaustion:" in str(result.err_value)


@pytest.mark.asyncio
async def test_chaos_resilience_timeout_async_exhaustion_os_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    @timeout(1.0)
    async def dummy_func() -> Result[str, Exception]:
        return Ok("success")

    async def mock_wait_for(*args, **kwargs):
        if args and hasattr(args[0], "close"):
            args[0].close()
        raise OSError("Resource exhaustion")

    monkeypatch.setattr(asyncio, "wait_for", mock_wait_for)

    result = await dummy_func()
    assert isinstance(result, Err)
    assert isinstance(result.err_value, RuntimeError)
    assert "Resource exhaustion:" in str(result.err_value)
