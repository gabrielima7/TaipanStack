import threading
import time

from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
    CircuitState,
)


def test_circuit_breaker_thundering_herd_chaos():
    """Simulate a thundering herd chaos scenario in the HALF_OPEN state.

    If multiple threads hit the HALF_OPEN state simultaneously, they might all
    evaluate `half_open_attempts < success_threshold` to True before any thread
    updates the state. This test verifies that the `HALF_OPEN` state concurrency limits
    properly free up attempt slots upon request completion so the circuit can fully close.
    """

    # Configure a breaker that requires 2 successes to close
    breaker = CircuitBreaker(failure_threshold=1, success_threshold=2, timeout=0.01)

    # Force the circuit into OPEN state, then wait for timeout to transition to HALF_OPEN
    breaker._state.state = CircuitState.OPEN
    breaker._state.last_failure_time = (
        time.monotonic() - 1.0
    )  # Guarantee it's passed the timeout

    # We'll use a mocked external service that intentionally sleeps long enough
    # for all threads to evaluate the state before the first thread completes.
    # It always succeeds.
    success_call_count = 0

    @breaker
    def slow_service():
        nonlocal success_call_count
        time.sleep(0.05)  # Crucial: Sleep inside the breaker to simulate latency
        success_call_count += 1
        return "success"

    # Launch multiple threads simultaneously (thundering herd)
    results = []
    exceptions = []

    def worker():
        try:
            results.append(slow_service())
        except CircuitBreakerError as e:
            exceptions.append(e)

    # We want 5 threads. The success threshold is 2.
    threads = [threading.Thread(target=worker) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # We expect the circuit to be CLOSED because at least 2 successes should have occurred.
    assert breaker.state == CircuitState.CLOSED

    # Assert an upper bound. The number of successful calls should be exactly the success threshold
    # or slightly higher depending on the implementation details.
    # We assert <= 5 to ensure that it doesn't run away.
    # The actual implementation currently allows EXACTLY 2 because of the lock in _should_attempt.
    assert success_call_count <= breaker.config.success_threshold
