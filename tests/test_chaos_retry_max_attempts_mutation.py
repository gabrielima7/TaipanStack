import pytest
from taipanstack.resilience.retry import Retrier

def test_chaos_retry_max_attempts_mutation():
    retrier = Retrier(max_attempts=3)
    # Simulate type mutation using object.__setattr__ to bypass dataclass frozen
    object.__setattr__(retrier.config, "max_attempts", "3")

    # This should not raise TypeError
    retrier._should_retry(ValueError)
