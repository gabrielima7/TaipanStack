from unittest.mock import patch

from taipanstack.utils.rate_limit import RateLimiter


def test_rate_limiter_time_anomaly_chaos():
    """Simulate extreme time anomalies (NaN/inf) from clock drift/hardware failure."""
    limiter = RateLimiter(2, 1.0)

    # Drain tokens
    assert limiter.consume() is True
    assert limiter.consume() is True
    assert limiter.consume() is False

    # Inject NaN for time.monotonic - this should be gracefully ignored without state corruption
    with patch("time.monotonic", return_value=float("nan")):
        limiter.consume()

    # Inject Infinity for time.monotonic - this should be gracefully ignored without state corruption
    with patch("time.monotonic", return_value=float("inf")):
        limiter.consume()

    # Now restore normal time but very far in future
    with patch("time.monotonic", return_value=1e10):
        # We should have recovered tokens due to elapsed time, and since state wasn't
        # corrupted by NaN/Inf, this should succeed.
        assert limiter.consume() is True
