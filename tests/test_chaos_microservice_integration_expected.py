import asyncio
from typing import Any

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from taipanstack.core.result import Err, Ok, Result
from taipanstack.resilience.adaptive.adaptive_breaker import AdaptiveCircuitBreaker
from taipanstack.resilience.adaptive.adaptive_retry import AdaptiveRetry
from taipanstack.resilience.adaptive.orchestrator import ResilienceOrchestrator
from taipanstack.security.guards import guard_path_traversal, guard_ssrf
from taipanstack.utils.rate_limit import rate_limit

orchestrator = (
    ResilienceOrchestrator()
    .with_bulkhead(max_concurrent=10, max_queue=20, timeout=1.0)
    .with_circuit_breaker(AdaptiveCircuitBreaker(recovery_timeout=0.1))
    .with_retry(AdaptiveRetry(max_attempts=3))
    .with_timeout(1.0)
)


@rate_limit(max_calls=1000, time_window=1.0)
async def process_user_request(
    url: str, filepath: str, payload: dict[str, Any]
) -> Result[str, Exception]:
    url_res = guard_ssrf(url)
    if isinstance(url_res, Err):
        return url_res  # type: ignore[return-value]

    path_res = guard_path_traversal(filepath, "/safe/dir")
    if isinstance(path_res, Err):
        return path_res  # type: ignore[return-value]

    await asyncio.sleep(0.01)

    if payload.get("crash"):
        return Err(RuntimeError("Simulated crash"))

    if payload.get("hang"):
        await asyncio.sleep(2.0)

    return Ok(f"Processed {url} and {filepath}")


@pytest.mark.asyncio
async def test_chaos_microservice_integration_high_concurrency_chaos_integration() -> (
    None
):
    urls = [
        "https://api.example.com",
        "http://169.254.169.254/latest/meta-data/",
        "http://localhost:8080",
        "file:///etc/passwd",
    ]
    paths = [
        "image.png",
        "../../../etc/passwd",
        "/safe/dir/data.txt",
        "/safe/dir/../../bin/sh",
    ]
    payloads = [
        {"ok": True},
        {"crash": True},
        {"hang": True},
    ]

    async def attacker(i: int) -> Result[str, Exception]:
        url = urls[i % len(urls)]
        path = paths[i % len(paths)]
        payload = payloads[i % len(payloads)]
        return await orchestrator.execute(process_user_request, url, path, payload)

    tasks = [attacker(i) for i in range(150)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for r in results:
        assert isinstance(r, (Ok, Err))


@given(
    url=st.text(max_size=1000),
    filepath=st.text(max_size=1000),
    crash=st.booleans(),
    hang=st.booleans(),
)
@settings(max_examples=50, deadline=None)
@pytest.mark.asyncio
async def test_chaos_microservice_integration_property_based_chaos_endpoint(
    url: str, filepath: str, crash: bool, hang: bool
) -> None:
    payload = {"crash": crash, "hang": hang}
    res = await orchestrator.execute(process_user_request, url, filepath, payload)
    assert isinstance(res, (Ok, Err))
