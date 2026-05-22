"""Chaos tests for circuit breaker type mutation and unexpected enum values."""

from taipanstack.resilience.circuit_breaker import CircuitBreaker


def test_chaos_circuit_breaker_type_mutation_circuit_breaker_type_mutation_success() -> None:
    """Test what happens if the state is an invalid value when _record_success is called."""
    cb = CircuitBreaker()

    # Mutate the state type to an invalid enum to hit the fallthrough branch of match statement
    cb._state.state = "INVALID_STATE"  # type: ignore[assignment]

    # Call _record_success to trigger the match block
    # It should fall through gracefully without crashing
    cb._record_success()


def test_chaos_circuit_breaker_type_mutation_circuit_breaker_type_mutation_failure() -> None:
    """Test what happens if the state is an invalid value when _record_failure is called."""
    cb = CircuitBreaker()

    # Mutate the state type to an invalid enum to hit the fallthrough branch of match statement
    cb._state.state = "INVALID_STATE"  # type: ignore[assignment]

    # Call _record_failure to trigger the match block
    # It should fall through gracefully without crashing
    cb._record_failure(Exception("Test failure"))


def test_chaos_circuit_breaker_type_mutation_circuit_breaker_type_mutation_success_open() -> None:
    """Test what happens if the state is OPEN when _record_success is called."""
    from taipanstack.resilience.circuit_breaker import CircuitState

    cb = CircuitBreaker()

    # Set the state to OPEN to hit the OPEN case in _record_success
    cb._state.state = CircuitState.OPEN

    # Call _record_success to trigger the match block
    # It should hit the OPEN case and fall through gracefully without crashing
    cb._record_success()


def test_chaos_circuit_breaker_type_mutation_circuit_breaker_type_mutation_failure_open() -> None:
    """Test what happens if the state is OPEN when _record_failure is called."""
    from taipanstack.resilience.circuit_breaker import CircuitState

    cb = CircuitBreaker()

    # Set the state to OPEN to hit the OPEN case in _record_failure
    cb._state.state = CircuitState.OPEN

    # Call _record_failure to trigger the match block
    # It should hit the OPEN case and fall through gracefully without crashing
    cb._record_failure(Exception("Test failure"))
