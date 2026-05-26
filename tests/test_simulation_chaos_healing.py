import asyncio

import pytest

from taipanstack.core.result import Err, Ok, Result
from taipanstack.resilience.adaptive.adaptive_breaker import AdaptiveCircuitBreaker
from taipanstack.resilience.adaptive.adaptive_retry import AdaptiveRetry
from taipanstack.resilience.adaptive.orchestrator import ResilienceOrchestrator
from taipanstack.security.guards import guard_ssrf
from taipanstack.utils.rate_limit import rate_limit


@pytest.mark.asyncio
async def test_complex_microservice_simulation_chaos() -> None:
    """Simulates a highly concurrent microservice handling malicious payloads."""
    # 1. Setup Architecture
    orchestrator = (
        ResilienceOrchestrator()
        .with_bulkhead(max_concurrent=5, max_queue=10, timeout=1.0)
        .with_circuit_breaker(AdaptiveCircuitBreaker(recovery_timeout=0.1))
        .with_retry(AdaptiveRetry(max_attempts=3))
        .with_timeout(2.0)
    )

    @rate_limit(max_calls=100, time_window=1.0)
    async def simulated_endpoint(url: str, payload: dict) -> Result[str, Exception]:
        # Validate Security
        sec_res = guard_ssrf(url)
        if isinstance(sec_res, Err):
            return sec_res  # Return SecurityError as Err

        # Simulated workload (Flaky and slow)
        await asyncio.sleep(0.01)
        if "fail" in payload:
            return Err(RuntimeError("Database exploded"))
        if "timeout" in payload:
            await asyncio.sleep(3.0)
        return Ok(f"Processed {url}")

    # 2. Audit and Chaos (Fuzzing / Thundering Herd)
    async def attacker_task(i: int) -> Result[str, Exception]:
        url = (
            "http://169.254.169.254/latest/meta-data/"
            if i % 2 == 0
            else "https://api.example.com/data"
        )
        payload = (
            {"fail": True}
            if i % 3 == 0
            else {"timeout": True}
            if i % 5 == 0
            else {"ok": True}
        )

        # Execute through orchestrator
        res = await orchestrator.execute(simulated_endpoint, url, payload)
        return res

    tasks = [attacker_task(i) for i in range(50)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # We expect failures (RuntimeErrors, SecurityErrors, BulkheadFullError, etc.)
    # The key is that the system doesn't deadlock, memory leak, or return unhandled exceptions out of the Result monad.
    for r in results:
        assert isinstance(r, (Ok, Err)), f"Outcome {r} must be wrapped in Result monad"


@pytest.mark.asyncio
async def test_complex_microservice_simulation_orchestrator_exception() -> None:
    """Tests the new except Exception branch wrapping _execute_inner."""
    orchestrator_with_bh = ResilienceOrchestrator().with_bulkhead(max_concurrent=5)
    orchestrator_without_bh = ResilienceOrchestrator()

    async def exploding_endpoint() -> Result[str, Exception]:
        raise ValueError("Critical simulated explosion")

    # With bulkhead
    res_bh = await orchestrator_with_bh.execute(exploding_endpoint)
    assert isinstance(res_bh, Err)
    assert isinstance(res_bh.err_value, ValueError)
    assert str(res_bh.err_value) == "Critical simulated explosion"

    # Without bulkhead
    res_no_bh = await orchestrator_without_bh.execute(exploding_endpoint)
    assert isinstance(res_no_bh, Err)
    assert isinstance(res_no_bh.err_value, ValueError)
    assert str(res_no_bh.err_value) == "Critical simulated explosion"


@pytest.mark.asyncio
async def test_complex_microservice_simulation_orchestrator_exception_coverage() -> (
    None
):
    """Coverage to hit the except Exception logic inside orchestrator execute().
    We mock _execute_inner to guarantee it raises synchronously.
    """
    import unittest.mock

    orchestrator_with_bh = ResilienceOrchestrator().with_bulkhead(max_concurrent=5)
    orchestrator_without_bh = ResilienceOrchestrator()

    async def dummy_endpoint() -> Result[str, Exception]:
        return Ok("dummy")

    with unittest.mock.patch.object(
        ResilienceOrchestrator,
        "_execute_inner",
        side_effect=RuntimeError("Mock Sync Failure"),
    ):
        res_bh = await orchestrator_with_bh.execute(dummy_endpoint)
        assert isinstance(res_bh, Err)
        assert isinstance(res_bh.err_value, RuntimeError)

        res_no_bh = await orchestrator_without_bh.execute(dummy_endpoint)
        assert isinstance(res_no_bh, Err)
        assert isinstance(res_no_bh.err_value, RuntimeError)
