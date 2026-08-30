import pytest

from taipanstack.resilience.circuit_breaker import CircuitBreakerConfig


def test_chaos_circuit_breaker_nan_config_chaos_circuit_breaker_config_rejects_nan_failure_threshold():
    """Chaos test: Inject NaN for failure_threshold in CircuitBreakerConfig."""
    with pytest.raises(ValueError, match="finite"):
        CircuitBreakerConfig(failure_threshold=float("nan"))


def test_chaos_circuit_breaker_nan_config_chaos_circuit_breaker_config_rejects_nan_success_threshold():
    """Chaos test: Inject NaN for success_threshold in CircuitBreakerConfig."""
    with pytest.raises(ValueError, match="finite"):
        CircuitBreakerConfig(success_threshold=float("nan"))


def test_chaos_circuit_breaker_nan_config_chaos_circuit_breaker_config_rejects_nan_timeout():
    """Chaos test: Inject NaN for timeout in CircuitBreakerConfig."""
    with pytest.raises(ValueError, match="finite"):
        CircuitBreakerConfig(timeout=float("nan"))
