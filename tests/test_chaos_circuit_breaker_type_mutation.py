"""Chaos tests for circuit breaker type mutation and unexpected enum values."""

from src.taipanstack.resilience.circuit_breaker import CircuitBreaker


def test_circuit_breaker_type_mutation_success() -> None:
    """Test what happens if the state is an invalid value when _record_success is called."""
    cb = CircuitBreaker()

    # Mutate the state type to an invalid enum to hit the fallthrough branch of match statement
    cb._state.state = "INVALID_STATE"  # type: ignore[assignment]

    # Call _record_success to trigger the match block
    # It should fall through gracefully without crashing
    cb._record_success()

def test_circuit_breaker_type_mutation_failure() -> None:
    """Test what happens if the state is an invalid value when _record_failure is called."""
    cb = CircuitBreaker()

    # Mutate the state type to an invalid enum to hit the fallthrough branch of match statement
    cb._state.state = "INVALID_STATE"  # type: ignore[assignment]

    # Call _record_failure to trigger the match block
    # It should fall through gracefully without crashing
    cb._record_failure(Exception("Test failure"))
