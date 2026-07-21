import pytest

from taipanstack.utils.rate_limit import RateLimiter


def test_rate_limiter_chaos_type_mutation():
    with pytest.raises(TypeError):
        RateLimiter(max_calls="5", time_window=1.0)
    with pytest.raises(TypeError):
        RateLimiter(max_calls=5, time_window="1.0")
