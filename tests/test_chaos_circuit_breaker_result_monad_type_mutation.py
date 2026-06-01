from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState


def test_chaos_circuit_breaker_result_monad_type_mutation_chaos_circuit_breaker_process_result_corrupted_result_standard() -> None:
    """Test _process_result when result is an invalid state."""
    cb = CircuitBreaker()

    class CorruptResult:
        def __init__(self):
            self.corrupt = True

    res = CorruptResult()
    # Mocking as Result type, this will just fall through isinstance checks
    assert cb._process_result(res) == res


def test_chaos_circuit_breaker_result_monad_type_mutation_chaos_circuit_breaker_process_result_corrupted_result_error() -> None:
    from taipanstack.core.result import Err

    cb = CircuitBreaker()

    # Passing an Err, it will unwrap and check failure exceptions
    res = Err(Exception("test"))
    assert cb._process_result(res) == res

    # Passing an Err with excluded exception
    class ExcludedError(Exception):
        def __init__(self, msg):
            super().__init__(msg)

    cb = CircuitBreaker(excluded_exceptions=(ExcludedError,))
    res_ex = Err(ExcludedError("test"))
    assert cb._process_result(res_ex) == res_ex


def test_chaos_circuit_breaker_result_monad_type_mutation_chaos_circuit_breaker_process_result_corrupted_result_ok() -> None:
    from taipanstack.core.result import Ok

    cb = CircuitBreaker()

    # Passing an Ok, it will record success
    res = Ok("success")
    assert cb._process_result(res) == res


def test_chaos_circuit_breaker_result_monad_type_mutation_chaos_circuit_breaker_corrupted_state_fallthrough_standard() -> None:
    """Test corrupted state handling across multiple methods."""
    cb = CircuitBreaker()
    cb._state.state = "INVALID_STATE"  # type: ignore[assignment]
    assert cb._should_attempt() is False
    cb._record_success()
    assert cb._get_failure_state_change() is None
    cb._safe_decrement_half_open_attempts()


def test_chaos_circuit_breaker_result_monad_type_mutation_chaos_circuit_breaker_half_open_attempts_negative_standard() -> None:
    """Test half open attempts becoming negative."""
    cb = CircuitBreaker()
    cb._state.state = CircuitState.HALF_OPEN
    cb._state.half_open_attempts = -1
    cb._safe_decrement_half_open_attempts()
    assert cb._state.half_open_attempts == 0


def test_chaos_circuit_breaker_result_monad_type_mutation_chaos_circuit_breaker_corrupted_half_open_attempts_standard() -> None:
    """Test half open attempts corrupted to a string."""
    cb = CircuitBreaker()
    cb._state.state = CircuitState.HALF_OPEN
    cb._state.half_open_attempts = "corrupted"  # type: ignore[assignment]
    cb._safe_decrement_half_open_attempts()
    assert cb._state.half_open_attempts == 0

    cb._state.half_open_attempts = float("nan")
    cb._safe_decrement_half_open_attempts()
    assert cb._state.half_open_attempts == 0


def test_chaos_circuit_breaker_result_monad_type_mutation_chaos_circuit_breaker_handle_failure_closed_corrupted_failure_count_standard() -> None:
    """Test handle_failure_closed when failure count is corrupted."""
    cb = CircuitBreaker()
    cb._state.state = CircuitState.CLOSED
    cb._state.failure_count = "corrupted"  # type: ignore[assignment]
    state_change = cb._handle_failure_closed()
    assert state_change == (CircuitState.CLOSED, CircuitState.OPEN)
    assert cb._state.state == CircuitState.OPEN

    cb._state.state = CircuitState.CLOSED
    cb._state.failure_count = float("nan")
    state_change = cb._handle_failure_closed()
    assert state_change == (CircuitState.CLOSED, CircuitState.OPEN)
    assert cb._state.state == CircuitState.OPEN
