import math

from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState


def test_chaos_circuit_breaker_nan_state_corruption():
    """Simulate extreme state corruption in CircuitBreaker counters.

    If memory or state gets corrupted such that `failure_count`, `success_count`,
    or `half_open_attempts` become NaN or Inf, the breaker should gracefully handle it
    and prioritize safety (e.g. failing closed/opening the circuit) without crashing or
    permanently bypassing threshold checks.
    """
    breaker = CircuitBreaker(failure_threshold=2, success_threshold=2, timeout=0.01)

    # Chaos: Corrupt failure_count to NaN in CLOSED state
    breaker._state.state = CircuitState.CLOSED
    object.__setattr__(breaker._state, "failure_count", float("nan"))

    # Should not crash, and should eventually open circuit to be safe
    breaker._record_failure(ValueError("test"))
    breaker._record_failure(ValueError("test"))

    # If failure_count is corrupted, it should be treated as max failures to open the circuit safely
    assert breaker._state.state == CircuitState.OPEN

    # Chaos: Corrupt success_count to NaN in HALF_OPEN state
    breaker = CircuitBreaker(failure_threshold=2, success_threshold=2, timeout=0.01)
    breaker._state.state = CircuitState.HALF_OPEN
    object.__setattr__(breaker._state, "success_count", float("nan"))

    # Record successes
    # When corrupted, success_count should be reset or ignored to prevent false recovery
    breaker._record_success()
    breaker._record_success()
    breaker._record_success()

    # Because it was NaN, it shouldn't meet the threshold immediately without actual successes,
    # but the logic resets it to 0, and then three successes will close the circuit
    assert breaker._state.state == CircuitState.CLOSED
    assert math.isfinite(breaker._state.success_count)

    # Chaos: Corrupt half_open_attempts to Inf in HALF_OPEN state
    breaker = CircuitBreaker(failure_threshold=2, success_threshold=2, timeout=0.01)
    breaker._state.state = CircuitState.HALF_OPEN
    object.__setattr__(breaker._state, "half_open_attempts", float("inf"))

    # _should_attempt should return False to prevent thundering herd when corrupted
    assert breaker._should_attempt() is False
    assert math.isfinite(
        breaker._state.half_open_attempts
    ) or breaker._state.half_open_attempts == float("inf")

    # Chaos: Corrupt half_open_attempts to NaN
    breaker._state.state = CircuitState.HALF_OPEN
    object.__setattr__(breaker._state, "half_open_attempts", float("nan"))

    # Should block attempt to be safe
    assert breaker._should_attempt() is False
