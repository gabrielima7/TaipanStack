from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState


class EvilInt(int):
    def __ge__(self, other):
        raise RuntimeError("Evil __ge__")

    def __gt__(self, other):
        raise RuntimeError("Evil __gt__")

    def __add__(self, other):
        raise RuntimeError("Evil __add__")

    def __sub__(self, other):
        raise RuntimeError("Evil __sub__")


def test_chaos_cb_evil_int_half_open():
    breaker = CircuitBreaker(failure_threshold=1)
    breaker._state.state = CircuitState.HALF_OPEN
    breaker._state.half_open_attempts = EvilInt(1)

    # This should safely degrade instead of crashing
    breaker._safe_decrement_half_open_attempts()
    # It safely degrading means it resets the attempt to 0 upon detecting corruption
    assert breaker._state.half_open_attempts == 0


def test_chaos_cb_evil_int_failure_count():
    breaker = CircuitBreaker(failure_threshold=1)
    breaker._state.failure_count = EvilInt(0)

    # This should not crash
    breaker._increment_failure_count()
    # Safely degrades by setting it to the threshold to immediately trigger OPEN
    assert breaker._state.failure_count == breaker.config.failure_threshold


def test_chaos_cb_evil_int_is_valid_metric():
    # The check involves >= which is __ge__ in python 3
    # If it crashes, the function isn't safe. The hardened code should return False
    assert CircuitBreaker._is_valid_metric(EvilInt(0)) is False
