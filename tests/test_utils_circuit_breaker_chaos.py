import contextlib
import threading
import time

import pytest

from taipanstack.utils.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
    CircuitState,
)


def test_circuit_breaker_chaos_thundering_herd_half_open():
    """Simulate a thundering herd on a recovering service in HALF_OPEN state.

    If the circuit is HALF_OPEN, it should only allow a limited number of requests
    (typically `success_threshold`) to test the waters. If it allows an unlimited
    number of concurrent requests, a thundering herd could overwhelm the fragile
    service before it has fully recovered.
    """
    breaker = CircuitBreaker(failure_threshold=1, success_threshold=2, timeout=0.1)

    # 1. Trip the circuit to OPEN
    with contextlib.suppress(ValueError):

        @breaker
        def fail_func():
            raise ValueError("Service unavailable")

        fail_func()

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
        with contextlib.suppress(CircuitBreakerError):
            test_water_func()

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

def test_circuit_breaker_chaos_excluded_exception_half_open_liveness():
    """Verify that an excluded/non-failure exception in HALF_OPEN does not permanently block the circuit.

    If the circuit is HALF_OPEN and a request raises an excluded exception, it shouldn't count
    as a success (it didn't succeed), nor as a failure (it was excluded). It should simply be
    refunded, allowing the circuit to try again. If it is not refunded, the attempts counter
    maxes out and the circuit is permanently bricked in HALF_OPEN.
    """
    breaker = CircuitBreaker(
        failure_threshold=1,
        success_threshold=1,
        timeout=0.1,
        excluded_exceptions=(ValueError,)
    )

    call_count = 0

    @breaker
    def flaky_func():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise TypeError("Real failure") # Trip the circuit
        elif call_count == 2:
            raise ValueError("Excluded failure") # This should NOT brick the circuit
        elif call_count == 3:
            return "success" # Recovery

    # 1. Trip the circuit
    with pytest.raises(TypeError):
        flaky_func()

    assert breaker.state == CircuitState.OPEN

    # Wait for timeout to allow HALF_OPEN transition
    time.sleep(0.15)

    # 2. Trigger the excluded exception (call_count=2)
    with pytest.raises(ValueError):
        flaky_func()

    # The circuit should still be HALF_OPEN because the excluded exception doesn't trip it back to OPEN
    assert breaker.state == CircuitState.HALF_OPEN

    # 3. If the vulnerability existed, this next call would raise CircuitBreakerError
    # because the allowed attempts would have been exhausted by the ValueError.
    # But since it's refunded, we can try again, and it should succeed and CLOSE.
    result = flaky_func()

    assert result == "success"
    assert breaker.state == CircuitState.CLOSED

@pytest.mark.asyncio
async def test_circuit_breaker_chaos_async_excluded_exception_half_open_liveness():
    """Verify that an excluded/non-failure exception in HALF_OPEN does not permanently block the circuit (async)."""
    breaker = CircuitBreaker(
        failure_threshold=1,
        success_threshold=1,
        timeout=0.1,
        excluded_exceptions=(ValueError,)
    )

    call_count = 0

    @breaker
    async def flaky_func():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise TypeError("Real failure")
        elif call_count == 2:
            raise ValueError("Excluded failure")
        elif call_count == 3:
            return "success"

    # 1. Trip the circuit
    with pytest.raises(TypeError):
        await flaky_func()

    assert breaker.state == CircuitState.OPEN

    # Wait for timeout
    time.sleep(0.15)

    # 2. Trigger the excluded exception
    with pytest.raises(ValueError):
        await flaky_func()

    assert breaker.state == CircuitState.HALF_OPEN

    # 3. Verify it's not bricked
    result = await flaky_func()

    assert result == "success"
    assert breaker.state == CircuitState.CLOSED
