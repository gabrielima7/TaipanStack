from taipanstack.resilience.retry import RetryConfig


def test_chaos_retry_config_exceptions_fallback() -> None:
    """Test that RetryConfig falls back to default values instead of raising ValueError."""
    # Attempt to initialize with invalid, negative, and infinite values
    config = RetryConfig(
        max_attempts=-1,
        initial_delay=float("inf"),
        max_delay=-100.0,
        exponential_base=float("nan"),
        jitter_factor=-0.5,
    )

    # Assert values fallback correctly to their defaults
    assert config.max_attempts == 3
    assert config.initial_delay == 1.0
    assert config.max_delay == 60.0
    assert config.exponential_base == 2.0
    assert config.jitter_factor == 0.1
