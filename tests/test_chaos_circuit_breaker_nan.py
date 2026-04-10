import math
from unittest.mock import patch

import pytest

from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitState,
)


def test_circuit_breaker_chaos_time_corruption_nan():
    breaker = CircuitBreaker(failure_threshold=1, timeout=0.1)

    @breaker
    def failing_service():
        raise ValueError("Simulated failure")

    # Simulate a failure while time is corrupted
    # _record_failure will be called with monotonic returning NaN
    with patch("time.monotonic", return_value=math.nan):
        with pytest.raises(ValueError, match="Simulated failure"):
            failing_service()

    # Circuit should be OPEN
    assert breaker.state == CircuitState.OPEN

    # Fast forward time to allow timeout to expire
    with patch("time.monotonic", return_value=100.0):
        # Because the previous last_failure_time might be NaN, elapsed time
        # calculated as 100.0 - NaN will result in NaN, and NaN >= 0.1 is False.
        # This locks the circuit breaker permanently in OPEN state if unhandled.
        # But with hardening, the circuit should evaluate it as safe to attempt.
        with pytest.raises(ValueError, match="Simulated failure"):
            failing_service()

    # It transitioned to HALF_OPEN, tried, and failed, so it returned to OPEN
    assert breaker.state == CircuitState.OPEN


def test_circuit_breaker_chaos_time_corruption_nan_current():
    breaker = CircuitBreaker(failure_threshold=1, timeout=0.1)

    @breaker
    def failing_service():
        raise ValueError("Simulated failure")

    # Normal failure
    with pytest.raises(ValueError, match="Simulated failure"):
        failing_service()

    assert breaker.state == CircuitState.OPEN

    # current time becomes NaN
    with patch("time.monotonic", return_value=math.nan):
        # Should attempt to break out of OPEN state
        with pytest.raises(ValueError, match="Simulated failure"):
            failing_service()

    assert breaker.state == CircuitState.OPEN
