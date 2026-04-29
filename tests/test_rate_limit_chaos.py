import math
import time
from taipanstack.utils.rate_limit import RateLimiter

def test_rate_limit_chaos_massive_time_jump():
    limiter = RateLimiter(10, 1.0)

    # simulate a massive time jump, producing tokens as infinity
    massive_time = limiter.last_update + 2e308
    limiter._add_tokens(massive_time)

    # It shouldn't be infinity, the system should gracefully handle it.
    assert not math.isinf(limiter.tokens), "Tokens became infinity!"
    assert limiter.tokens <= limiter.capacity, "Tokens exceeded capacity!"

def test_rate_limit_chaos_nan_jump():
    limiter = RateLimiter(10, 1.0)

    # What if time.monotonic() returns NaN? (Mocked by passing float('nan'))
    nan_time = float('nan')
    res = limiter._add_tokens(nan_time)

    # if it fails it should return False
    assert res == False or not math.isnan(limiter.tokens), "Tokens became NaN!"
