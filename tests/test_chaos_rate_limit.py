import time
from unittest import mock

from taipanstack.utils.rate_limit import RateLimiter


def test_rate_limiter_clock_anomaly_chaos():
    """Simulate extreme clock anomalies (NaN, Inf) to test rate limiter resilience."""

    limiter = RateLimiter(max_calls=2, time_window=1.0)

    # Normal consume
    assert limiter.consume() is True
    assert limiter.consume() is True
    assert limiter.consume() is False

    # Inject NaN
    with mock.patch("time.monotonic", return_value=float("nan")):
        # If it doesn't handle NaN properly, it might get stuck or crash
        limiter.consume()

    # Inject Inf
    with mock.patch("time.monotonic", return_value=float("inf")):
        # If it doesn't handle Inf properly, tokens might become Inf
        limiter.consume()

    # Now back to normal time, but tokens might be corrupted (NaN or Inf)
    with mock.patch("time.monotonic", return_value=time.monotonic() + 1.0):
        # We should be able to consume exactly 2 tokens if it recovered,
        # or it might fail if state is corrupted.
        # But we'd need to fix the rate limiter to prevent state corruption
        assert limiter.consume() is True
