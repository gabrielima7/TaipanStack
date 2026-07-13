from unittest import mock

from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState


def test_circuit_breaker_callback_exception_logging():
    def exploding_callback(_old, _new):
        raise ValueError("Boom!")

    cb = CircuitBreaker(on_state_change=exploding_callback)

    cb._state.failure_count = cb.config.failure_threshold
    cb._should_attempt()
    cb._record_failure(Exception("test"))

    assert cb.state == CircuitState.OPEN


def test_circuit_breaker_failure_count_property():
    cb = CircuitBreaker()
    cb._state.failure_count = 42
    assert cb.failure_count == 42


@mock.patch("taipanstack.resilience.circuit_breaker._HAS_STRUCTLOG", False)
def test_circuit_breaker_notify_state_change_no_callback_no_structlog():
    cb = CircuitBreaker()

    cb._state.failure_count = cb.config.failure_threshold
    cb._should_attempt()
    cb._record_failure(Exception("test"))

    assert cb.state == CircuitState.OPEN
