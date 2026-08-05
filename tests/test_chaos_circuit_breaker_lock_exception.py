from taipanstack.resilience.circuit_breaker import CircuitBreaker


def test_chaos_circuit_breaker_lock_acquire_raises():
    breaker = CircuitBreaker(failure_threshold=2)

    class BadLock:
        def acquire(self, timeout=-1):
            raise RuntimeError("Chaos lock acquire error")
        def release(self):
            pass

    breaker._state.lock = BadLock()

    # This shouldn't crash if we are resilient!
    result = breaker._should_attempt()
    assert result is False
