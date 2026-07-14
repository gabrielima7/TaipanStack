import pytest

from taipanstack.utils.rate_limit import RateLimiter, rate_limit


def test_chaos_rate_limit_nan_chaos_rate_limit_nan_execution_success():
    # Micro-chaos on rate_limit.
    # What happens when RateLimiter gets nan max_calls?

    with pytest.raises(ValueError, match="finite numbers"):
        RateLimiter(max_calls=float("nan"), time_window=1.0)

    with pytest.raises(ValueError, match="finite numbers"):
        RateLimiter(max_calls=10, time_window=float("nan"))

    with pytest.raises(ValueError, match="finite numbers"):

        @rate_limit(max_calls=float("inf"), time_window=1.0)
        def my_func():
            return None

        my_func()
