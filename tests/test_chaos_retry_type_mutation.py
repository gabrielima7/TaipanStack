from taipanstack.resilience.retry import RetryConfig, calculate_delay
import math

def test_calculate_delay_type_mutation() -> None:
    """Test what happens if delay calculation gets incorrect types via state mutation."""
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    # Mutate a property post-init to simulate runtime corruption
    object.__setattr__(config, "initial_delay", "string_mutation")

    # Should not crash, should calculate a fallback delay safely
    delay = calculate_delay(1, config)

    assert math.isfinite(delay)
