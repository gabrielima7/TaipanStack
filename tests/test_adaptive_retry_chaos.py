"""Chaos tests for AdaptiveRetry."""

import pytest

from taipanstack.resilience.adaptive.adaptive_retry import AdaptiveRetry


def test_adaptive_retry_chaos_time_anomalies() -> None:
    """Simulate a chaos scenario where external clock measurements are corrupted.

    If `elapsed` time is recorded as `NaN`, `inf`, or negative due to system clock
    drifts or adversarial manipulation, the AdaptiveRetry should reject these values
    to prevent corrupting the internal statistical delays and causing DoS via
    unbounded `time.sleep()`.
    """
    ar = AdaptiveRetry(min_delay=0.1, max_delay=10.0)

    # Injecting anomalous elapsed times should raise ValueError
    anomalous_times = [float("nan"), float("inf"), float("-inf"), -1.0]

    for bad_time in anomalous_times:
        with pytest.raises(
            ValueError, match="elapsed must be a finite, non-negative number"
        ):
            ar.record_outcome(attempt=1, success=True, elapsed=bad_time)

    # Ensure internal state was not corrupted
    assert ar.get_delay(1) == 0.1  # Fallback exponent backoff (0.1 * 2^0)

    # Valid time should work
    ar.record_outcome(attempt=1, success=True, elapsed=5.0)
    assert ar.get_delay(1) == 5.0
