import threading

import pytest

from taipanstack.utils.rate_limit import RateLimiter


def test_chaos_rate_limit_lock_contention_timeout():
    """
    Simulate a rare production failure where the rate limiter's internal lock
    is held indefinitely by a stalled thread.
    The consume method should not hang indefinitely but safely degrade by
    timing out and rejecting the consumption (returning False).
    """
    limiter = RateLimiter(max_calls=10, time_window=1.0)

    # Simulate another thread acquiring the lock and never releasing it
    limiter._lock.acquire()

    success = [None]

    def call_consume():
        success[0] = limiter.consume(1)

    t = threading.Thread(target=call_consume)
    t.start()

    t.join(timeout=0.5)

    if t.is_alive():
        # Release the lock so the thread can finish and the test suite doesn't hang
        limiter._lock.release()
        t.join()
        pytest.fail("RateLimiter.consume() hung indefinitely on lock acquisition")

    assert success[0] is False, (
        "Expected consume to return False when lock acquisition times out"
    )
