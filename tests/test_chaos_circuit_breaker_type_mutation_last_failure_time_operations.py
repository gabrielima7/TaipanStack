from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState


def test_circuit_breaker_last_failure_time_mutation():
    breaker = CircuitBreaker()
    breaker._state.state = CircuitState.OPEN
    breaker._state.last_failure_time = "corrupted_time" # type: ignore[assignment]

    # Should safely fail closed/not open instead of crashing
    assert not breaker._should_attempt()
