from unittest.mock import patch

import pytest

from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitBreakerError


def test_circuit_breaker_chaos_mock_time():
    breaker = CircuitBreaker(failure_threshold=2, timeout=0.1)

    @breaker
    def failing_call():
        raise ValueError("failure")

    with pytest.raises(ValueError):
        failing_call()

    with pytest.raises(ValueError):
        failing_call()

    # Breaker is now open
    with pytest.raises(CircuitBreakerError):
        failing_call()

    # Now chaos: we make time.monotonic() return an invalid type (string)
    # The circuit breaker handles time elapsed checks.
    with patch("time.monotonic", return_value="invalid_time"):
        with pytest.raises(CircuitBreakerError):
            failing_call()


def test_circuit_breaker_chaos_time_jump():
    breaker = CircuitBreaker(failure_threshold=1, timeout=10.0)

    @breaker
    def failing_call():
        raise ValueError("failure")

    with pytest.raises(ValueError):
        failing_call()

    # Breaker is open.
    with pytest.raises(CircuitBreakerError):
        failing_call()

    # Simulate massive time jump
    with patch("time.monotonic", return_value=1e10):
        # State should move to half open and we should be able to call it
        with pytest.raises(ValueError):
            failing_call()
