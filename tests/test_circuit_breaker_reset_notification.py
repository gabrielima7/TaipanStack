from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState


def test_circuit_breaker_reset_notification():
    notified = []

    def on_change(old, new):
        notified.append((old, new))

    cb = CircuitBreaker(failure_threshold=1, on_state_change=on_change)

    # Trigger a failure to open the circuit
    cb._record_failure(ValueError("test error"))
    assert cb.state == CircuitState.OPEN
    assert len(notified) == 1
    assert notified[0] == (CircuitState.CLOSED, CircuitState.OPEN)

    # Clear the list
    notified.clear()

    # Reset should trigger notification
    cb.reset()
    assert cb.state == CircuitState.CLOSED
    assert len(notified) == 1
    assert notified[0] == (CircuitState.OPEN, CircuitState.CLOSED)

    # Reset again should do nothing
    notified.clear()
    cb.reset()
    assert cb.state == CircuitState.CLOSED
    assert len(notified) == 0
