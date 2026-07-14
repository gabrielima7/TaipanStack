import pytest

from taipanstack.resilience.adaptive.adaptive_breaker import AdaptiveCircuitBreaker
from taipanstack.resilience.adaptive.bulkhead import Bulkhead
from taipanstack.resilience.adaptive.orchestrator import ResilienceOrchestrator
from taipanstack.resilience.circuit_breaker import CircuitBreaker


def test_chaos_circuit_breaker_nan_circuit_breaker_rejects_nan_failure_threshold_execution_success():
    """Chaos test: Inject NaN for failure_threshold."""
    with pytest.raises(ValueError, match="must be a finite"):
        CircuitBreaker(failure_threshold=float("nan"))


def test_chaos_circuit_breaker_nan_circuit_breaker_rejects_nan_success_threshold_execution_success():
    """Chaos test: Inject NaN for success_threshold."""
    with pytest.raises(ValueError, match="must be a finite"):
        CircuitBreaker(success_threshold=float("nan"))


def test_chaos_circuit_breaker_nan_circuit_breaker_rejects_inf_failure_threshold_execution_success():
    """Chaos test: Inject Inf for failure_threshold."""
    with pytest.raises(ValueError, match="must be a finite"):
        CircuitBreaker(failure_threshold=float("inf"))


def test_chaos_circuit_breaker_nan_circuit_breaker_rejects_inf_success_threshold_execution_success():
    """Chaos test: Inject Inf for success_threshold."""
    with pytest.raises(ValueError, match="must be a finite"):
        CircuitBreaker(success_threshold=float("inf"))


def test_chaos_circuit_breaker_nan_adaptive_breaker_rejects_nan_recovery_timeout_execution_success():
    """Chaos test: Inject NaN for recovery timeout."""
    with pytest.raises(ValueError, match="must be a finite"):
        AdaptiveCircuitBreaker(recovery_timeout=float("nan"))


def test_chaos_circuit_breaker_nan_bulkhead_rejects_nan_timeout_execution_success():
    """Chaos test: Inject NaN for timeout."""
    with pytest.raises(ValueError, match="must be a finite"):
        Bulkhead("default", timeout=float("nan"))


def test_chaos_circuit_breaker_nan_orchestrator_rejects_nan_timeout_execution_success():
    """Chaos test: Inject NaN for orchestrator timeout."""
    with pytest.raises(ValueError, match="must be a finite"):
        ResilienceOrchestrator().with_timeout(float("nan"))


def test_chaos_circuit_breaker_nan_orchestrator_with_bulkhead_rejects_nan_timeout_execution_success():
    """Chaos test: Inject NaN for orchestrator bulkhead timeout."""
    with pytest.raises(ValueError, match="finite non-negative number"):
        ResilienceOrchestrator().with_bulkhead(timeout=float("nan"))
