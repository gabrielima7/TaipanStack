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


def test_calculate_delay_nan_chaos_with_jitter_negative_result():
    """Simulate NaN jitter that results in a negative outcome or similar fallback."""
    config = RetryConfig(
        initial_delay=1.0,
        max_delay=60.0,
        exponential_base=2.0,
        jitter=True,
        jitter_factor=float("nan"),
    )
    # the function falls back to 0.1 for jitter_factor, so delay shouldn't be negative here.
    # to hit line 151 (`return 0.0`), we need `delay` to be non-finite or < 0
    # Let's mock uniform to force a very negative delay
    import unittest.mock
    with unittest.mock.patch("secrets.SystemRandom.uniform", return_value=-1000.0):
        delay = calculate_delay(1, config)
        assert delay == 0.0


def test_calculate_delay_inf_chaos_with_jitter():
    """Simulate Infinity jitter configurations in RetryConfig."""
    config = RetryConfig(
        initial_delay=1.0,
        max_delay=60.0,
        exponential_base=2.0,
        jitter=True,
        jitter_factor=float("inf"),
    )
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)
    assert delay >= 0


def test_calculate_delay_nan_chaos_override():
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
