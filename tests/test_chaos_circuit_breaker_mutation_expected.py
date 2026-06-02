from dataclasses import FrozenInstanceError

import pytest

from taipanstack.resilience.circuit_breaker import CircuitBreaker


def test_chaos_circuit_breaker_mutation_chaos_circuit_breaker_config_mutation_prevented_operations_expected():
    """Chaos test: Attempt to mutate config at runtime. Must be blocked by frozen dataclass."""
    breaker = CircuitBreaker()

    with pytest.raises(FrozenInstanceError):
        breaker.config.timeout = float("nan")
