"""Chaos tests for circuit breaker type mutation half open attempt count."""


import pytest
from src.taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState


def test_circuit_breaker_half_open_attempts_mutation_decrement() -> None:
    """Test safe degradation when half_open_attempts is corrupted."""
    cb = CircuitBreaker()
    cb._state.state = CircuitState.HALF_OPEN

    # Mutate half_open_attempts to string
    cb._state.half_open_attempts = "1" # type: ignore[assignment]

    try:
        cb._decrement_half_open(True)
    except TypeError:
        pytest.fail("Decrement failed due to TypeError")

    assert cb._state.half_open_attempts == 0
