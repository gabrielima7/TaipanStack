import asyncio
import time
from unittest.mock import patch

import pytest

from taipanstack.core.result import Err, Ok, Result
from taipanstack.resilience.adaptive.adaptive_breaker import AdaptiveCircuitBreaker
from taipanstack.resilience.adaptive.orchestrator import ResilienceOrchestrator
from taipanstack.resilience.circuit_breaker import CircuitBreakerError


@pytest.mark.asyncio
async def test_chaos_orchestrator_evaluate_standard_breaker_expected() -> None:
    from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState

    cb = CircuitBreaker(name="test_std_cb", failure_threshold=1, timeout=60.0)
    cb._state.state = CircuitState.OPEN
    cb._state.last_failure_time = time.monotonic()

    orchestrator = ResilienceOrchestrator().with_circuit_breaker(cb)

    async def dummy() -> Result[str, Exception]:
        return Ok("success")

    res = await orchestrator.execute(dummy)
    assert isinstance(res, Err)
    assert isinstance(res.err_value, CircuitBreakerError)
    assert "Circuit 'test_std_cb' is open" in str(res.err_value)


@pytest.mark.asyncio
async def test_chaos_orchestrator_evaluate_adaptive_breaker_expected() -> None:
    from taipanstack.resilience.circuit_breaker import CircuitState

    cb = AdaptiveCircuitBreaker(name="test_adapt_cb", recovery_timeout=60.0)
    cb._state = CircuitState.OPEN
    cb._last_opened_at = time.monotonic()

    orchestrator = ResilienceOrchestrator().with_circuit_breaker(cb)

    async def dummy() -> Result[str, Exception]:
        return Ok("success")

    res = await orchestrator.execute(dummy)
    assert isinstance(res, Err)
    assert isinstance(res.err_value, CircuitBreakerError)
    assert "Circuit 'test_adapt_cb' is open" in str(res.err_value)


@pytest.mark.asyncio
async def test_chaos_orchestrator_bulkhead_edge_expected() -> None:
    from taipanstack.resilience.adaptive.bulkhead import BulkheadFullError

    orchestrator = ResilienceOrchestrator().with_bulkhead(
        max_concurrent=1, max_queue=0, timeout=0.1
    )

    async def slow_endpoint() -> Result[str, Exception]:
        await asyncio.sleep(0.5)
        return Ok("Success")

    tasks = [orchestrator.execute(slow_endpoint) for _ in range(3)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    errors = [
        r
        for r in results
        if isinstance(r, Err) and isinstance(r.err_value, BulkheadFullError)
    ]
    assert len(errors) >= 1


@pytest.mark.asyncio
async def test_chaos_orchestrator_resource_exhaustion_expected() -> None:
    orchestrator = ResilienceOrchestrator().with_bulkhead(
        max_concurrent=1, max_queue=1, timeout=0.1
    )

    async def resource_exhaustion_endpoint() -> Result[str, Exception]:
        raise MemoryError("Out of memory!")

    res = await orchestrator.execute(resource_exhaustion_endpoint)

    assert isinstance(res, Err)
    assert isinstance(res.err_value, MemoryError)


@pytest.mark.asyncio
async def test_chaos_orchestrator_cancellation_expected() -> None:
    orchestrator = ResilienceOrchestrator().with_bulkhead(max_concurrent=5)

    active_calls = 0

    async def slow_endpoint() -> Result[str, Exception]:
        nonlocal active_calls
        active_calls += 1
        try:
            await asyncio.sleep(2.0)
            return Ok("Success")
        finally:
            active_calls -= 1

    task = asyncio.create_task(orchestrator.execute(slow_endpoint))
    await asyncio.sleep(0.1)
    task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await task

    assert active_calls == 0


@pytest.mark.asyncio
async def test_chaos_orchestrator_handle_retry_failure_timeout_expected() -> (
    None
):
    from taipanstack.resilience.adaptive.orchestrator import ResilienceOrchestrator
    from taipanstack.resilience.retry import RetryConfig

    # We want to trigger the specific branch in _handle_retry_failure
    orchestrator = ResilienceOrchestrator().with_retry(
        RetryConfig(max_attempts=3, initial_delay=0.01)
    )

    # Let's mock _calculate_retry_delay to return a huge value so we can hit the `delay` branch logic
    with patch.object(orchestrator, "_calculate_retry_delay", return_value=0.01):

        async def dummy() -> Result[str, Exception]:
            raise ValueError("fail")

        res = await orchestrator.execute(dummy)
        assert isinstance(res, Err)
