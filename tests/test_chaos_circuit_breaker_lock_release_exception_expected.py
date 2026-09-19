from taipanstack.resilience.circuit_breaker import CircuitBreaker


def test_chaos_circuit_breaker_lock_release_raises_expected():
    breaker = CircuitBreaker(failure_threshold=2)

    class BadLock:
        def acquire(self, timeout=-1):
            return True

        def release(self):
            raise RuntimeError("Chaos lock release error")

    breaker._state.lock = BadLock()

    # This will crash if release() is not safely handled
    breaker._should_attempt()

    # We should also cover the other places where release is called
    breaker._record_success()
    breaker._record_failure(Exception("test"))
    breaker.reset()
    breaker._decrement_half_open(True)
