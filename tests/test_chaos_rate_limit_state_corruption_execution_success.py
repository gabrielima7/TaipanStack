from taipanstack.utils.rate_limit import RateLimiter


def test_chaos_rate_limit_state_corruption_returns_false_execution_success():
    """Simulate extreme state corruption in RateLimiter.

    If memory or state gets corrupted such that `time_window` is 0.0,
    the limiter should gracefully reject (fail closed) rather than crash
    with a ZeroDivisionError. Similarly, NaN and Inf capacities should be
    rejected safely.
    """
    limiter = RateLimiter(10, 10.0)

    # Chaos: Corrupt time_window to 0.0
    object.__setattr__(limiter, "time_window", 0.0)
    assert limiter.consume() is False

    # Chaos: Corrupt time_window to NaN
    object.__setattr__(limiter, "time_window", float("nan"))
    assert limiter.consume() is False

    # Chaos: Corrupt capacity to NaN
    limiter = RateLimiter(10, 10.0)
    object.__setattr__(limiter, "capacity", float("nan"))
    assert limiter.consume() is False

    # Chaos: Corrupt capacity to Inf
    object.__setattr__(limiter, "capacity", float("inf"))
    assert limiter.consume() is False

    # Chaos: Corrupt tokens to NaN
    limiter = RateLimiter(10, 10.0)
    object.__setattr__(limiter, "tokens", float("nan"))
    assert limiter.consume() is False
