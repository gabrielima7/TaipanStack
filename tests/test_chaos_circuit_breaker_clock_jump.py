import time

import pytest

from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
    CircuitState,
)


def test_chaos_circuit_breaker_clock_jump_circuit_breaker_backward_clock_jump_chaos_expected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Simulate a backward clock jump (NTP anomaly) keeping circuit OPEN forever."""
    breaker = CircuitBreaker(failure_threshold=1, timeout=10.0)

    time_val = 1000.0
    monkeypatch.setattr(time, "monotonic", lambda: time_val)

    @breaker
    def failing_func():
        raise ValueError("Fail")

    with pytest.raises(ValueError):
        failing_func()

    assert breaker.state == CircuitState.OPEN

    # Clock jumps backward by 1 day!
    time_val = 1000.0 - 86400.0

    # Wait for the normal timeout (10 seconds)
    time_val += 10.0

    # We expect the breaker to recognize the clock jump and allow a HALF_OPEN attempt,
    # rather than staying OPEN for 86400 seconds.
    try:
        failing_func()
    except CircuitBreakerError:
        pytest.fail("CircuitBreaker got stuck OPEN due to backward clock jump!")
    except ValueError:
        assert True

    assert breaker.state == CircuitState.OPEN  # Reopened after failure
