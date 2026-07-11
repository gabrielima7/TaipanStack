from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState
from taipanstack.resilience.watchdogs.health_pinger import _force_open_breaker


def test_health_pinger_force_open_cap():
    b = CircuitBreaker()
    b._state.state = CircuitState.CLOSED
    b._state.failure_count = float("-inf")
    b._is_valid_metric = lambda _x: True

    # Should cap the attempts and force open
    _force_open_breaker(b, "test_target")

    assert b.state == CircuitState.OPEN


def test_health_pinger_force_open_normal():
    b = CircuitBreaker(failure_threshold=2)
    b._state.state = CircuitState.CLOSED

    _force_open_breaker(b, "test_target")

    assert b.state == CircuitState.OPEN


def test_health_pinger_force_open_triggers_callback():
    called = []

    def callback(old_state, new_state):
        called.append((old_state, new_state))

    b = CircuitBreaker(on_state_change=callback)
    b._state.state = CircuitState.CLOSED
    b._state.failure_count = float("-inf")
    b._is_valid_metric = lambda _x: True

    _force_open_breaker(b, "test_target")
    assert b.state == CircuitState.OPEN
    assert called == [(CircuitState.CLOSED, CircuitState.OPEN)]
