import threading
import time

from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
    CircuitState,
)


def test_circuit_breaker_thundering_herd_chaos_expected():
    """Simulate a thundering herd chaos scenario in the HALF_OPEN state.

    If multiple threads hit the HALF_OPEN state simultaneously, they might all
    evaluate `half_open_attempts < success_threshold` to True before any thread
    updates the state. This test verifies that the `HALF_OPEN` state concurrency limits
    properly free up attempt slots upon request completion so the circuit can fully close.
    """
    breaker = CircuitBreaker(failure_threshold=1, success_threshold=2, timeout=0.01)
    breaker._state.state = CircuitState.OPEN
    breaker._state.last_failure_time = time.monotonic() - 1.0
    success_call_count = 0

    @breaker
    def slow_service():
        nonlocal success_call_count
        time.sleep(0.05)
        success_call_count += 1
        return "success"

    results = []
    exceptions = []

    def worker():
        try:
            results.append(slow_service())
        except CircuitBreakerError as e:
            exceptions.append(e)

    threads = [threading.Thread(target=worker) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert breaker.state == CircuitState.CLOSED
    assert success_call_count <= breaker.config.success_threshold
