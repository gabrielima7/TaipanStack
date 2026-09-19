import threading

import pytest

from taipanstack.resilience.circuit_breaker import CircuitBreaker


def test_circuit_breaker_callback_no_deadlock_circuit_breaker_callback_deadlock_prevented_expected() -> (
    None
):
    in_callback = threading.Event()
    finish_callback = threading.Event()

    def on_change(_old, _new):
        in_callback.set()
        finish_callback.wait(timeout=5.0)

    cb = CircuitBreaker(failure_threshold=1, on_state_change=on_change)

    def fail_call():
        cb._record_failure(Exception("test"))

    t1 = threading.Thread(target=fail_call)
    t1.start()

    assert in_callback.wait(timeout=2.0), "Callback was not reached"

    # Try to acquire lock. If cb holds lock during callback, this times out.
    locked = cb._state.lock.acquire(blocking=True, timeout=0.2)

    finish_callback.set()
    t1.join()

    if not locked:
        pytest.fail(
            "VULNERABILITY: Circuit breaker holds internal lock during state change callbacks, allowing slow callbacks to deadlock the system."
        )
    else:
        cb._state.lock.release()
