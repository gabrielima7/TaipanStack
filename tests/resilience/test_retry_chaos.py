import pytest


def test_retry_extreme_jitter_mutation():
    """Simulate a situation where retry delay calculation receives NaN or Inf."""
    import math

    from taipanstack.resilience.retry import RetryConfig

    # Check if RetryConfig correctly rejects NaN initial_delay
    with pytest.raises(ValueError, match="finite"):
        RetryConfig(
            max_attempts=3,
            initial_delay=math.nan,  # type: ignore
            max_delay=60.0,
            exponential_base=2.0,
            jitter=True,
        )
