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


def test_chaos_retry_type_mutation_calculate_delay_type_mutation_exponential_base() -> (
    None
):
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "exponential_base", "string_mutation")
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_chaos_retry_type_mutation_calculate_delay_type_mutation_jitter_factor() -> (
    None
):
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "jitter_factor", "string_mutation")
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_chaos_retry_type_mutation_calculate_delay_type_mutation_delay_initial_delay() -> (
    None
):
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "initial_delay", "string_mutation")
    object.__setattr__(config, "max_delay", "string_mutation")
    delay = calculate_delay(1, config)
    assert delay == 0.0


def test_chaos_retry_type_mutation_calculate_delay_type_mutation_delay_all_fails() -> (
    None
):
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "initial_delay", "string_mutation")
    object.__setattr__(config, "max_delay", "string_mutation")
    object.__setattr__(config, "exponential_base", "string_mutation")
    delay = calculate_delay(1, config)
    assert delay == 0.0


def test_chaos_retry_type_mutation_calculate_delay_type_mutation_delay_all_fails2() -> (
    None
):
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "initial_delay", "string_mutation")
    object.__setattr__(config, "exponential_base", 1)
    object.__setattr__(config, "max_delay", "string_mutation")
    delay = calculate_delay(1, config)
    assert delay == 0.0


def test_chaos_retry_type_mutation_calculate_delay_type_mutation_delay_all_fails3() -> (
    None
):
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "max_delay", 1.0)
    object.__setattr__(config, "exponential_base", "string_mutation")
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_chaos_retry_type_mutation_calculate_delay_type_mutation_delay_all_fails4() -> (
    None
):
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "max_delay", "string_mutation")
    object.__setattr__(config, "exponential_base", 2.0)
    delay = calculate_delay(1, config)
    assert delay == 0.0


def test_chaos_retry_type_mutation_calculate_delay_type_mutation_delay_all_fails5() -> (
    None
):
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "max_delay", 1.0)
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_chaos_retry_type_mutation_apply_jitter_mutation_delay2() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "jitter_factor", 1.0)
    object.__setattr__(config, "jitter", "string_mutation")
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_chaos_retry_type_mutation_calculate_delay_type_mutation_delay_all_fails7() -> (
    None
):
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "exponential_base", 1)
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_chaos_retry_type_mutation_calculate_delay_type_mutation_delay_all_fails8() -> (
    None
):
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


def test_chaos_retry_on_exception() -> None:
    from taipanstack.resilience.retry import RetryError, retry_on_exception

    @retry_on_exception((ValueError,), max_attempts=2)
    def test_func_standard():
        raise ValueError("test")

    with pytest.raises(RetryError):
        test_func_standard()


def test_chaos_retry_exit_should_retry_false_due_to_none_exc_val() -> None:
    # Coverage for `self.last_exception = exc_val if isinstance(exc_val, Exception) else None`
    # When exc_val is None (or not Exception, like BaseException).
    r = Retrier()

    class CustomExc(BaseException):
        def __init__(self):
            super().__init__("custom")

    with pytest.raises(CustomExc):
        with r:
            raise CustomExc()


def test_chaos_retry_exit_success() -> None:
    r = Retrier()
    r.__exit__(None, None, None)


def test_chaos_retry_should_retry_type_error_for_issubclass() -> None:
    """
    Test the try...except TypeError block for issubclass inside _should_retry.
    """
    r = Retrier()

    # Pass an object instead of a type to trigger TypeError in issubclass
    class InvalidExc:
        def __init__(self):
            self.invalid = True

    assert r._should_retry(InvalidExc()) is False


@pytest.mark.asyncio
async def test_chaos_retry_decorator_type_error_for_isinstance() -> None:
    """
    Test the try...except TypeError block for isinstance inside the retry decorator.
    """
    from taipanstack.resilience.retry import retry

    @retry(max_attempts=2, on=ValueError)
    async def async_fail():
        raise ValueError("async fail")

    @retry(max_attempts=2, on=ValueError)
    def sync_fail():
        raise ValueError("sync fail")

    class TypeErrorRaiserMeta(type):
        def __instancecheck__(cls, instance):
            raise TypeError("Chaos injected TypeError")

    class TypeErrorRaiserError(Exception, metaclass=TypeErrorRaiserMeta):
        """Custom exception to inject TypeError on instancecheck"""

    @retry(max_attempts=2, on=TypeErrorRaiserError)
    async def async_fail2():
        raise ValueError("async fail")

    @retry(max_attempts=2, on=TypeErrorRaiserError)
    def sync_fail2():
        raise ValueError("sync fail")

    with pytest.raises(ValueError, match="async fail"):
        await async_fail2()

    with pytest.raises(ValueError, match="sync fail"):
        sync_fail2()
