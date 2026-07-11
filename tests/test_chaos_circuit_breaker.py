import contextlib
import time

from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitState,
)


def test_circuit_breaker_chaos_time_and_timeout_corruption():
    breaker = CircuitBreaker(failure_threshold=1)

    # Simulate a failure to open the circuit
    @breaker
    def failing_func():
        raise ValueError("Fail")

    with contextlib.suppress(ValueError):
        failing_func()

    assert breaker.state == CircuitState.OPEN

    # Chaos 1: Corrupt last_failure_time to NaN and timeout to a string
    breaker._state.last_failure_time = float("nan")
    object.__setattr__(breaker.config, "timeout", "corrupted")

    # Because last_failure_time is NaN, _calculate_elapsed_time should return safe_timeout (30.0)
    # The elapsed time of 30.0 will be compared against timeout (which will also be safely parsed as 30.0 or default).
    # _should_attempt() will trigger a transition to HALF_OPEN.
    assert breaker._should_attempt() is True
    assert breaker.state == CircuitState.HALF_OPEN

    # Reset
    breaker.reset()
    with contextlib.suppress(ValueError):
        failing_func()
    assert breaker.state == CircuitState.OPEN

    # Chaos 2: Backward clock jump and invalid type for timeout (a tuple)
    breaker._state.last_failure_time = time.monotonic() + 10000.0  # Future time
    object.__setattr__(breaker.config, "timeout", (1, 2, 3))  # TypeError

    # Because elapsed < 0, it should return safe_timeout (30.0)
    # _handle_open_state defaults config.timeout to 30.0 because it's a tuple.
    # elapsed (30.0) >= timeout (30.0) -> transitions to HALF_OPEN
    assert breaker._should_attempt() is True
    assert breaker.state == CircuitState.HALF_OPEN
