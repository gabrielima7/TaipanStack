from unittest.mock import patch

import pytest

from taipanstack.core.result import Err
from taipanstack.resilience.adaptive.orchestrator import ResilienceOrchestrator


@pytest.mark.asyncio
async def test_chaos_orchestrator_resource_exhaustion_orchestrator_bulkhead_oserror_chaos_returns_err() -> None:
    """Chaos test: Inject OSError when acquiring semaphore in Orchestrator."""

    orchestrator: ResilienceOrchestrator[str] = ResilienceOrchestrator(
        "test_orch"
    ).with_bulkhead(max_concurrent=1, max_queue=1)

    async def dummy_task() -> str:
        return "success"

    with patch("asyncio.Semaphore.acquire", side_effect=OSError("Too many open files")):
        result = await orchestrator.execute(dummy_task)
        assert isinstance(result, Err)
        assert isinstance(result.unwrap_err(), RuntimeError)
        assert "Resource exhaustion" in str(result.unwrap_err())
        assert "Too many open files" in str(result.unwrap_err())


@pytest.mark.asyncio
async def test_chaos_orchestrator_resource_exhaustion_orchestrator_bulkhead_memoryerror_chaos_returns_err() -> None:
    """Chaos test: Inject MemoryError when acquiring semaphore in Orchestrator."""

    orchestrator: ResilienceOrchestrator[str] = ResilienceOrchestrator(
        "test_orch"
    ).with_bulkhead(max_concurrent=1, max_queue=1)

    async def dummy_task() -> str:
        return "success"

    with patch("asyncio.Semaphore.acquire", side_effect=MemoryError("Out of memory")):
        result = await orchestrator.execute(dummy_task)
        assert isinstance(result, Err)
        assert isinstance(result.unwrap_err(), RuntimeError)
        assert "Resource exhaustion" in str(result.unwrap_err())
        assert "Out of memory" in str(result.unwrap_err())


@pytest.mark.asyncio
async def test_chaos_orchestrator_resource_exhaustion_orchestrator_bulkhead_runtimeerror_chaos_returns_err() -> None:
    """Chaos test: Inject RuntimeError when acquiring semaphore in Orchestrator."""

    orchestrator: ResilienceOrchestrator[str] = ResilienceOrchestrator(
        "test_orch"
    ).with_bulkhead(max_concurrent=1, max_queue=1)

    async def dummy_task() -> str:
        return "success"

    with patch(
        "asyncio.Semaphore.acquire", side_effect=RuntimeError("Event loop closed")
    ):
        result = await orchestrator.execute(dummy_task)
        assert isinstance(result, Err)
        assert isinstance(result.unwrap_err(), RuntimeError)
        assert "Resource exhaustion" in str(result.unwrap_err())
        assert "Event loop closed" in str(result.unwrap_err())
