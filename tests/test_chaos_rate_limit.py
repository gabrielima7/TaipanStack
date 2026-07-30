import threading

from taipanstack.utils.rate_limit import RateLimiter


def test_rate_limiter_lock_contention_chaos():
    limiter = RateLimiter(max_calls=10, time_window=1.0)

    # Simulate a stalled thread holding the lock
    limiter._lock.acquire()

    result = []

    def try_consume():
        res = limiter.consume(1)
        result.append(res)

    t = threading.Thread(target=try_consume)
    t.start()
    t.join(timeout=0.5)

    assert not t.is_alive(), "consume() hung indefinitely due to lock contention"
    assert result == [False], "consume() should fail safely when lock is contested"

    limiter._lock.release()
