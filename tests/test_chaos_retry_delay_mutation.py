from taipanstack.resilience.retry import RetryConfig, calculate_delay


def test_chaos_retry_calculate_delay_mutation() -> None:
    config = RetryConfig(max_attempts=3, initial_delay=1.0, max_delay=10.0, exponential_base=2.0, jitter_factor=0.1)

    val = calculate_delay("string", config)  # type: ignore
    assert 0.0 <= val <= 11.0

    object.__setattr__(config, "exponential_base", "string")
    val2 = calculate_delay(1, config)
    assert 0.0 <= val2 <= 11.0

    object.__setattr__(config, "initial_delay", "string")
    val3 = calculate_delay(1, config)
    assert 0.0 <= val3 <= 11.0

def test_chaos_retry_calculate_delay_jitter_mutation() -> None:
    config = RetryConfig(max_attempts=3, initial_delay=1.0, max_delay=10.0, exponential_base=2.0, jitter_factor="string")

    val = calculate_delay(1, config)
    assert 0.0 <= val <= 11.0

def test_chaos_retry_calculate_delay_attempt_mutation() -> None:
    config = RetryConfig(max_attempts=3, initial_delay=1.0, max_delay=10.0, exponential_base=2.0, jitter_factor=0.1)

    val = calculate_delay(None, config)  # type: ignore
    assert 0.0 <= val <= 11.0
