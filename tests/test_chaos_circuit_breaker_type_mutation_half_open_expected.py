from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState


def test_chaos_circuit_breaker_type_mutation_half_open_circuit_breaker_type_corruption_half_open_attempts_negative_expected() -> (
    None
):
    breaker = CircuitBreaker(
        name="test_half_open", failure_threshold=3, success_threshold=2
    )
    breaker._state.state = CircuitState.HALF_OPEN
    breaker._state.half_open_attempts = -1
    breaker._safe_decrement_half_open_attempts()
    # It now resets corrupted (negative) attempts to 0, which is correctly handling the logic error
    assert breaker._state.half_open_attempts == 0


def test_chaos_circuit_breaker_type_mutation_half_open_circuit_breaker_type_corruption_half_open_attempts_zero_expected() -> (
    None
):
    breaker = CircuitBreaker(
        name="test_half_open", failure_threshold=3, success_threshold=2
    )
    breaker._state.state = CircuitState.HALF_OPEN
    breaker._state.half_open_attempts = 0
    breaker._safe_decrement_half_open_attempts()
    assert breaker._state.half_open_attempts == 0


def test_chaos_circuit_breaker_type_mutation_half_open_circuit_breaker_type_corruption_half_open_attempts_corrupted_expected() -> (
    None
):
    breaker = CircuitBreaker(
        name="test_half_open", failure_threshold=3, success_threshold=2
    )
    breaker._state.state = CircuitState.HALF_OPEN
    breaker._state.half_open_attempts = "corrupted"  # type: ignore[assignment]
    breaker._safe_decrement_half_open_attempts()
    assert breaker._state.half_open_attempts == 0


def test_chaos_circuit_breaker_type_mutation_half_open_circuit_breaker_type_corruption_half_open_attempts_decrement_expected() -> (
    None
):
    breaker = CircuitBreaker(
        name="test_half_open", failure_threshold=3, success_threshold=2
    )
    breaker._state.state = CircuitState.HALF_OPEN
    breaker._state.half_open_attempts = 1
    breaker._safe_decrement_half_open_attempts()
    assert breaker._state.half_open_attempts == 0


def test_chaos_circuit_breaker_type_mutation_half_open_circuit_breaker_type_corruption_half_open_attempts_decrement_closed_expected() -> (
    None
):
    breaker = CircuitBreaker(
        name="test_half_open", failure_threshold=3, success_threshold=2
    )
    breaker._state.state = CircuitState.CLOSED
    breaker._safe_decrement_half_open_attempts()
    assert breaker._state.half_open_attempts == 0


def test_chaos_circuit_breaker_type_mutation_half_open_circuit_breaker_decrement_half_open_false_expected() -> (
    None
):
    breaker = CircuitBreaker(
        name="test_half_open", failure_threshold=3, success_threshold=2
    )
    breaker._state.state = CircuitState.HALF_OPEN
    breaker._state.half_open_attempts = 1
    breaker._decrement_half_open(False)
    assert breaker._state.half_open_attempts == 1


def test_chaos_circuit_breaker_type_mutation_half_open_circuit_breaker_decrement_half_open_true_expected() -> (
    None
):
    breaker = CircuitBreaker(
        name="test_half_open", failure_threshold=3, success_threshold=2
    )
    breaker._state.state = CircuitState.HALF_OPEN
    breaker._state.half_open_attempts = 1
    breaker._decrement_half_open(True)
    assert breaker._state.half_open_attempts == 0


def test_chaos_circuit_breaker_type_mutation_half_open_circuit_breaker_safe_decrement_attempts_zero_expected() -> (
    None
):
    breaker = CircuitBreaker(
        name="test_half_open", failure_threshold=3, success_threshold=2
    )
    breaker._state.state = CircuitState.HALF_OPEN
    breaker._state.half_open_attempts = 0
    breaker._safe_decrement_half_open_attempts()
    assert breaker._state.half_open_attempts == 0
