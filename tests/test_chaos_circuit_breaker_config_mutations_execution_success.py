from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState


def test_chaos_circuit_breaker_config_timeout_mutation_execution_success():
    cb = CircuitBreaker()
    cb._state.state = CircuitState.OPEN
    cb._state.last_failure_time = 0.0  # Set it so time has elapsed

    # Mutate timeout to string
    object.__setattr__(cb.config, "timeout", "corrupted")

    # Should not crash, should fallback
    cb._should_attempt()


def test_chaos_circuit_breaker_config_success_threshold_mutation_execution_success():
    cb = CircuitBreaker()
    cb._state.state = CircuitState.HALF_OPEN

    # Mutate success_threshold to string
    object.__setattr__(cb.config, "success_threshold", "corrupted")

    # Should not crash
    cb._handle_attempt_half_open()
    cb._handle_success_half_open()


def test_chaos_circuit_breaker_config_failure_threshold_mutation_execution_success():
    cb = CircuitBreaker()
    cb._state.state = CircuitState.CLOSED
    cb._state.failure_count = 1

    # Mutate failure_threshold to string
    object.__setattr__(cb.config, "failure_threshold", "corrupted")

    # Should not crash
    cb._handle_failure_closed()


def test_chaos_circuit_breaker_config_timeout_nan_mutation_execution_success():
    cb = CircuitBreaker()
    cb._state.state = CircuitState.OPEN
    cb._state.last_failure_time = 0.0

    object.__setattr__(cb.config, "timeout", float("nan"))

    cb._should_attempt()
