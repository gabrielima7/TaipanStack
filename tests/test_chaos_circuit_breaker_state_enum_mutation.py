import pytest

from taipanstack.resilience.circuit_breaker import CircuitBreaker


class CorruptedState:
    """A corrupted state object that crashes on equality check."""

    def __eq__(self, other: object) -> bool:
        """Crash on equality comparison to simulate chaos."""
        raise RuntimeError("Chaos failure on equality comparison")

    def __hash__(self) -> int:
        """Implement hash to satisfy Ruff PLW1641."""
        return 1


def test_chaos_circuit_breaker_state_enum_mutation_fail_safe():
    """Verify CircuitBreaker fails safe when state is mutated to a type that crashes on equality."""
    breaker = CircuitBreaker()

    # Mutate the state to a corrupted object that crashes on ==
    breaker._state.state = CorruptedState()  # type: ignore

    # Due to 'is' checks, this should evaluate gracefully without hitting __eq__
    try:
        result = breaker._should_attempt()
        # The result falls back to False because it's an unrecognized state
        assert result is False
    except RuntimeError:
        pytest.fail("CircuitBreaker crashed due to == comparison instead of using 'is'")
