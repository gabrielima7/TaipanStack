import pytest

from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
    CircuitState,
)
from taipanstack.utils.rate_limit import RateLimiter


def test_circuit_breaker_lock_deadlock() -> None:
    cb = CircuitBreaker(failure_threshold=1)

    # Intentionally hold the lock to simulate a crashed or stalled thread
    cb._state.lock.acquire()

    @cb
    def safe_task() -> str:
        return "success"

    # We expect this to fail quickly and safely (via CircuitBreakerError or similar)
    # instead of deadlocking and hanging forever.
    try:
        safe_task()
        pytest.fail("Should not succeed when lock is held")
    except CircuitBreakerError:
        pass
    except Exception as e:
        pytest.fail(f"Failed with unexpected error: {e}")

def test_rate_limit_lock_deadlock() -> None:
    limiter = RateLimiter(max_calls=10, time_window=1.0)

    # Intentionally hold the lock
    limiter._lock.acquire()

    # We expect this to return False quickly instead of deadlocking
    res = limiter.consume(1)
    assert res is False

def test_circuit_breaker_lock_timeout_branches() -> None:
    # We need to trigger the `return` lines when lock acquisition fails (timeout=0.1)
    # The branches are in `_record_success`, `_record_failure`, `reset`, and `_decrement_half_open`
    # We can mock the lock's acquire method to always return False for this test.

    cb = CircuitBreaker(failure_threshold=1)

    # 0. Acquire the lock so that timeout=0.1 fails inside
    cb._state.lock.acquire()

    try:
        # 1. _record_success
        cb._record_success()
        # Should return silently without changing success_count
        assert cb._state.success_count == 0

        # 2. _record_failure
        cb._record_failure(ValueError("test"))
        # Should return silently without changing failure_count
        assert cb._state.failure_count == 0

        # 3. reset
        cb._state.failure_count = 5
        cb.reset()
        # Should not reset since lock failed
        assert cb._state.failure_count == 5

        # 4. _decrement_half_open
        cb._state.state = CircuitState.HALF_OPEN
        cb._state.half_open_attempts = 2
        cb._decrement_half_open(is_half_open=True)
        # Should not decrement since lock failed
        assert cb._state.half_open_attempts == 2
    finally:
        cb._state.lock.release()

        # Should not decrement since lock failed
        assert cb._state.half_open_attempts == 2
