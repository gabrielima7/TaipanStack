from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState


def test_circuit_breaker_corrupt_failure_count_to_nan_closed_expected():
    # Setup
    breaker = CircuitBreaker(failure_threshold=5)
    breaker._state.state = CircuitState.CLOSED
    breaker._state.failure_count = float("nan")  # simulate memory corruption

    # Execution
    state_change = breaker._handle_failure_closed()

    # Assert
    assert breaker._state.state == CircuitState.OPEN
    assert state_change == (CircuitState.CLOSED, CircuitState.OPEN)


def test_circuit_breaker_corrupt_failure_count_to_string_closed_expected():
    # Setup
    breaker = CircuitBreaker(failure_threshold=5)
    breaker._state.state = CircuitState.CLOSED
    breaker._state.failure_count = "corrupted"  # simulate memory corruption

    # Execution
    state_change = breaker._handle_failure_closed()

    # Assert
    assert breaker._state.state == CircuitState.OPEN
    assert state_change == (CircuitState.CLOSED, CircuitState.OPEN)


def test_circuit_breaker_corrupt_failure_count_to_nan_update_expected():
    # Setup
    breaker = CircuitBreaker(failure_threshold=5)
    breaker._state.state = CircuitState.CLOSED
    breaker._state.failure_count = float("nan")  # simulate memory corruption

    # Execution
    # the failure count should be reset to max to force circuit opening
    breaker._update_failure_metrics()

    # Assert
    assert breaker._state.failure_count == breaker.config.failure_threshold


def test_circuit_breaker_corrupt_failure_count_to_string_update_expected():
    # Setup
    breaker = CircuitBreaker(failure_threshold=5)
    breaker._state.state = CircuitState.CLOSED
    breaker._state.failure_count = "corrupted"  # simulate memory corruption

    # Execution
    # the failure count should be reset to max to force circuit opening
    breaker._update_failure_metrics()

    # Assert
    assert breaker._state.failure_count == breaker.config.failure_threshold


def test_circuit_breaker_corrupt_half_open_attempts_to_nan_expected():
    # Setup
    breaker = CircuitBreaker(success_threshold=2)
    breaker._state.state = CircuitState.HALF_OPEN
    breaker._state.half_open_attempts = float("nan")  # simulate memory corruption

    can_attempt = breaker._handle_attempt_half_open()

    # Assert
    assert can_attempt is False


def test_circuit_breaker_corrupt_half_open_attempts_to_string_expected():
    # Setup
    breaker = CircuitBreaker(success_threshold=2)
    breaker._state.state = CircuitState.HALF_OPEN
    breaker._state.half_open_attempts = "corrupted"

    can_attempt = breaker._handle_attempt_half_open()

    assert can_attempt is False


def test_circuit_breaker_record_success_open_state_expected():
    # Setup
    breaker = CircuitBreaker()
    breaker._state.state = CircuitState.OPEN

    # Execution
    # It should pass gracefully
    breaker._record_success()

    # Assert
    assert breaker._state.state == CircuitState.OPEN
