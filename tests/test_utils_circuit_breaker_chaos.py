import threading
import time
import pytest

from taipanstack.utils.circuit_breaker import CircuitBreaker, CircuitState, CircuitBreakerError

def test_circuit_breaker_chaos_thundering_herd_half_open():
    """Simulate a thundering herd on a recovering service in HALF_OPEN state.

    If the circuit is HALF_OPEN, it should only allow a limited number of requests
    (typically `success_threshold`) to test the waters. If it allows an unlimited
    number of concurrent requests, a thundering herd could overwhelm the fragile
    service before it has fully recovered.
    """
    breaker = CircuitBreaker(failure_threshold=1, success_threshold=2, timeout=0.1)

    # 1. Trip the circuit to OPEN
    try:
        @breaker
        def fail_func():
            raise ValueError("Service unavailable")
        fail_func()
    except ValueError:
        pass

    assert breaker.state == CircuitState.OPEN

    # 2. Wait for timeout to allow HALF_OPEN transition
    time.sleep(0.15)

    # 3. Simulate a massive concurrent spike of 100 requests exactly when it transitions to HALF_OPEN.
    # We want to see how many requests actually slip through to the target service.
    allowed_executions = 0
    lock = threading.Lock()

    @breaker
    def test_water_func():
        nonlocal allowed_executions
        with lock:
            allowed_executions += 1
        # Simulate some network delay so all threads have time to enter HALF_OPEN
        time.sleep(0.1)
        return "ok"

    def worker():
        try:
            test_water_func()
        except CircuitBreakerError:
            pass

    threads = [threading.Thread(target=worker) for _ in range(50)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # The circuit should have closed eventually
    assert breaker.state == CircuitState.CLOSED

    # The vulnerability: if the circuit allows unlimited requests in HALF_OPEN,
    # allowed_executions will be 50. It SHOULD strictly be the success_threshold (2).
    # If this assertion fails, we have a thundering herd vulnerability.
    assert allowed_executions <= breaker.config.success_threshold, (
        f"Thundering herd vulnerability! Allowed {allowed_executions} requests "
        f"in HALF_OPEN state, but success_threshold is only {breaker.config.success_threshold}."
    )
