import pytest

from taipanstack.resilience.adaptive.adaptive_breaker import AdaptiveCircuitBreaker
from taipanstack.resilience.adaptive.bulkhead import Bulkhead
from taipanstack.resilience.adaptive.orchestrator import ResilienceOrchestrator
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


def test_adaptive_breaker_rejects_nan_recovery_timeout():
    with pytest.raises(ValueError, match="must be a finite"):
        AdaptiveCircuitBreaker(recovery_timeout=float("nan"))

def test_bulkhead_rejects_nan_timeout():
    with pytest.raises(ValueError, match="must be a finite"):
        Bulkhead(timeout=float("nan"))

def test_orchestrator_rejects_nan_timeout():
    with pytest.raises(ValueError, match="must be a finite"):
        ResilienceOrchestrator().with_timeout(float("nan"))
