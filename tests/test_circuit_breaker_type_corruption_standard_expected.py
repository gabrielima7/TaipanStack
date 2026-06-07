from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState


def test_circuit_breaker_type_corruption_half_open_attempts_standard_expected() -> None:
    breaker = CircuitBreaker(
        name="test_half_open", failure_threshold=3, success_threshold=2
    )
    breaker._state.state = CircuitState.HALF_OPEN
    # Induce type mutation
    breaker._state.half_open_attempts = "corrupted"  # type: ignore[assignment]
    # This should return False because it catches TypeError in math.isfinite()
    assert breaker._handle_attempt_half_open() is False


def test_circuit_breaker_type_corruption_success_count_standard_expected() -> None:
    breaker = CircuitBreaker(
        name="test_success", failure_threshold=3, success_threshold=2
    )
    breaker._state.state = CircuitState.HALF_OPEN
    # Induce type mutation
    breaker._state.success_count = "corrupted"  # type: ignore[assignment]
    # It catches TypeError, resets to 1, and stays HALF_OPEN because 1 < 2
    breaker._handle_success_half_open()
    assert breaker._state.success_count == 1
    assert breaker._state.state == CircuitState.HALF_OPEN


def test_circuit_breaker_type_corruption_failure_count_in_update_standard_expected() -> None:
    breaker = CircuitBreaker(
        name="test_failure_update", failure_threshold=3, success_threshold=2
    )
    breaker._state.state = CircuitState.CLOSED
    # Induce type mutation
    breaker._state.failure_count = "corrupted"  # type: ignore[assignment]
    # It catches TypeError in math.isfinite() inside _update_failure_metrics
    # Safe degradation sets failure_count to config.failure_threshold
    breaker._update_failure_metrics()
    assert breaker._state.failure_count == 3


def test_circuit_breaker_type_corruption_handle_failure_closed_direct_standard_expected() -> None:
    breaker = CircuitBreaker(
        name="test_failure_closed", failure_threshold=3, success_threshold=2
    )
    breaker._state.state = CircuitState.CLOSED
    # Set to type mutation
    breaker._state.failure_count = "corrupted"  # type: ignore[assignment]
    breaker._handle_failure_closed()
    assert breaker._state.state == CircuitState.OPEN
