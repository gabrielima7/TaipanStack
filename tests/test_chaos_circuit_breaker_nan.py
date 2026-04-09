import math
import time

import pytest

from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
    CircuitState,
)


def test_circuit_breaker_chaos_timeout_nan():
    """Simulate a chaos scenario where the timeout becomes NaN."""
    # We create a circuit breaker with a NaN timeout. This could happen
    # due to config corruption, missing env vars parsed as float('nan'), etc.
    breaker = CircuitBreaker(failure_threshold=1, success_threshold=1, timeout=math.nan)

    @breaker
    def failing_service():
        raise RuntimeError("Service failure")

    @breaker
    def successful_service():
        return "success"

    # Trip the circuit (CLOSED -> OPEN)
    with pytest.raises(RuntimeError, match="Service failure"):
        failing_service()

    assert breaker.state == CircuitState.OPEN

    # Fast forward time to simulate a long wait (1000 seconds)
    breaker._state.last_failure_time = time.monotonic() - 1000.0

    # If vulnerable to NaN, `elapsed >= math.nan` is False, so it's stuck OPEN forever.
    try:
        successful_service()
    except CircuitBreakerError as e:
        pytest.fail(f"Circuit breaker permanently stuck OPEN due to NaN timeout: {e}")

    assert breaker.state == CircuitState.CLOSED
