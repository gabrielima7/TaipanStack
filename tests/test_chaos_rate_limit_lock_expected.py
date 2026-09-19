from taipanstack.utils.rate_limit import RateLimiter, rate_limit


def test_chaos_rate_limit_lock_mutation_expected():
    """Chaos test: Inject a corrupted lock into RateLimiter."""
    limiter = RateLimiter(max_calls=10, time_window=1.0)

    # Mutate lock to raise Exception on acquire
    class BadLock:
        def acquire(self, timeout=-1):
            raise RuntimeError("Corrupted lock state")

        def release(self):
            return None

    limiter._lock = BadLock()

    # Should safely return False instead of crashing
    assert limiter.consume() is False


def test_chaos_rate_limit_lock_decorator_mutation_expected():
    """Chaos test: Check the decorator behavior when lock is corrupted."""

    @rate_limit(max_calls=10, time_window=1.0)
    def my_func() -> str:
        return "success"

    # In python, closure vars aren't directly mutable like this.
    # To test decorator robustness to limiter exception, we can mock it
    # We will test async and sync.
