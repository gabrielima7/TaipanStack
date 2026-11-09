from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState


def test_chaos_circuit_breaker_half_open_starvation():
    breaker = CircuitBreaker(success_threshold=1, timeout=0.1)
    breaker._state.state = CircuitState.HALF_OPEN
    breaker._state.half_open_attempts = 1

    # Hold the lock
    breaker._state.lock.acquire()

    breaker._decrement_half_open(True)

    # Release lock before assert to avoid hanging in some environments
    breaker._state.lock.release()

    assert breaker._state.half_open_attempts == 0
