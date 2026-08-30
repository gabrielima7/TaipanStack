import asyncio

import pytest

from taipanstack.core.result import Err, Ok, Result
from taipanstack.resilience.adaptive.adaptive_breaker import AdaptiveCircuitBreaker
from taipanstack.resilience.adaptive.adaptive_retry import AdaptiveRetry
from taipanstack.resilience.adaptive.orchestrator import ResilienceOrchestrator
from taipanstack.resilience.circuit_breaker import CircuitState


@pytest.mark.asyncio
async def test_math_chaos_expected():
    orchestrator = (
        ResilienceOrchestrator("math_chaos")
        .with_bulkhead(max_concurrent=10, max_queue=20, timeout=1.0)
        .with_circuit_breaker(
            AdaptiveCircuitBreaker(
                "math_cb", target_error_rate=0.4, recovery_timeout=0.1
            )
        )
        .with_retry(AdaptiveRetry(max_attempts=1))
        .with_timeout(1.0)
    )

    async def f_x(x: int) -> Result[int, Exception]:
        if x % 2 == 0:
            return Ok(x * 2)
        else:
            raise ValueError("Odd numbers fail")

    tasks = [orchestrator.execute(f_x, i) for i in range(100)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    cb = orchestrator._adaptive_breaker
    if cb is not None:
        # After 100 iterations with 50% failure rate, the error rate exceeds target 0.4.
        # We explicitly assert the circuit breaker transitions correctly out of CLOSED state
        assert cb.state in (CircuitState.OPEN, CircuitState.HALF_OPEN)

    assert len(results) == 100
    for r in results:
        # The orchestrator MUST wrap everything in Result monad
        assert isinstance(r, (Ok, Err))
