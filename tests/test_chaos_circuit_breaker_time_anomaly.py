import math
from unittest.mock import patch
import pytest

from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState


def test_circuit_breaker_time_anomaly_negative_elapsed():
    """Chaos test: time.monotonic() returns an earlier time than last_failure_time.
    This simulates a clock jump backwards or negative elapsed time anomaly.
    """
    breaker = CircuitBreaker(failure_threshold=1, timeout=10.0)

    # Open the circuit
    breaker._record_failure(Exception("test failure"))
    assert breaker.state == CircuitState.OPEN

    # Simulate a negative elapsed time (e.g. time jumping backwards)
    breaker._state.last_failure_time = 100.0
    with patch("time.monotonic", return_value=90.0):
        # elapsed would be 90.0 - 100.0 = -10.0
        # If not clamped to >= 0, and if we were doing weird math, it might cause issues.
        # It definitely shouldn't transition to HALF_OPEN (timeout is 10.0).
        # We also want to verify it doesn't crash or behave unexpectedly.
        result = breaker._should_attempt()
        assert result is False
        assert breaker.state == CircuitState.OPEN


def test_circuit_breaker_time_anomaly_nan_elapsed():
    """Chaos test: time.monotonic() results in NaN elapsed time.
    This simulates extreme time manipulation or mocked anomalies.
    """
    breaker = CircuitBreaker(failure_threshold=1, timeout=10.0)

    breaker._record_failure(Exception("test failure"))
    assert breaker.state == CircuitState.OPEN

    breaker._state.last_failure_time = 100.0
    with patch("time.monotonic", return_value=float("nan")):
        # elapsed would be NaN.
        # math.isfinite(NaN) is False.
        # elapsed >= timeout where elapsed is NaN evaluates to False,
        # but if the result is NaN, logging might format it weirdly or it might cause float issues.
        result = breaker._should_attempt()
        assert result is False
        assert breaker.state == CircuitState.OPEN


def test_circuit_breaker_time_anomaly_inf_elapsed():
    """Chaos test: time.monotonic() results in INF elapsed time.
    This simulates extreme time manipulation or mocked anomalies.
    """
    breaker = CircuitBreaker(failure_threshold=1, timeout=10.0)

    breaker._record_failure(Exception("test failure"))
    assert breaker.state == CircuitState.OPEN

    breaker._state.last_failure_time = 100.0
    with patch("time.monotonic", return_value=float("inf")):
        # elapsed would be INF.
        # INF >= 10.0 is True.
        # But if we want to guard against INF, it should not transition, or it should clamp.
        # The prompt suggests checking math.isfinite. If not finite, default to 0.0,
        # so it won't transition to HALF_OPEN.
        result = breaker._should_attempt()
        assert result is False
        assert breaker.state == CircuitState.OPEN
