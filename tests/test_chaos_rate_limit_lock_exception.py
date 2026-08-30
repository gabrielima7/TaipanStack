from taipanstack.utils.rate_limit import RateLimiter


def test_rate_limit_lock_acquire_exception():
    limiter = RateLimiter(10, 1.0)

    class BadLock:
        def acquire(self, timeout=-1):
            raise RuntimeError("Chaos lock error")

        def release(self):
            return None

    limiter._lock = BadLock()

    # Should not crash but return False
    limiter.consume()
