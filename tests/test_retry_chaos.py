import math

from taipanstack.resilience.retry import RetryConfig, calculate_delay


def test_retry_chaos_inf_delay():
    """
    Simulate a scenario where max_delay is inf, and jitter is False,
    which will cause calculate_delay to return inf, leading to unbounded
    sleep or ValueError in time.sleep().
    """
    config = RetryConfig(
        initial_delay=float("inf"), max_delay=float("inf"), jitter=False
    )
    delay = calculate_delay(1, config)

    # After our fix, calculate_delay should enforce math.isfinite(delay)
    # and safely downgrade to a maximum allowed finite delay (e.g., config.max_delay if finite)
    # Since config.max_delay is also inf, it should fall back to 0.0 or a safe default.
    assert math.isfinite(delay)
    assert delay >= 0


def test_retry_chaos_nan_delay():
    """
    Simulate a scenario where initial_delay is nan.
    Even though max(0, nan) is 0 in some python versions due to argument order,
    we explicitly enforce math.isfinite to be strictly safe and predictable.
    """
    config = RetryConfig(initial_delay=float("nan"), max_delay=60.0, jitter=False)
    delay = calculate_delay(1, config)

    assert math.isfinite(delay)
    assert delay >= 0


def test_retry_chaos_extreme_negative():
    """
    Ensure negative delays (from time drifts or malicious configs)
    are caught and do not cause exceptions in uniform() if jitter is enabled.
    """
    # If initial delay is negative, and jitter is enabled:
    config = RetryConfig(initial_delay=-100.0, max_delay=60.0, jitter=True)
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)
    assert delay >= 0
