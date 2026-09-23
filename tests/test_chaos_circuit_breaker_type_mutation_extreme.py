"""Tests simulating extreme type mutations in CircuitBreakerConfig using hypothesis."""

import hypothesis.strategies as st
import pytest
from hypothesis import HealthCheck, given, settings

from taipanstack.resilience.circuit_breaker import CircuitBreakerConfig


@settings(
    max_examples=100,
    suppress_health_check=[HealthCheck.too_slow],
    deadline=None,
)
@given(
    st.one_of(
        st.text(),
        st.booleans(),
        st.dictionaries(st.text(), st.text()),
        st.lists(st.text()),
    )
)
def test_circuit_breaker_config_extreme_type_mutation_failure_threshold(
    mutated_val: object,
) -> None:
    """Simulate extreme type mutations for failure_threshold."""
    with pytest.raises((ValueError, TypeError)):
        CircuitBreakerConfig(failure_threshold=mutated_val)  # type: ignore


@settings(
    max_examples=100,
    suppress_health_check=[HealthCheck.too_slow],
    deadline=None,
)
@given(
    st.one_of(
        st.text(),
        st.booleans(),
        st.dictionaries(st.text(), st.text()),
        st.lists(st.text()),
    )
)
def test_circuit_breaker_config_extreme_type_mutation_success_threshold(
    mutated_val: object,
) -> None:
    """Simulate extreme type mutations for success_threshold."""
    with pytest.raises((ValueError, TypeError)):
        CircuitBreakerConfig(success_threshold=mutated_val)  # type: ignore


@settings(
    max_examples=100,
    suppress_health_check=[HealthCheck.too_slow],
    deadline=None,
)
@given(
    st.one_of(
        st.text(),
        st.booleans(),
        st.dictionaries(st.text(), st.text()),
        st.lists(st.text()),
    )
)
def test_circuit_breaker_config_extreme_type_mutation_timeout(
    mutated_val: object,
) -> None:
    """Simulate extreme type mutations for timeout."""
    with pytest.raises((ValueError, TypeError)):
        CircuitBreakerConfig(timeout=mutated_val)  # type: ignore
