import time

from taipanstack.utils.rate_limit import RateLimiter


def test_chaos_rate_limit_token_inf_mutation() -> None:
    """Test that RateLimiter handles infinite token mutation gracefully."""
    limiter = RateLimiter(max_calls=5, time_window=10.0)

    # We must ensure _try_consume is reached directly
    limiter.tokens = float("inf")
    result = limiter._try_consume(1.0)
    assert result is False
    assert limiter.tokens == limiter.capacity

    # Mutate tokens to nan
    limiter.tokens = float("nan")
    result = limiter._try_consume(1.0)
    assert result is False
    assert limiter.tokens == limiter.capacity

    # Run through the full consume flow with inf
    limiter.last_update = time.monotonic()
    limiter.tokens = float("inf")
    result = limiter.consume(1.0)
    assert result is False
    assert limiter.tokens == limiter.capacity

    # Run through the full consume flow with nan
    limiter.last_update = time.monotonic()
    limiter.tokens = float("nan")
    result = limiter.consume(1.0)
    assert result is False
    assert limiter.tokens == limiter.capacity
