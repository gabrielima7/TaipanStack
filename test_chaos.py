import math
import time

from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState

def test_circuit_breaker_chaos_time_corruption():
    breaker = CircuitBreaker(failure_threshold=1, timeout=10.0)

    # First attempt: failure
    try:
        raise ValueError("failure")
    except ValueError as e:
        breaker._record_failure(e)

    assert breaker._state.state == CircuitState.OPEN

    # Let's say monotonic time gets corrupted or something returns NaN
    import builtins
    original_monotonic = time.monotonic
    time.monotonic = lambda: float('nan')

    try:
        # Check if we should attempt
        attempt = breaker._should_attempt()
        print(f"Should attempt: {attempt}")
    finally:
        time.monotonic = original_monotonic

test_circuit_breaker_chaos_time_corruption()
