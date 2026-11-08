from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState

def test_chaos_circuit_breaker_missing_config_chaos_circuit_breaker_missing_config_is_failure_exception():
    cb = CircuitBreaker()
    cb.config = None
    assert cb._is_failure_exception(ValueError("foo")) == True

def test_chaos_circuit_breaker_missing_config_chaos_circuit_breaker_missing_config_is_excluded_exception():
    cb = CircuitBreaker()
    cb.config = None
    assert cb._is_excluded_exception(ValueError("foo")) == False

def test_chaos_circuit_breaker_missing_config_chaos_circuit_breaker_missing_config_handle_exception_in_call():
    cb = CircuitBreaker()
    cb.config = None
    cb._handle_exception_in_call(ValueError("foo"))
    assert cb._state.failure_count == 1

def test_chaos_circuit_breaker_missing_config_chaos_circuit_breaker_missing_config_get_safe_timeout():
    cb = CircuitBreaker()
    cb.config = None
    assert cb._get_safe_timeout() == 30.0

def test_chaos_circuit_breaker_missing_config_chaos_circuit_breaker_missing_config_evaluate_open_timeout():
    cb = CircuitBreaker()
    cb.config = None
    cb._state.state = CircuitState.OPEN
    cb._state.last_failure_time = 0.0
    # Should open and transition to half open with elapsed time > default 30
    should_attempt, state_change = cb._evaluate_open_timeout(31.0)
    assert should_attempt == True
    assert state_change == (CircuitState.OPEN, CircuitState.HALF_OPEN)

def test_chaos_circuit_breaker_missing_config_chaos_circuit_breaker_missing_config_handle_attempt_half_open():
    cb = CircuitBreaker()
    cb.config = None
    cb._state.state = CircuitState.HALF_OPEN
    assert cb._handle_attempt_half_open() == True

def test_chaos_circuit_breaker_missing_config_chaos_circuit_breaker_missing_config_handle_success_half_open():
    cb = CircuitBreaker()
    cb.config = None
    cb._state.state = CircuitState.HALF_OPEN
    state_change = cb._handle_success_half_open()
    assert state_change == None

def test_chaos_circuit_breaker_missing_config_chaos_circuit_breaker_missing_config_handle_failure_closed():
    cb = CircuitBreaker()
    cb.config = None
    cb._state.state = CircuitState.CLOSED
    cb._state.failure_count = 5
    state_change = cb._handle_failure_closed()
    assert state_change == (CircuitState.CLOSED, CircuitState.OPEN)

def test_chaos_circuit_breaker_missing_config_chaos_circuit_breaker_missing_config_increment_failure_count():
    cb = CircuitBreaker()
    cb.config = None
    cb._state.failure_count = "corrupted"
    cb._increment_failure_count()
    assert cb._state.failure_count == 5
