import contextlib

import pytest

from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
    CircuitState,
)


class BrokenLock:
    def acquire(self, timeout=-1):
        return False

    def release(self):
        pass


def test_circuit_breaker_lock_failure_degrades_to_allow_if_closed():
    breaker = CircuitBreaker()

    @breaker
    def successful_call():
        return "ok"

    breaker._state.lock = BrokenLock()
    assert successful_call() == "ok"


def test_circuit_breaker_lock_failure_degrades_to_deny_if_open():
    breaker = CircuitBreaker(failure_threshold=1)

    @breaker
    def failing_call():
        raise ValueError("failure")

    with contextlib.suppress(ValueError):
        failing_call()

    assert breaker.state == CircuitState.OPEN

    breaker._state.lock = BrokenLock()
    with pytest.raises(CircuitBreakerError):
        failing_call()
