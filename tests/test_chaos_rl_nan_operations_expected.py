import math
import time

import pytest

from taipanstack.utils.rate_limit import RateLimiter


def test_chaos_rl_nan_rate_limiter_chaos_time_corruption_expected(monkeypatch: pytest.MonkeyPatch) -> None:
    limiter = RateLimiter(max_calls=5, time_window=10.0)

    # Empty the bucket
    for _ in range(5):
        assert limiter.consume() is True
    assert limiter.consume() is False

    # Simulate time corruption (NaN)
    monkeypatch.setattr(time, "monotonic", lambda: math.nan)
    assert limiter.consume() is False

    # Restore normal time, fast forward 20 seconds
    # Bucket should normally refill
    monkeypatch.setattr(time, "monotonic", lambda: limiter.last_update + 20.0)

    # If vulnerable, last_update is poisoned with NaN, elapsed becomes NaN,
    # and max(0.0, NaN) is 0.0, so tokens never refill.
    assert limiter.consume() is True, "Rate limiter permanently poisoned by NaN time"


def test_chaos_rl_nan_rate_limiter_chaos_time_corruption_has_tokens_expected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    limiter = RateLimiter(max_calls=5, time_window=10.0)

    # Do not empty the bucket, so it has tokens
    assert limiter.consume() is True
    assert limiter.tokens >= 1.0

    # Simulate time corruption (NaN)
    monkeypatch.setattr(time, "monotonic", lambda: math.nan)

    # Calling consume while time is NaN but bucket has tokens should succeed and deduct a token
    initial_tokens = limiter.tokens
    assert limiter.consume() is True
    assert limiter.tokens == initial_tokens - 1.0


def test_chaos_rl_nan_rate_limiter_chaos_consume_zero_tokens_expected() -> None:
    limiter = RateLimiter(max_calls=5, time_window=10.0)
    assert limiter.consume(tokens=0) is True
    assert limiter.consume(tokens=-1) is True
