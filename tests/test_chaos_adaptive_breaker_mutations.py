import time

from taipanstack.resilience.adaptive.adaptive_breaker import AdaptiveCircuitBreaker
from taipanstack.resilience.circuit_breaker import CircuitState


def test_chaos_adaptive_breaker_mutations_adaptive_breaker_target_error_rate_mutation():
    """Chaos test: Mutate target_error_rate to a string."""
    breaker = AdaptiveCircuitBreaker(min_throughput=1)
    object.__setattr__(breaker, "_target_error_rate", "corrupted")

    # Should safely fail closed (open the circuit) rather than crashing
    breaker.record_failure(ValueError("test"))
    assert breaker.state == CircuitState.OPEN


def test_chaos_adaptive_breaker_mutations_adaptive_breaker_target_error_rate_nan():
    """Chaos test: Mutate target_error_rate to NaN."""
    breaker = AdaptiveCircuitBreaker(min_throughput=1)
    object.__setattr__(breaker, "_target_error_rate", float("nan"))

    # Should safely fail closed (open the circuit) rather than crashing
    breaker.record_failure(ValueError("test"))
    assert breaker.state == CircuitState.OPEN


def test_chaos_adaptive_breaker_mutations_adaptive_breaker_last_opened_at_mutation():
    """Chaos test: Mutate last_opened_at to a string."""
    breaker = AdaptiveCircuitBreaker()
    breaker._state = CircuitState.OPEN
    object.__setattr__(breaker, "_last_opened_at", "corrupted")

    # Should safely recover to HALF_OPEN to not lock out forever
    assert breaker.state == CircuitState.HALF_OPEN


def test_chaos_adaptive_breaker_mutations_adaptive_breaker_last_opened_at_nan():
    """Chaos test: Mutate last_opened_at to NaN."""
    breaker = AdaptiveCircuitBreaker()
    breaker._state = CircuitState.OPEN
    object.__setattr__(breaker, "_last_opened_at", float("nan"))

    # Should safely recover to HALF_OPEN to not lock out forever
    assert breaker.state == CircuitState.HALF_OPEN


def test_chaos_adaptive_breaker_mutations_adaptive_breaker_clock_jump_backward():
    """Chaos test: Time jumps backward, so elapsed time is negative."""
    breaker = AdaptiveCircuitBreaker(recovery_timeout=30.0)
    breaker._state = CircuitState.OPEN
    breaker._last_opened_at = time.monotonic() + 1000.0  # Time in future

    # Should safely handle elapsed < 0 and allow recovery to prevent lockout
    assert breaker.state == CircuitState.HALF_OPEN


def test_chaos_adaptive_breaker_mutations_adaptive_breaker_time_corruption_nan(
    monkeypatch,
):
    """Chaos test: time.monotonic() returns NaN."""
    breaker = AdaptiveCircuitBreaker(recovery_timeout=30.0)
    breaker._state = CircuitState.OPEN
    breaker._last_opened_at = time.monotonic() - 40.0

    monkeypatch.setattr(time, "monotonic", lambda: float("nan"))

    # Should safely stay OPEN and not crash
    assert breaker.state == CircuitState.OPEN


def test_chaos_adaptive_breaker_mutations_adaptive_breaker_min_throughput_invalid():
    """Test that min_throughput < 1 raises ValueError."""
    import pytest

    with pytest.raises(ValueError, match="min_throughput must be at least 1"):
        AdaptiveCircuitBreaker(min_throughput=0)


def test_chaos_adaptive_breaker_mutations_adaptive_breaker_calculate_error_rate_zero():
    """Test _calculate_error_rate when total is 0 or less."""
    breaker = AdaptiveCircuitBreaker()
    assert breaker._calculate_error_rate(0) == 0.0
    assert breaker._calculate_error_rate(-1) == 0.0
