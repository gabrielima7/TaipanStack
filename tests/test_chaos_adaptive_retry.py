import math

import pytest

from taipanstack.resilience.adaptive.adaptive_retry import AdaptiveRetry


def test_adaptive_retry_chaos_nan_inf_propagation() -> None:
    """Simulate extreme time anomalies (NaN, Inf, -Inf) propagating into AdaptiveRetry.

    If an upstream component or a mocked clock bug injects `float('nan')` or
    `float('inf')` into the `elapsed` metric of a successful outcome, the
    internal `statistics.median` or `statistics.mean` will return `NaN` or `inf`.
    This causes `get_delay` to return `NaN` or `inf`, which if passed to `time.sleep`,
    will either crash the application with a ValueError or cause it to sleep forever
    (Denial of Service).
    """
    ar = AdaptiveRetry(min_delay=0.1, max_delay=10.0)

    # Simulate an NTP or system clock anomaly that resulted in NaN or Infinity
    # being passed as the elapsed time.
    ar.record_outcome(attempt=1, success=True, elapsed=float("nan"))
    ar.record_outcome(attempt=1, success=True, elapsed=float("inf"))
    ar.record_outcome(attempt=1, success=True, elapsed=float("-inf"))

    # Also record some valid outcomes to show they get poisoned
    ar.record_outcome(attempt=1, success=True, elapsed=1.5)

    try:
        delay = ar.get_delay(1)
        # Python's min/max with NaN behaves unpredictably depending on order
        # max(0.1, min(nan, 10.0)) usually returns nan.
        assert not math.isnan(delay), (
            "Delay was corrupted to NaN by anomalous time input!"
        )
        assert math.isfinite(delay), (
            "Delay was corrupted to Infinity by anomalous time input!"
        )
        assert 0.1 <= delay <= 10.0, f"Delay {delay} escaped the configured bounds!"
    except Exception as e:
        pytest.fail(f"get_delay crashed due to anomalous time input: {e}")

    # Metrics should also not crash or be poisoned
    try:
        metrics = ar.metrics
        assert not math.isnan(metrics.avg_delay), (
            "Metrics average delay was corrupted to NaN!"
        )
        assert math.isfinite(metrics.avg_delay), (
            "Metrics average delay was corrupted to Infinity!"
        )
        assert not math.isnan(metrics.p95_delay), (
            "Metrics P95 delay was corrupted to NaN!"
        )
    except Exception as e:
        pytest.fail(f"metrics crashed due to anomalous time input: {e}")
