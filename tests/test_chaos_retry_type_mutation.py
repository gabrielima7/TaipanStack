import math

import pytest

from taipanstack.resilience.retry import Retrier


def test_retrier_attempt_type_mutation_graceful_degradation():
    """
    Simulate a rare production failure where the `attempt` state of the Retrier
    gets corrupted/mutated to a non-numeric type (e.g. a string).
    The system should safely degrade by aborting the retry logic
    (letting the exception propagate), rather than crashing with a TypeError.
    """
    retrier = Retrier(max_attempts=3, on=(ValueError,))

    # Intentionally corrupt the state
    retrier.attempt = "corrupted"  # type: ignore[assignment]

    with pytest.raises(ValueError, match="Expected failure"):
        with retrier:
            raise ValueError("Expected failure")


def test_retrier_attempt_nan_mutation_graceful_degradation():
    """
    Simulate a rare production failure where the `attempt` state of the Retrier
    gets corrupted/mutated to NaN (math.nan).
    The system should safely degrade by aborting the retry logic.
    """
    retrier = Retrier(max_attempts=3, on=(ValueError,))

    # Intentionally corrupt the state to NaN
    retrier.attempt = math.nan  # type: ignore[assignment]

    with pytest.raises(ValueError, match="Expected failure"):
        with retrier:
            raise ValueError("Expected failure")
