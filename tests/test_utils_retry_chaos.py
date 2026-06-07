"""Chaos test for retry calculation resiliency."""

from taipanstack.resilience.retry import RetryConfig, calculate_delay


def test_utils_retry_chaos_retry_chaos_extreme_attempt_standard_expected() -> None:
    """Simulate a severe failure with a huge attempt number.

    A massively large attempt number can cause an OverflowError
    during exponential backoff calculation. The system should gracefully
    fallback to the max delay.
    """
    config = RetryConfig(
        initial_delay=1.0,
        exponential_base=2.0,
        max_delay=60.0,
    )
    # Attempting to calculate delay for a very high attempt number
    # This might throw OverflowError if attempt is huge
    delay = calculate_delay(2000, config)

    # Due to jitter it might be slightly higher than max_delay,
    # but the base delay before jitter should be clamped to max_delay.
    # jitter is uniform(-jitter_amount, jitter_amount), max jitter_factor is 0.1
    # So max possible value is 60.0 * 1.1 = 66.0
    assert delay <= 66.0
    assert delay >= 0.0


def test_utils_retry_chaos_retry_chaos_nan_inf_config_standard_expected() -> None:
    """Simulate NaN or Inf values in the retry configuration.

    If configuration parameters accidentally become NaN or Inf,
    the calculated delay could become NaN, crashing time.sleep() with ValueError,
    or blocking infinitely with Inf.
    """
    import pytest

    with pytest.raises(ValueError, match="finite"):
        RetryConfig(
            initial_delay=float("nan"),
            max_delay=float("inf"),
        )

    # Also test an explicit inf config value
    with pytest.raises(ValueError, match="finite"):
        RetryConfig(
            initial_delay=float("inf"),
            max_delay=60.0,
        )


def test_utils_retry_chaos_coverage_retry_chaos_base_delay_nan_standard_expected() -> None:
    # Test line 121-123.
    # The config now catches this, so we bypass config to hit calculate delay directly.
    config = RetryConfig()
    object.__setattr__(config, "initial_delay", float("nan"))
    object.__setattr__(config, "max_delay", float("nan"))
    delay = calculate_delay(2, config)
    assert delay == 0.0


def test_utils_retry_chaos_coverage_retry_chaos_jitter_exception_2_standard_expected() -> None:
    # Test line 134-140. Jitter exception.
    import pytest

    config = RetryConfig(jitter=True)
    with pytest.MonkeyPatch.context() as m:
        import secrets

        def mock_uniform(*args, **kwargs):
            raise ValueError("Mocked jitter exception")

        m.setattr(secrets.SystemRandom, "uniform", mock_uniform)

        delay = calculate_delay(2, config)
        assert delay == config.initial_delay * config.exponential_base


def test_utils_retry_chaos_coverage_retry_chaos_base_delay_finite_standard_expected() -> None:
    # Test line 122->125 where delay is NOT finite but max_delay IS finite.
    config = RetryConfig(max_delay=60.0, jitter=False)
    object.__setattr__(config, "initial_delay", float("nan"))
    delay = calculate_delay(2, config)
    assert delay == 60.0
