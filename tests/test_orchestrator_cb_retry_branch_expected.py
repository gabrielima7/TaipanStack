import pytest

from taipanstack.core.result import Err, safe
from taipanstack.resilience.adaptive import (
    AdaptiveCircuitBreaker,
    ResilienceOrchestrator,
)
from taipanstack.resilience.circuit_breaker import CircuitBreakerError
from taipanstack.resilience.retry import RetryConfig


@pytest.mark.asyncio
async def test_orchestrator_cb_retry_branch_orchestrator_circuit_breaker_trips_during_retry():
    orch = (
        ResilienceOrchestrator("test_orch")
        .with_circuit_breaker(
            AdaptiveCircuitBreaker(
                "test_cb", target_error_rate=0.0, min_throughput=1, window_size=5
            )
        )
        .with_retry(RetryConfig(max_attempts=3, initial_delay=0.0))
    )

    attempts = 0

    @safe
    async def failing_func():
        nonlocal attempts
        attempts += 1
        raise ValueError("failed")

    result = await orch.execute(failing_func)

    assert isinstance(result, Err)
    # the first attempt throws ValueError. The CB records the failure.
    # min_throughput is 1, window size 5, error rate is 1.0 > 0.0.
    # Circuit Breaker OPENS.
    # attempt 2 will evaluate the CB and see it's OPEN.
    # It will break the retry loop and return the CB error.
    assert isinstance(result.err_value, CircuitBreakerError)
    assert attempts == 1
