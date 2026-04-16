import math
import time

import pytest

from taipanstack.utils.rate_limit import RateLimiter


def test_rate_limiter_chaos_time_corruption_expected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    limiter = RateLimiter(max_calls=5, time_window=10.0)
    for _ in range(5):
        assert limiter.consume() is True
    assert limiter.consume() is False
    monkeypatch.setattr(time, "monotonic", lambda: math.nan)
    assert limiter.consume() is False
    monkeypatch.setattr(time, "monotonic", lambda: limiter.last_update + 20.0)
    assert limiter.consume() is True, "Rate limiter permanently poisoned by NaN time"


def test_rate_limiter_chaos_time_corruption_has_tokens_expected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    limiter = RateLimiter(max_calls=5, time_window=10.0)
    assert limiter.consume() is True
    assert limiter.tokens >= 1.0
    monkeypatch.setattr(time, "monotonic", lambda: math.nan)
    initial_tokens = limiter.tokens
    assert limiter.consume() is True
    assert limiter.tokens == initial_tokens - 1.0


def test_rate_limiter_chaos_consume_zero_tokens_expected() -> None:
    limiter = RateLimiter(max_calls=5, time_window=10.0)
    assert limiter.consume(tokens=0) is True
    assert limiter.consume(tokens=-1) is True
