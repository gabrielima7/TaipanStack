from taipanstack.resilience.adaptive.adaptive_retry import AdaptiveRetry


def test_adaptive_retry_calculate_delay_metrics_expected():
    ar = AdaptiveRetry()

    # Test empty delays
    assert ar._calculate_delay_metrics([]) == (0.0, 0.0)

    # Test delays list logic
    ar.record_outcome(1, True, 1.0)
    ar.record_outcome(1, True, 2.0)
    ar.record_outcome(1, True, 3.0)

    metrics = ar.metrics
    assert metrics.total_outcomes == 3
    assert metrics.success_rate == 1.0
    assert metrics.avg_delay == 2.0
    assert metrics.p95_delay == 3.0


def test_adaptive_retry_to_retry_config_expected():
    ar = AdaptiveRetry(max_attempts=5, min_delay=0.5, max_delay=10.0)
    # Give it some history for attempt=1 to test get_delay logic in to_retry_config
    ar.record_outcome(1, True, 2.0)
    ar.record_outcome(1, True, 2.0)

    config = ar.to_retry_config()
    assert config.max_attempts == 5
    assert config.initial_delay == 2.0  # median of [2.0, 2.0]
    assert config.max_delay == 10.0
    assert config.jitter is False
