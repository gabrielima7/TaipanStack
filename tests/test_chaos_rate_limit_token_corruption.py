import math

from taipanstack.utils.rate_limit import RateLimiter


def test_chaos_rate_limit_token_corruption():
    limiter = RateLimiter(10, 1.0)

    # Mutate tokens to NaN
    limiter.tokens = float("nan")

    # Should degrade gracefully or repair itself
    result = limiter.consume(1)

    assert result is True or result is False
    assert not math.isnan(limiter.tokens)
