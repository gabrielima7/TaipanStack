import math

import pytest

from taipanstack.resilience.adaptive.adaptive_breaker import AdaptiveCircuitBreaker
from taipanstack.resilience.circuit_breaker import CircuitState


def test_coverage_adaptive_breaker_adaptive_breaker_reset_and_should_allow():
    breaker = AdaptiveCircuitBreaker(min_throughput=1, target_error_rate=0.0)
    assert breaker.should_allow() is True

    breaker.record_failure(ValueError("fail"))
    assert breaker.should_allow() is False

    breaker.reset()
    assert breaker.should_allow() is True
    assert breaker.metrics.total_calls == 0


def test_coverage_adaptive_breaker_adaptive_breaker_invalid_recovery_timeout():
    with pytest.raises(
        ValueError, match="recovery_timeout must be a finite non-negative number"
    ):
        AdaptiveCircuitBreaker(recovery_timeout=-1.0)

    with pytest.raises(
        ValueError, match="recovery_timeout must be a finite non-negative number"
    ):
        AdaptiveCircuitBreaker(recovery_timeout=math.nan)


def test_coverage_adaptive_breaker_adaptive_breaker_evaluate_trip_returns_early():
    breaker = AdaptiveCircuitBreaker(min_throughput=5, recovery_timeout=30.0)

    # Force state to something other than CLOSED
    breaker._state = CircuitState.OPEN
    import time

    breaker._last_opened_at = time.monotonic()  # avoid timeout to half open
    breaker._evaluate_trip()
    assert breaker._state == CircuitState.OPEN  # No change

    breaker._state = CircuitState.CLOSED
    # Less than min_throughput (bypassing record_failure which calls it)
    breaker._evaluate_trip()
    assert breaker._state == CircuitState.CLOSED


def test_coverage_adaptive_breaker_adaptive_breaker_half_open_success_and_failure(
    monkeypatch,
):
    breaker = AdaptiveCircuitBreaker(recovery_timeout=0.0)
    breaker._state = CircuitState.OPEN
    breaker._last_opened_at = 0.0  # Force immediate recovery

    # Transition to half open
    assert breaker.state == CircuitState.HALF_OPEN

    # Success in half open
    import time

    monkeypatch.setattr(time, "monotonic", lambda: 100.0)
    breaker.record_success()
    assert breaker.state == CircuitState.CLOSED
    assert len(breaker._window) == 1

    # Force open again
    breaker._state = CircuitState.OPEN
    breaker._last_opened_at = 0.0
    assert breaker.state == CircuitState.HALF_OPEN

    # Failure in half open
    monkeypatch.setattr(time, "monotonic", lambda: 100.0)
    breaker = AdaptiveCircuitBreaker(recovery_timeout=30.0)
    breaker._state = CircuitState.HALF_OPEN
    breaker.record_failure(ValueError("fail"))
    assert breaker._state == CircuitState.OPEN


def test_coverage_adaptive_breaker_adaptive_breaker_evaluate_trip_with_half_open(
    monkeypatch,
):
    breaker = AdaptiveCircuitBreaker(recovery_timeout=0.0)
    breaker._state = CircuitState.OPEN
    breaker._last_opened_at = 0.0

    # State is now HALF_OPEN due to property
    assert breaker.state == CircuitState.HALF_OPEN

    # Test record_success from HALF_OPEN to cover lines 169-171
    # We monkeypatch time.monotonic to ensure no weird state changes
    import time

    monkeypatch.setattr(time, "monotonic", lambda: 100.0)

    breaker.record_success()
    assert breaker.state == CircuitState.CLOSED


def test_coverage_adaptive_breaker_adaptive_breaker_evaluate_trip_failure_with_half_open(
    monkeypatch,
):
    breaker = AdaptiveCircuitBreaker(recovery_timeout=30.0)
    breaker._state = CircuitState.HALF_OPEN

    assert breaker.state == CircuitState.HALF_OPEN

    # Test record_failure from HALF_OPEN to cover lines 189-191
    import time

    monkeypatch.setattr(time, "monotonic", lambda: 100.0)
    breaker.record_failure(ValueError("test"))
    assert breaker.state == CircuitState.OPEN


def test_coverage_adaptive_breaker_adaptive_breaker_evaluate_trip_with_min_throughput():
    breaker = AdaptiveCircuitBreaker(min_throughput=2, target_error_rate=0.5)

    # 1 error, less than min_throughput (2)
    breaker.record_failure(ValueError("test"))
    assert breaker.state == CircuitState.CLOSED

    # 2 errors, now hits min_throughput and error_rate > target (2/2 = 1.0 > 0.5)
    breaker.record_failure(ValueError("test2"))
    assert breaker.state == CircuitState.OPEN


def test_coverage_adaptive_breaker_adaptive_breaker_evaluate_trip_with_min_throughput_and_target_rate():
    # specifically test when target_rate is negative for coverage line 161
    breaker = AdaptiveCircuitBreaker(min_throughput=1, target_error_rate=-1.0)

    # Negative target rate means it fails closed immediately upon error
    # (since error_rate 1.0 > target -1.0)
    breaker.record_failure(ValueError("test"))
    assert breaker.state == CircuitState.OPEN


def test_coverage_adaptive_breaker_adaptive_breaker_invalid_recovery_timeout_type():
    with pytest.raises(
        TypeError, match="recovery_timeout must be a finite non-negative number"
    ):
        AdaptiveCircuitBreaker(recovery_timeout="30.0")  # type: ignore


def test_coverage_adaptive_breaker_adaptive_breaker_invalid_recovery_timeout_type_mock_finite():
    # If the check for isinstance is hit, we cover line 95
    """Tests invalid recovery timeout mocking finite check logic."""
    with pytest.raises(
        TypeError, match="recovery_timeout must be a finite non-negative number"
    ):
        AdaptiveCircuitBreaker(recovery_timeout="30.0")  # type: ignore


def test_coverage_adaptive_breaker_adaptive_breaker_min_throughput_type_error():
    # Cover the ValueError in _validate_min_throughput for invalid values like 0
    with pytest.raises(ValueError, match="min_throughput must be at least 1"):
        AdaptiveCircuitBreaker(min_throughput=0)
