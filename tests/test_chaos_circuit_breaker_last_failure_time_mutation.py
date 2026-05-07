
from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState


def test_circuit_breaker_survives_last_failure_time_mutation():
    """Simulate type corruption where last_failure_time becomes a string."""
    breaker = CircuitBreaker(failure_threshold=1, timeout=0.01)

    # Force the circuit into OPEN state
    breaker._state.state = CircuitState.OPEN

    # Intentionally mutate the state type
    breaker._state.last_failure_time = "corrupted"  # type: ignore[assignment]

    # Evaluate whether to attempt half-open
    # It should safely degrade to False (deny attempt) and stay OPEN, instead of crashing
    result = breaker._should_attempt()

    assert result is False
    assert breaker.state == CircuitState.OPEN
