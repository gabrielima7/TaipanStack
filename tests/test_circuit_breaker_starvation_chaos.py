import threading
import time

import pytest

from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
    CircuitState,
)


def test_circuit_breaker_half_open_starvation_chaos():
    """Simulate lock contention during half-open cleanup, causing starvation."""
    breaker = CircuitBreaker(failure_threshold=1, success_threshold=1, timeout=0.01)

    # Force into OPEN state
    breaker._state.state = CircuitState.OPEN
    breaker._state.last_failure_time = time.monotonic() - 1.0

    sync_event = threading.Event()

    @breaker
    def delayed_success():
        sync_event.set()
        time.sleep(0.3)  # Wait for main thread to grab the lock and cause contention
        return "ok"

    def worker():
        import contextlib

        with contextlib.suppress(Exception):
            delayed_success()

    t = threading.Thread(target=worker)
    t.start()

    # Wait for the worker to pass _should_attempt and enter the function
    sync_event.wait()

    # Grab the lock to simulate heavy contention (e.g., another thread stuck or slow)
    # This ensures that `_record_success` and `_decrement_half_open` will timeout (0.1s).
    acquired = breaker._state.lock.acquire()

    # Wait for worker to finish and try to cleanup (which will fail due to lock)
    t.join()

    # Release the lock so future calls can attempt
    if acquired:
        breaker._state.lock.release()

    # Now check the state of the circuit breaker.
    # If the bug exists, the attempt slot was lost forever, and state is still HALF_OPEN.

    try:
        # A new call should succeed, because either the previous success closed it,
        # or it should at least retry if the slot was freed.
        # But if the slot is permanently lost, this will raise CircuitBreakerError.
        @breaker
        def quick_success():
            return "ok"

        quick_success()
    except CircuitBreakerError:
        pytest.fail("Circuit breaker is permanently starved and stuck in HALF_OPEN!")
