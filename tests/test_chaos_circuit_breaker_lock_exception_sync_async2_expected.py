from taipanstack.resilience.circuit_breaker import CircuitBreaker


def test_circuit_breaker_lock_acquire_exception_record_success_expected():
    breaker = CircuitBreaker(failure_threshold=2)

    class BadLock:
        def acquire(self, timeout=-1):
            raise RuntimeError("Chaos lock acquire error")

        def release(self):
            return None

    breaker._state.lock = BadLock()

    # The exception should not bubble out
    breaker._record_success()


def test_circuit_breaker_lock_acquire_exception_record_failure_expected():
    breaker = CircuitBreaker(failure_threshold=2)

    class BadLock:
        def acquire(self, timeout=-1):
            raise RuntimeError("Chaos lock acquire error")

        def release(self):
            return None

    breaker._state.lock = BadLock()

    # The exception should not bubble out
    breaker._record_failure(ValueError("test error"))


def test_circuit_breaker_lock_acquire_exception_reset_expected():
    breaker = CircuitBreaker(failure_threshold=2)

    class BadLock:
        def acquire(self, timeout=-1):
            raise RuntimeError("Chaos lock acquire error")

        def release(self):
            return None

    breaker._state.lock = BadLock()

    breaker.reset()


def test_circuit_breaker_lock_acquire_exception_decrement_half_open_expected():
    breaker = CircuitBreaker(failure_threshold=2)

    class BadLock:
        def acquire(self, timeout=-1):
            raise RuntimeError("Chaos lock acquire error")

        def release(self):
            return None

    breaker._state.lock = BadLock()

    breaker._decrement_half_open(True)
