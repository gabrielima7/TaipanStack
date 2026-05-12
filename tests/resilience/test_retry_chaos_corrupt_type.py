import math

import pytest

from taipanstack.resilience.retry import RetryConfig, calculate_delay


def test_calculate_delay_state_corruption():
    # If a config value somehow mutates *after* post_init:
    config = RetryConfig(
        max_attempts=3,
        initial_delay=1.0,
        max_delay=60.0,
        exponential_base=2.0,
        jitter=True
    )

    # Mutate post-init (simulating memory corruption / bad type manipulation)
    object.__setattr__(config, "initial_delay", "string_corruption")

    # calculate_delay should safely fallback without crashing
    try:
        delay = calculate_delay(2, config)
        assert math.isfinite(delay), "Delay should fallback to a safe finite value"
        assert delay >= 0, "Delay should be non-negative"
    except Exception as e:
        pytest.fail(f"calculate_delay crashed on corrupted state: {e}")
