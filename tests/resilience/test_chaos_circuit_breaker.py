import threading
import time

import pytest

from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitState,
)


def test_circuit_breaker_half_open_starvation():
    breaker = CircuitBreaker(failure_threshold=1, success_threshold=2, timeout=0.1)

    # 1. Trip the circuit
    @breaker
    def fail():
        raise ValueError("fail")

    with pytest.raises(ValueError):
        fail()

    assert breaker.is_open
    time.sleep(0.15)  # Wait for timeout to enter HALF_OPEN

    def hold_lock():
        breaker._state.lock.acquire()
        time.sleep(0.5)
        breaker._state.lock.release()

    @breaker
    def success_thread_safe():
        # spawn a thread to hold the lock for 0.5 seconds
        t = threading.Thread(target=hold_lock)
        t.start()
        # wait a tiny bit to make sure thread holds the lock
        time.sleep(0.05)
        return "ok"

    res1 = success_thread_safe()
    assert res1 == "ok"

    # Wait for the thread to release the lock
    time.sleep(0.6)

    # With the fallback, half_open_attempts should have been decremented
    # successfully, even though lock couldn't be acquired!
    # And since record_success couldn't acquire lock, success_count is 0
    assert breaker._state.success_count == 0
    assert breaker._state.half_open_attempts == 0

    res2 = success_thread_safe()
    assert res2 == "ok"

    time.sleep(0.6)

    assert breaker._state.success_count == 0
    assert breaker._state.half_open_attempts == 0

    # Now it is NOT completely starved! It can make another attempt!

    @breaker
    def final_success():
        return "ok"

    res3 = final_success()
    assert res3 == "ok"
    # we didn't hold the lock, so success count goes up, attempt goes up (then down)

    assert breaker._state.success_count == 1
    assert breaker._state.half_open_attempts == 0

    res4 = final_success()
    assert res4 == "ok"

    assert breaker._state.state == CircuitState.CLOSED
