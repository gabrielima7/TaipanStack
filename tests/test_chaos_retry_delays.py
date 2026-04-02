import math

import pytest

from taipanstack.resilience.retry import RetryConfig, RetryError, calculate_delay, retry


def test_calculate_delay_nan_chaos():
    """Simulate NaN configurations in RetryConfig."""
    config = RetryConfig(
        initial_delay=float("nan"),
        max_delay=float("nan"),
        exponential_base=float("nan"),
        jitter=False,
    )
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)
    assert delay >= 0


def test_calculate_delay_inf_chaos():
    """Simulate infinite configurations in RetryConfig."""
    config = RetryConfig(
        initial_delay=float("inf"),
        max_delay=float("inf"),
        exponential_base=float("inf"),
        jitter=False,
    )
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)
    assert delay >= 0


def test_calculate_delay_negative_chaos():
    """Simulate negative configurations in RetryConfig."""
    config = RetryConfig(
        initial_delay=-5.0, max_delay=-10.0, exponential_base=-2.0, jitter=False
    )
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)
    assert delay >= 0


def test_retry_decorator_nan_chaos():
    """Simulate an actual retry decorator experiencing NaN."""

    @retry(initial_delay=float("nan"), max_delay=float("nan"), max_attempts=2)
    def fail_service():
        raise ValueError("boom")

    with pytest.raises(RetryError):
        fail_service()


def test_retry_decorator_inf_chaos():
    """Simulate an actual retry decorator experiencing inf."""

    @retry(initial_delay=float("inf"), max_delay=float("inf"), max_attempts=2)
    def fail_service():
        raise ValueError("boom")

    with pytest.raises(RetryError):
        fail_service()
