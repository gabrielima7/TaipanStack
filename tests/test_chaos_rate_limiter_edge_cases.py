import math

import pytest

from taipanstack.utils.rate_limit import RateLimiter


def test_rate_limiter_chaos_nan_inf_init() -> None:
    with pytest.raises(ValueError, match="must be finite"):
        RateLimiter(max_calls=math.nan, time_window=10)

    with pytest.raises(ValueError, match="must be finite"):
        RateLimiter(max_calls=10, time_window=math.inf)


def test_rate_limiter_chaos_nan_inf_consume() -> None:
    rl = RateLimiter(max_calls=10, time_window=10)
    assert rl.consume(tokens=math.nan) is False
    assert rl.consume(tokens=math.inf) is False
