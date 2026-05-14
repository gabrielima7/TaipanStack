import pytest

from taipanstack.utils.rate_limit import RateLimiter


def test_rate_limit_chaos_memory_corruption():
    limiter = RateLimiter(max_calls=10, time_window=1.0)

    # 1. Mutate internal state into invalid types
    limiter.time_window = "corrupted"  # type: ignore
    limiter.capacity = "corrupted"  # type: ignore
    limiter.tokens = "corrupted"  # type: ignore
    limiter.last_update = "corrupted"  # type: ignore

    # 2. Try to consume. It should safely degrade, catch TypeError, and reject token consumption.
    try:
        allowed = limiter.consume()
        assert (
            allowed is False
        ), "Rate limiter should reject calls when internal state is corrupted"
    except Exception as e:
        pytest.fail(f"RateLimiter crashed on corrupted state: {e}")
