import asyncio
import threading
import time

import pytest

from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
    CircuitState,
)


def test_utils_circuit_breaker_chaos_half_open_thundering_herd_chaos_expected():
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

    # Launch 5 threads. The success threshold is 2.
    # The first 2 will be allowed, the remaining 3 will be rejected.
    # We must ensure the allowed ones can finish and successfully close the circuit.
    threads = [threading.Thread(target=worker) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert breaker.state == CircuitState.CLOSED
    assert success_call_count <= breaker.config.success_threshold


def test_utils_circuit_breaker_chaos_half_open_exhaustion_with_system_exit_expected():
    """Simulate uncatchable exception bypassing normal state updates in HALF_OPEN.

    If a thread dies via SystemExit or similar BaseException, the circuit breaker
    MUST release the `half_open_attempts` slot in a finally block so the circuit
    doesn't become permanently stuck in HALF_OPEN.
    """
    breaker = CircuitBreaker(failure_threshold=1, success_threshold=3, timeout=0.01)

    breaker._state.state = CircuitState.OPEN
    breaker._state.last_failure_time = time.monotonic() - 1.0

    @breaker
    def suicidal_service():
        raise SystemExit(0)

    @breaker
    def successful_service():
        return "success"

    # Start the request that will die. It transitions to HALF_OPEN and takes a slot.
    def worker():
        with pytest.raises(SystemExit):
            suicidal_service()

    t = threading.Thread(target=worker)
    t.start()
    t.join()

    # State should be HALF_OPEN. If the slot was NOT freed, it consumed an attempt.
    # Send successful requests. If the slot was consumed, we'd only have 2 left.
    # Since we need 3 successes to close, the circuit would get stuck.
    # But because the slot IS freed, we should be able to send 3 successful requests.

    for _ in range(3):
        assert successful_service() == "success"

    # The circuit should now be closed.
    assert breaker.state == CircuitState.CLOSED


@pytest.mark.asyncio
async def test_utils_circuit_breaker_chaos_async_half_open_exhaustion_with_cancelled_error_expected_expected():
    """Simulate uncatchable exception in async bypassing normal state updates."""
    breaker = CircuitBreaker(failure_threshold=1, success_threshold=3, timeout=0.01)

    breaker._state.state = CircuitState.OPEN
    breaker._state.last_failure_time = time.monotonic() - 1.0

    @breaker
    async def suicidal_service():
        raise asyncio.CancelledError()

    @breaker
    async def successful_service():
        return "success"

    with pytest.raises(asyncio.CancelledError):
        await suicidal_service()

    for _ in range(3):
        assert await successful_service() == "success"

    assert breaker.state == CircuitState.CLOSED
