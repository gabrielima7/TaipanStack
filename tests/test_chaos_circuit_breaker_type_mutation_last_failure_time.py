from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState


def test_chaos_circuit_breaker_type_mutation_last_failure_time_circuit_breaker_last_failure_time_mutation():
    breaker = CircuitBreaker()
    breaker._state.state = CircuitState.OPEN
    breaker._state.last_failure_time = "corrupted_time"  # type: ignore[assignment]

    # Should safely fail closed/not open instead of crashing
    assert not breaker._should_attempt()


def test_chaos_circuit_breaker_nan_last_failure_time_allows_recovery():
    breaker = CircuitBreaker(timeout=0.01)
    breaker._state.state = CircuitState.OPEN
    breaker._state.last_failure_time = float("nan")

    # Should gracefully allow recovery/attempt after timeout instead of permanent lockout
    assert breaker._should_attempt()
    assert breaker._state.state == CircuitState.HALF_OPEN
