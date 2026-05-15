from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState


def test_do_decrement_half_open_negative():
    cb = CircuitBreaker()
    cb._state.state = CircuitState.HALF_OPEN
    cb._state.half_open_attempts = -1
    cb._do_decrement_half_open()
    assert cb._state.half_open_attempts == -1


def test_do_decrement_half_open_infinite():
    cb = CircuitBreaker()
    cb._state.state = CircuitState.HALF_OPEN
    # Use float('inf') to hit the not isfinite branch, which we restored to match original behavior
    cb._state.half_open_attempts = float("inf")
    cb._do_decrement_half_open()
    assert cb._state.half_open_attempts == float("inf")
