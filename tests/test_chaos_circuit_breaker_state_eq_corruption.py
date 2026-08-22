from taipanstack.resilience.circuit_breaker import CircuitBreaker


def test_chaos_circuit_breaker_type_mutation_success_corrupted_state_eq():
    cb = CircuitBreaker()

    class InvalidState:
        def __eq__(self, other):
            raise TypeError("Equality corrupted")

        def __hash__(self):
            return 1

    cb._state.state = InvalidState()  # type: ignore[assignment]
    # Should not raise exception
    cb._get_success_state_change()


def test_chaos_circuit_breaker_type_mutation_failure_corrupted_state_eq():
    cb = CircuitBreaker()

    class InvalidState:
        def __eq__(self, other):
            raise TypeError("Equality corrupted")

        def __hash__(self):
            return 1

    cb._state.state = InvalidState()  # type: ignore[assignment]
    # Should not raise exception
    cb._get_failure_state_change()
