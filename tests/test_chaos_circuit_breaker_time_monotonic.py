import time
from unittest import mock

from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState


def test_circuit_breaker_time_monotonic_exception_update_metrics():
    # Setup
    breaker = CircuitBreaker(failure_threshold=5)
    breaker._state.state = CircuitState.CLOSED
    breaker._state.failure_count = 4

    # Execution
    with mock.patch("time.monotonic", side_effect=RuntimeError("System error")):
        # Should gracefully fail or just not update last_failure_time, but NOT crash
        breaker._update_failure_metrics()

    # Assert
    assert breaker._state.failure_count == 5


def test_circuit_breaker_time_monotonic_exception_handle_open():
    # Setup
    breaker = CircuitBreaker(timeout=1.0)
    breaker._state.state = CircuitState.OPEN
    breaker._state.last_failure_time = time.monotonic() - 10.0

    # Execution
    with mock.patch("time.monotonic", side_effect=RuntimeError("System error")):
        should_attempt, state_change = breaker._handle_open_state()

    # Assert
    assert should_attempt is False
    assert state_change is None
