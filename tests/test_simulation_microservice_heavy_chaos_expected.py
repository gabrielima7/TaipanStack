import asyncio

import pytest

from taipanstack.core.result import Err, Ok, Result
from taipanstack.resilience.adaptive.adaptive_breaker import AdaptiveCircuitBreaker
from taipanstack.resilience.adaptive.adaptive_retry import AdaptiveRetry
from taipanstack.resilience.adaptive.orchestrator import ResilienceOrchestrator
from taipanstack.security.guards import guard_path_traversal, guard_ssrf
from taipanstack.utils.rate_limit import rate_limit


@pytest.mark.asyncio
async def test_heavy_chaos_expected():
    orchestrator = (
        ResilienceOrchestrator("billing_service")
        .with_bulkhead(max_concurrent=10, max_queue=20, timeout=1.0)
        .with_circuit_breaker(
            AdaptiveCircuitBreaker(
                "billing_cb", target_error_rate=0.1, recovery_timeout=0.1
            )
        )
        .with_retry(AdaptiveRetry(max_attempts=3))
        .with_timeout(1.0)
    )

    @rate_limit(max_calls=500, time_window=1.0)
    async def process_payment(
        url: str, amount: float, path: str
    ) -> Result[str, Exception]:
        res_url = guard_ssrf(url)
        if isinstance(res_url, Err):
            return res_url

        try:
            res_path = guard_path_traversal(path, "/data")
        except Exception as e:
            return Err(e)

        if amount < 0:
            return Err(ValueError("Negative amount"))

        await asyncio.sleep(0.05)

        if amount > 1000:
            # We purposely raise an exception here instead of returning an Err
            raise ConnectionError("DB Timeout")

        return Ok(f"Processed {amount} for {url} via {res_path}")

    async def worker(i: int):
        url = (
            "https://api.stripe.com/charge"
            if i % 2 == 0
            else "http://169.254.169.254/meta"
        )
        path = f"/data/user_{i}.txt" if i % 3 != 0 else "../../../etc/passwd"
        amount = 50.0 if i % 4 != 0 else 1500.0

        # We do NOT catch exceptions here. We let the Orchestrator handle them.
        return await orchestrator.execute(process_payment, url, amount, path)

    tasks = [worker(i) for i in range(200)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    errors = 0
    success = 0
    for r in results:
        # Guarantee orchestrator caught all exceptions and converted them to Err or Ok
        assert isinstance(r, (Ok, Err))
        if isinstance(r, Ok):
            success += 1
        elif isinstance(r, Err):
            errors += 1

    # Ensure actual processing happened
    assert success > 0
    assert errors > 0
    assert success + errors == 200
    assert len(results) == 200
