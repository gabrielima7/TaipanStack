import pytest

from taipanstack.resilience.circuit_breaker import CircuitBreaker


def test_circuit_breaker_rejects_nan_failure_threshold():
    """Chaos test: Inject NaN for failure_threshold."""
    with pytest.raises(ValueError, match="must be a finite"):
        CircuitBreaker(failure_threshold=float("nan"))


def test_circuit_breaker_rejects_nan_success_threshold():
    """Chaos test: Inject NaN for success_threshold."""
    with pytest.raises(ValueError, match="must be a finite"):
        CircuitBreaker(success_threshold=float("nan"))


def test_circuit_breaker_rejects_inf_failure_threshold():
    """Chaos test: Inject Inf for failure_threshold."""
    with pytest.raises(ValueError, match="must be a finite"):
        CircuitBreaker(failure_threshold=float("inf"))


def test_circuit_breaker_rejects_inf_success_threshold():
    """Chaos test: Inject Inf for success_threshold."""
    with pytest.raises(ValueError, match="must be a finite"):
        CircuitBreaker(success_threshold=float("inf"))
