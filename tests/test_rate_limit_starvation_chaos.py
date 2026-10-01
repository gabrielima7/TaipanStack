"""Chaos test for token starvation in RateLimiter."""

import time

import pytest

from taipanstack.utils.rate_limit import RateLimiter


def test_rate_limit_starvation_chaos_transient_corruption(
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """Simulate token starvation due to transient state corruption.

    If `_add_tokens` updates `self.last_update` before fully validating and
    applying the new tokens, a transient error (e.g., state corruption or
    calculation error) will cause the elapsed time to be permanently lost,
    leading to token starvation where the limiter incorrectly stays empty.
    """
    limiter = RateLimiter(max_calls=10, time_window=10.0)

    # Fast-forward time to a stable start point
    current_time = 100.0

    def mock_monotonic() -> float:
        return current_time

    monkeypatch.setattr(time, "monotonic", mock_monotonic)

    # Empty the bucket
    for _ in range(10):
        assert limiter.consume() is True

    assert limiter.consume() is False
    assert limiter.tokens == 0.0

    # Advance time by 5 seconds (enough for 5 tokens)
    current_time += 5.0

    # Simulate a transient state corruption (e.g., config error)
    original_capacity = limiter.capacity
    limiter.capacity = float("nan")

    # Attempt to consume. This will fail because capacity is NaN,
    # but more importantly, it SHOULD NOT advance `last_update`.
    assert limiter.consume() is False

    # Restore the state
    limiter.capacity = original_capacity

    # Advance time slightly more
    current_time += 0.1

    # Attempt to consume again. The limiter should correctly account for
    # the FULL 5.1 seconds that elapsed since the bucket was emptied,
    # adding 5.1 tokens, and allowing the consume to succeed.
    assert limiter.consume() is True
    # If the time was lost, it would only calculate 0.1 seconds elapsed,
    # add 0.1 tokens, and fail the consumption.
    assert limiter.tokens >= 4.0, "Token starvation occurred! Elapsed time was lost."
