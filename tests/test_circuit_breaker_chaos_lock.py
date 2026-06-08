from taipanstack.resilience.circuit_breaker import CircuitBreaker


class ExplodingLock:
    def __enter__(self):
        raise RuntimeError("Resource exhaustion")

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def test_circuit_breaker_lock_exhaustion_should_attempt():
    breaker = CircuitBreaker()
    breaker._state.lock = ExplodingLock()
    assert breaker._should_attempt() is False


def test_circuit_breaker_lock_exhaustion_record_success():
    breaker = CircuitBreaker()
    breaker._state.lock = ExplodingLock()
    breaker._record_success()


def test_circuit_breaker_lock_exhaustion_record_failure():
    breaker = CircuitBreaker()
    breaker._state.lock = ExplodingLock()
    breaker._record_failure(ValueError("test"))


def test_circuit_breaker_lock_exhaustion_reset():
    breaker = CircuitBreaker()
    breaker._state.lock = ExplodingLock()
    breaker.reset()


def test_circuit_breaker_lock_exhaustion_decrement_half_open():
    breaker = CircuitBreaker()
    breaker._state.lock = ExplodingLock()
    breaker._decrement_half_open(True)
