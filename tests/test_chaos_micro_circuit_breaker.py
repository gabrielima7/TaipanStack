import time

import pytest

from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState


def test_chaos_circuit_breaker_calculate_elapsed_time_type_mutation():
    """Simulate state corruption where last_failure_time is mutated to a malicious type."""

    class CorruptFloat(float):
        def __sub__(self, other):
            raise RuntimeError("Chaos __sub__")

        def __rsub__(self, other):
            raise RuntimeError("Chaos __rsub__")

        def __float__(self):
            raise RuntimeError("Chaos __float__")

    breaker = CircuitBreaker(failure_threshold=3, timeout=0.1)
    breaker._state.state = CircuitState.OPEN
    breaker._state.last_failure_time = CorruptFloat(100.0)

    try:
        elapsed = breaker._calculate_elapsed_time(200.0)
        # Because of corruption, it should degrade safely, returning safe_timeout
        assert elapsed == breaker._get_safe_timeout()
    except Exception as e:
        pytest.fail(f"CircuitBreaker crashed with exception: {e}")


def test_chaos_circuit_breaker_get_valid_elapsed_type_mutation(
    monkeypatch: pytest.MonkeyPatch,
):
    """Simulate time.monotonic returning a malicious type."""

    class CorruptFloat(float):
        def __ge__(self, other):
            raise RuntimeError("Chaos __ge__")

    monkeypatch.setattr(time, "monotonic", lambda: CorruptFloat(100.0))
    breaker = CircuitBreaker(failure_threshold=3, timeout=0.1)
    breaker._state.state = CircuitState.OPEN
    breaker._state.last_failure_time = 50.0

    try:
        # math.isfinite inside _get_valid_elapsed or > / < might fail
        elapsed = breaker._get_valid_elapsed()
        assert (
            elapsed is None or elapsed == 50.0
        )  # elapsed could be calculated if isfinite doesn't fail
    except Exception as e:
        pytest.fail(f"CircuitBreaker crashed with exception: {e}")


def test_chaos_circuit_breaker_get_valid_elapsed_type_mutation_not_isfinite(
    monkeypatch: pytest.MonkeyPatch,
):
    """Simulate time.monotonic returning a malicious type."""

    class CorruptFloat(float):
        def __sub__(self, other):
            raise RuntimeError("Chaos __sub__")

    monkeypatch.setattr(time, "monotonic", lambda: CorruptFloat(100.0))
    breaker = CircuitBreaker(failure_threshold=3, timeout=0.1)
    breaker._state.state = CircuitState.OPEN
    breaker._state.last_failure_time = 50.0

    try:
        # math.isfinite inside _get_valid_elapsed or > / < might fail
        elapsed = breaker._get_valid_elapsed()
        assert elapsed is None or elapsed in {0.1, 30.0}
    except Exception as e:
        pytest.fail(f"CircuitBreaker crashed with exception: {e}")


def test_chaos_circuit_breaker_get_valid_elapsed_type_mutation_isfinite_runtime(
    monkeypatch: pytest.MonkeyPatch,
):
    """Simulate time.monotonic returning a malicious type."""

    class CorruptFloat(float):
        def __ge__(self, other):
            raise RuntimeError("Chaos __ge__")

    monkeypatch.setattr(time, "monotonic", lambda: CorruptFloat(100.0))
    import math

    original_isfinite = math.isfinite

    def fake_isfinite(val):
        if isinstance(val, CorruptFloat):
            raise TypeError("Chaos isfinite")
        return original_isfinite(val)

    monkeypatch.setattr(math, "isfinite", fake_isfinite)

    breaker = CircuitBreaker(failure_threshold=3, timeout=0.1)
    breaker._state.state = CircuitState.OPEN
    breaker._state.last_failure_time = 50.0

    try:
        # math.isfinite inside _get_valid_elapsed or > / < might fail
        elapsed = breaker._get_valid_elapsed()
        assert elapsed is None
    except Exception as e:
        pytest.fail(f"CircuitBreaker crashed with exception: {e}")
