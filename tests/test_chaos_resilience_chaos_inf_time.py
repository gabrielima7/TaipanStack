from unittest.mock import patch

import pytest

from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitBreakerError


def test_circuit_breaker_chaos_time_jump_massive():
    breaker = CircuitBreaker(failure_threshold=1, timeout=10.0)

    @breaker
    def failing_call():
        raise ValueError("failure")

    with pytest.raises(ValueError):
        failing_call()

    with pytest.raises(CircuitBreakerError):
        failing_call()

    # Simulate massive time jump that produces math.inf
    # By changing circuit breaker to degrade safely on math.inf,
    # it treats it as timeout elapsed.
    with patch("time.monotonic", return_value=float("inf")):
        with pytest.raises(ValueError):
            failing_call()
