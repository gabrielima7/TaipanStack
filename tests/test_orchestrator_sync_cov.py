import pytest

from taipanstack.core.result import Ok
from taipanstack.resilience.adaptive.orchestrator import ResilienceOrchestrator


@pytest.mark.asyncio
async def test_orchestrator_sync_fn_timeout():
    orch = ResilienceOrchestrator("test_sync").with_timeout(10.0)

    def sync_fn():
        return Ok("sync_success")

    res = await orch.execute(sync_fn)
    assert res == Ok("sync_success")


@pytest.mark.asyncio
async def test_orchestrator_sync_fn_timeout_none():
    orch = ResilienceOrchestrator("test_sync")

    def sync_fn():
        return Ok("sync_success")

    res = await orch.execute(sync_fn)
    assert res == Ok("sync_success")
