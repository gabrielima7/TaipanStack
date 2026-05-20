import math

import pytest

from taipanstack.resilience.retry import Retrier, RetryConfig, calculate_delay


def test_chaos_retry_type_mutation_retrier_attempt_type_mutation_graceful_degradation():
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


def test_chaos_retry_type_mutation_retrier_attempt_nan_mutation_graceful_degradation():
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


def test_chaos_retry_type_mutation_calculate_delay_type_mutation() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "initial_delay", "string_mutation")
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_chaos_retry_type_mutation_calculate_delay_type_mutation_max_delay() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "max_delay", "string_mutation")
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_chaos_retry_type_mutation_calculate_delay_type_mutation_exponential_base() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "exponential_base", "string_mutation")
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_chaos_retry_type_mutation_calculate_delay_type_mutation_jitter_factor() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "jitter_factor", "string_mutation")
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_chaos_retry_type_mutation_calculate_delay_type_mutation_delay_initial_delay() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "initial_delay", "string_mutation")
    object.__setattr__(config, "max_delay", "string_mutation")
    delay = calculate_delay(1, config)
    assert delay == 0.0


def test_chaos_retry_type_mutation_calculate_delay_type_mutation_delay_all_fails() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "initial_delay", "string_mutation")
    object.__setattr__(config, "max_delay", "string_mutation")
    object.__setattr__(config, "exponential_base", "string_mutation")
    delay = calculate_delay(1, config)
    assert delay == 0.0


def test_chaos_retry_type_mutation_calculate_delay_type_mutation_delay_all_fails2() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "initial_delay", "string_mutation")
    object.__setattr__(config, "exponential_base", 1)
    object.__setattr__(config, "max_delay", "string_mutation")
    delay = calculate_delay(1, config)
    assert delay == 0.0


def test_chaos_retry_type_mutation_calculate_delay_type_mutation_delay_all_fails3() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "max_delay", 1.0)
    object.__setattr__(config, "exponential_base", "string_mutation")
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_chaos_retry_type_mutation_calculate_delay_type_mutation_delay_all_fails4() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "max_delay", "string_mutation")
    object.__setattr__(config, "exponential_base", 2.0)
    delay = calculate_delay(1, config)
    assert delay == 0.0


def test_chaos_retry_type_mutation_calculate_delay_type_mutation_delay_all_fails5() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "max_delay", 1.0)
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_chaos_retry_type_mutation_calculate_delay_type_mutation_delay_all_fails6() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "initial_delay", "string_mutation")
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_chaos_retry_type_mutation_apply_jitter_mutation_delay() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "jitter_factor", "string_mutation")
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_chaos_retry_type_mutation_apply_jitter_mutation_delay2() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "jitter_factor", 1.0)
    object.__setattr__(config, "jitter", "string_mutation")
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_chaos_retry_type_mutation_calculate_delay_type_mutation_delay_all_fails7() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "exponential_base", 1)
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_chaos_retry_type_mutation_calculate_delay_type_mutation_delay_all_fails8() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "exponential_base", 2.0)
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_chaos_retry_type_mutation_retry_config_init_type_mutation() -> None:
    config = RetryConfig(
        max_attempts="string_mutation",  # type: ignore
        initial_delay="string_mutation",  # type: ignore
        max_delay="string_mutation",  # type: ignore
        exponential_base="string_mutation",  # type: ignore
        jitter_factor="string_mutation",  # type: ignore
    )
    assert config.max_attempts == 3
    assert config.initial_delay == 1.0
    assert config.max_delay == 60.0
    assert config.exponential_base == 2.0
    assert config.jitter_factor == 0.1
