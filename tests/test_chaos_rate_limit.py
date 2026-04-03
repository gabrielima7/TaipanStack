import math
import time

import pytest

from taipanstack.utils.rate_limit import RateLimiter


def test_rate_limiter_chaos_nan_injection():
    """
    Simulate a rare but severe production failure where the system clock
    returns NaN (Not a Number) due to extreme hardware/OS anomalies.
    The rate limiter should not be permanently bricked by this.
    """
    limiter = RateLimiter(max_calls=1, time_window=1.0)

    # Normal consume
    assert limiter.consume() is True
    assert limiter.tokens == 0.0

    # Inject NaN
    orig_monotonic = time.monotonic
    time.monotonic = lambda: float("nan")
    try:
        # This will either return False or True, but shouldn't crash
        # Prior to fixing, it corrupts the tokens state to NaN
        limiter.consume()
    finally:
        time.monotonic = orig_monotonic

    # Tokens should not be NaN
    assert not math.isnan(limiter.tokens)

    # Advance time normally by 2 seconds
    original_update = limiter.last_update
    # If last_update got corrupted to NaN, we need to fix it in the test to verify recovery,
    # but the fix should prevent last_update from becoming NaN in the first place.
    if math.isnan(limiter.last_update):
        pytest.fail("last_update was corrupted to NaN")

    time.monotonic = lambda: original_update + 2.0
    try:
        # Should have recovered
        assert limiter.consume() is True
    finally:
        time.monotonic = orig_monotonic


def test_rate_limiter_chaos_inf_injection():
    """
    Simulate a time anomaly where the clock jumps to Infinity.
    """
    limiter = RateLimiter(max_calls=1, time_window=1.0)

    # Normal consume
    assert limiter.consume() is True

    # Inject inf
    orig_monotonic = time.monotonic
    time.monotonic = lambda: float("inf")
    try:
        # Tokens might fill up, but shouldn't become inf/NaN in a way that breaks future calls
        limiter.consume()
    finally:
        time.monotonic = orig_monotonic

    assert math.isfinite(limiter.tokens)

    if not math.isfinite(limiter.last_update):
        pytest.fail("last_update was corrupted to inf")

    # Advance time normally
    time.monotonic = lambda: limiter.last_update + 2.0
    try:
        assert limiter.consume() is True
    finally:
        time.monotonic = orig_monotonic


def test_rate_limiter_corrupted_tokens():
    """
    Simulate state corruption where tokens becomes NaN.
    The limiter should recover by resetting tokens to capacity.
    """
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    limiter.tokens = float("nan")
    # Should recover gracefully to max capacity and then be consumed
    assert limiter.consume() is True
    assert not math.isnan(limiter.tokens)


def test_rate_limiter_corrupted_elapsed():
    """
    Simulate state corruption where elapsed calculation becomes NaN.
    The limiter should default elapsed to 0.0.
    """
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    limiter.last_update = float("nan")
    # Should recover gracefully to max capacity and then be consumed
    assert limiter.consume() is True


def test_rate_limiter_chaos_negative_time_jump():
    """
    Simulate a clock that jumps backwards (NTP sync anomaly).
    """
    limiter = RateLimiter(max_calls=1, time_window=1.0)

    # Normal consume
    assert limiter.consume() is True

    # Inject negative time jump
    orig_monotonic = time.monotonic
    time.monotonic = lambda: limiter.last_update - 100.0
    try:
        limiter.consume()
    finally:
        time.monotonic = orig_monotonic

    # State should remain valid
    assert limiter.tokens >= 0.0
    assert math.isfinite(limiter.tokens)

    # Advance time normally
    time.monotonic = lambda: limiter.last_update + 2.0
    try:
        assert limiter.consume() is True
    finally:
        time.monotonic = orig_monotonic
