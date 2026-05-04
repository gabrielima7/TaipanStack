from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState


def test_circuit_breaker_chaos_type_mutation():
    """Chaos test: simulate type mutation of internal failure count."""
    breaker = CircuitBreaker(failure_threshold=3, timeout=10.0)

    # Force a failure to ensure state is initialized
    try:
        raise ValueError("failure")
    except ValueError as e:
        breaker._record_failure(e)

    assert breaker._state.failure_count == 1
    assert breaker._state.state == CircuitState.CLOSED

    # Chaos: Mutate failure_count to a completely different type (e.g. list, string)
    breaker._state.failure_count = "corrupted_string"

    # Should not crash on subsequent failures, but safely reject or reset
    try:
        raise ValueError("second failure")
    except ValueError as e:
        # Before refactoring this will crash with TypeError: >= not supported between instances of 'str' and 'int'
        breaker._record_failure(e)

    # The system should open the circuit if corrupted, or reset.
    assert breaker._state.state == CircuitState.OPEN
