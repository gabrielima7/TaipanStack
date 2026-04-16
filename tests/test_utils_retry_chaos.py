"""Chaos test for retry calculation resiliency."""

import math

from taipanstack.resilience.retry import RetryConfig, calculate_delay


def test_retry_chaos_extreme_attempt_expected() -> None:
    """Simulate a severe failure with a huge attempt number.

    A massively large attempt number can cause an OverflowError
    during exponential backoff calculation. The system should gracefully
    fallback to the max delay.
    """
    config = RetryConfig(initial_delay=1.0, exponential_base=2.0, max_delay=60.0)
    delay = calculate_delay(2000, config)
    assert delay <= 66.0
    assert delay >= 0.0


def test_retry_chaos_nan_inf_config_expected() -> None:
    """Simulate NaN or Inf values in the retry configuration.

    If configuration parameters accidentally become NaN or Inf,
    the calculated delay could become NaN, crashing time.sleep() with ValueError,
    or blocking infinitely with Inf.
    """
    config = RetryConfig(initial_delay=float("nan"), max_delay=float("inf"))
    delay = calculate_delay(2, config)
    assert math.isfinite(delay)
    assert delay >= 0.0
    config_inf = RetryConfig(initial_delay=float("inf"), max_delay=60.0)
    delay_inf = calculate_delay(2, config_inf)
    assert math.isfinite(delay_inf)
    assert delay_inf >= 0.0
    assert delay_inf <= 66.0
