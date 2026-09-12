from taipanstack.utils.rate_limit import RateLimiter


class ChaosLock:
    def acquire(self, timeout=-1):
        raise ValueError("Chaos acquire failure")

    def release(self):
        pass

def test_chaos_rate_limit_lock_acquire():
    limiter = RateLimiter(10, 1.0)
    limiter._lock = ChaosLock()

    # Should not raise ValueError, should degrade gracefully to False
    result = limiter.consume()
    assert result is False
