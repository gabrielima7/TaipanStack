import time

import pytest

from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState


def test_chaos_circuit_breaker_time_corruption_circuit_breaker_chaos_time_corruption_standard_expected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Chaos test: simulate time.monotonic() returning NaN or Inf."""
    breaker = CircuitBreaker(failure_threshold=1, timeout=10.0)

    # Force failure -> OPEN
    try:
        raise ValueError("failure")
    except ValueError as e:
        breaker._record_failure(e)

    assert breaker._state.state == CircuitState.OPEN

    # 1. NaN test
    monkeypatch.setattr(time, "monotonic", lambda: float("nan"))
    # Should not attempt, NaN elapsed time shouldn't be >= timeout
    assert breaker._should_attempt() is False
    assert breaker._state.state == CircuitState.OPEN

    # 2. Inf test
    monkeypatch.setattr(time, "monotonic", lambda: float("inf"))
    # Should not attempt, Inf elapsed time could artificially advance it to HALF_OPEN, we want to protect against this
    assert breaker._should_attempt() is False
    assert breaker._state.state == CircuitState.OPEN


def test_chaos_circuit_breaker_time_corruption_circuit_breaker_chaos_time_corruption_record_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    breaker = CircuitBreaker(failure_threshold=2, timeout=10.0)

    monkeypatch.setattr(time, "monotonic", lambda: float("nan"))
    try:
        raise ValueError("failure")
    except ValueError as e:
        breaker._record_failure(e)

    assert breaker._state.last_failure_time == 0.0  # Default value
