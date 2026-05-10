from taipanstack.resilience.retry import RetryConfig, _calculate_base_delay

def test_calculate_base_delay_type_mutation():
    config = RetryConfig()
    # Force mutation
    object.__setattr__(config, "initial_delay", "1.0")
    _calculate_base_delay(2, config)
