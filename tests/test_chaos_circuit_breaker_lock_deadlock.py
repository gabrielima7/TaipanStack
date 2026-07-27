import time

from taipanstack.resilience.circuit_breaker import CircuitBreaker


def test_chaos_circuit_breaker_lock_deadlock():
    breaker = CircuitBreaker(failure_threshold=2)

    # We need to test the actual timeout parameter handling
    class HangingLock:
        def acquire(self, blocking=True, timeout=-1):
            if timeout > 0:
                # the caller passed a timeout!
                time.sleep(timeout)
                return False
            time.sleep(10)
            return False

        def release(self):
            pass

        def __enter__(self):
            self.acquire()
            return True

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.release()

    breaker._state.lock = HangingLock()

    start = time.monotonic()
    should_attempt = breaker._should_attempt()
    end = time.monotonic()

    assert end - start < 5.0, "Circuit breaker lock deadlocked"
    assert should_attempt is False

    breaker._record_success()
    breaker._record_failure(ValueError("test"))
    breaker.reset()
    breaker._decrement_half_open(True)
