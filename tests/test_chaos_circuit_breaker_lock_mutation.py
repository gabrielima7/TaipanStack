import pytest

from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
    CircuitState,
)


def test_chaos_circuit_breaker_malicious_lock_acquire_exception():
    breaker = CircuitBreaker(failure_threshold=2)

    class ThrowingLock:
        def acquire(self, timeout=-1):
            raise MemoryError("Extreme acquire failure")

        def release(self):
            pass

    breaker._state.lock = ThrowingLock()

    @breaker
    def dummy_call():
        return "success"

    with pytest.raises(CircuitBreakerError):
        dummy_call()


def test_chaos_circuit_breaker_malicious_lock_release_suppressed():
    breaker = CircuitBreaker(failure_threshold=2)

    class AcquireOnlyLock:
        def acquire(self, timeout=-1):
            return True

        def release(self):
            raise RuntimeError("Extreme release failure")

    breaker._state.lock = AcquireOnlyLock()

    @breaker
    def dummy_call():
        return "success"

    assert dummy_call() == "success"


def test_chaos_circuit_breaker_malicious_lock_acquire_exception_in_reset():
    breaker = CircuitBreaker(failure_threshold=2)

    class ThrowingLock:
        def acquire(self, timeout=-1):
            raise MemoryError("Extreme acquire failure")

        def release(self):
            pass

    breaker._state.lock = ThrowingLock()

    breaker.reset()
    assert breaker._state.state == CircuitState.CLOSED


def test_chaos_circuit_breaker_malicious_lock_decrement_half_open():
    breaker = CircuitBreaker(failure_threshold=2)

    class ThrowingLock:
        def acquire(self, timeout=-1):
            raise MemoryError("Extreme acquire failure in decrement")

        def release(self):
            pass

    breaker._state.lock = ThrowingLock()

    breaker._decrement_half_open(True)
    assert breaker._state.half_open_attempts == 0


def test_chaos_circuit_breaker_malicious_lock_record_success():
    breaker = CircuitBreaker(failure_threshold=2)

    class ThrowingLock:
        def acquire(self, timeout=-1):
            raise MemoryError("Extreme acquire failure in record_success")

        def release(self):
            pass

    breaker._state.lock = ThrowingLock()

    breaker._record_success()
    assert breaker._state.success_count == 0


def test_chaos_circuit_breaker_malicious_lock_record_failure():
    breaker = CircuitBreaker(failure_threshold=2)

    class ThrowingLock:
        def acquire(self, timeout=-1):
            raise MemoryError("Extreme acquire failure in record_failure")

        def release(self):
            pass

    breaker._state.lock = ThrowingLock()

    breaker._record_failure(RuntimeError("dummy"))
    assert breaker._state.failure_count == 0


def test_chaos_circuit_breaker_malicious_lock_decrement_half_open_suppress():
    breaker = CircuitBreaker(failure_threshold=2)

    class ThrowingLock:
        def acquire(self, timeout=-1):
            raise RuntimeError("Normal acquire failure in decrement")

        def release(self):
            pass

    breaker._state.lock = ThrowingLock()
    breaker._state.state = CircuitState.HALF_OPEN
    breaker._state.half_open_attempts = 1

    # Should suppress Exception and return
    breaker._decrement_half_open(True)
    assert breaker._state.half_open_attempts == 1
