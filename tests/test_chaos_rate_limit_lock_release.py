from taipanstack.utils.rate_limit import RateLimiter


class ChaosLock:
    def acquire(self, timeout=-1):
        return True

    def release(self):
        raise ValueError("Chaos release failure")

def test_chaos_rate_limit_lock_release():
    limiter = RateLimiter(10, 1.0)
    limiter._lock = ChaosLock()

    # Should not raise ValueError
    result = limiter.consume()
    assert result is True or result is False
