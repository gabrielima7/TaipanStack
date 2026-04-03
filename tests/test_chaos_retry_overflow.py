"""Chaos test for retry backoff overflow."""

import pytest

from taipanstack.resilience.retry import RetryConfig, calculate_delay


def test_retry_calculate_delay_overflow_chaos():
    """Simulate extreme attempt number causing OverflowError in exponential backoff.

    If the system is stuck in an endless retry loop, high attempts (e.g., 2000)
    will cause `math.pow` or `**` to overflow, crashing the application.
    The `calculate_delay` function MUST catch this and safely return `max_delay`.
    """
    config = RetryConfig(
        max_attempts=2000,
        initial_delay=1.0,
        max_delay=60.0,
        exponential_base=2.0,
        jitter=False
    )

    # Attempt 2000 will calculate `1.0 * (2.0 ** 1999)`, which overflows float capacity
    # It should gracefully handle the OverflowError and clamp to max_delay (60.0)
    delay = calculate_delay(2000, config)

    assert delay == 60.0, f"Expected 60.0, got {delay}"
