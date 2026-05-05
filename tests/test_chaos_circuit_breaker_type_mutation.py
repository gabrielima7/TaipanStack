
from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState


def test_circuit_breaker_survives_type_mutation_failure_metrics():
    """Simulate extreme state corruption where failure_count becomes a string."""
    breaker = CircuitBreaker(failure_threshold=3, timeout=0.01)

    # Intentionally mutate the state type
    breaker._state.failure_count = "2" # type: ignore

    # Trigger a failure
    breaker._record_failure(ValueError("Boom"))

    # It should safely degrade to OPEN state rather than crashing
    assert breaker.state == CircuitState.OPEN


def test_circuit_breaker_survives_type_mutation_half_open_attempt():
    """Simulate type corruption during half-open attempt."""
    breaker = CircuitBreaker(failure_threshold=1, timeout=0.01)

    # Force into half-open
    breaker._state.state = CircuitState.HALF_OPEN
    breaker._state.half_open_attempts = "1" # type: ignore

    # Attempt call
    result = breaker._should_attempt()

    # Should safely fail the attempt evaluation if it encounters TypeError
    assert result is False


def test_circuit_breaker_survives_type_mutation_half_open_success():
    """Simulate type corruption during half-open success."""
    breaker = CircuitBreaker(failure_threshold=1, success_threshold=2, timeout=0.01)

    # Force into half-open
    breaker._state.state = CircuitState.HALF_OPEN
    breaker._state.success_count = "1" # type: ignore

    # Record success
    breaker._record_success()

    # Since success_count is corrupt, it might just reset it, but we mainly check it doesn't crash
    # And state remains HALF_OPEN or CLOSED if it managed to reset and increment
    # It shouldn't raise TypeError
    assert breaker.state in (CircuitState.HALF_OPEN, CircuitState.CLOSED)
