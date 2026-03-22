import threading
import time

import pytest

from taipanstack.utils.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
    CircuitState,
)


def test_circuit_breaker_half_open_thundering_herd() -> None:
    """Simulate a thundering herd during HALF_OPEN state."""
    breaker = CircuitBreaker(failure_threshold=1, success_threshold=2, timeout=0.1)

    @breaker
    def failing_func():
        raise ValueError("Simulated failure")

    # 1. Trip the circuit
    with pytest.raises(ValueError):
        failing_func()

    assert breaker.state == CircuitState.OPEN

    # 2. Wait for timeout to allow half-open
    time.sleep(0.15)

    # 3. Simulate thundering herd: multiple threads trying to call concurrently
    # The first one to check should transition state to HALF_OPEN.
    # The remaining should be restricted.

    allowed_calls = 0
    rejected_calls = 0
    lock = threading.Lock()
    barrier = threading.Barrier(10)

    @breaker
    def slow_recovering_func():
        # Simulate a slow recovering service call
        time.sleep(0.05)
        return "ok"

    def worker():
        nonlocal allowed_calls, rejected_calls
        barrier.wait()
        try:
            slow_recovering_func()
            with lock:
                allowed_calls += 1
        except CircuitBreakerError:
            with lock:
                rejected_calls += 1

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # We want strictly max `success_threshold` (which is 2) allowed calls.
    # If there are more than 2 allowed, it's vulnerable to thundering herd.
    assert allowed_calls <= 2, (
        f"Allowed {allowed_calls} calls, expected max 2 (success_threshold)"
    )
    assert rejected_calls >= 8, f"Rejected {rejected_calls} calls, expected min 8"
