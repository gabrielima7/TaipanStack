import time

from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState


def test_chaos_circuit_breaker_time_monotonic_mutation_survives_string_corruption(
    monkeypatch,
) -> None:
    cb = CircuitBreaker()
    cb._state.state = CircuitState.OPEN
    cb._state.last_failure_time = 100.0

    monkeypatch.setattr(time, "monotonic", lambda: "corrupted_time_string")

    # Should not raise TypeError, but safely handle the corruption
    assert cb._should_attempt() is True
    assert cb._state.state == CircuitState.HALF_OPEN


def test_chaos_circuit_breaker_time_monotonic_mutation_survives_none_corruption(
    monkeypatch,
) -> None:
    cb = CircuitBreaker()
    cb._state.state = CircuitState.OPEN
    cb._state.last_failure_time = 100.0

    monkeypatch.setattr(time, "monotonic", lambda: None)

    # Should not raise TypeError, but safely handle the corruption
    assert cb._should_attempt() is True
    assert cb._state.state == CircuitState.HALF_OPEN
