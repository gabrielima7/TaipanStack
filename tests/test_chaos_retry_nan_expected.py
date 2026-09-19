import pytest

from taipanstack.resilience.retry import Retrier, RetryConfig, retry, retry_on_exception


def test_chaos_retry_nan_chaos_retry_rejects_nan_max_attempts_expected():
    """Chaos test: Inject NaN for max_attempts in retry decorator."""
    with pytest.raises(ValueError, match="finite"):

        @retry(max_attempts=float("nan"))
        def my_func():
            return None


def test_chaos_retry_nan_chaos_retry_rejects_nan_initial_delay_expected():
    """Chaos test: Inject NaN for initial_delay in retry decorator."""
    with pytest.raises(ValueError, match="finite"):

        @retry(initial_delay=float("nan"))
        def my_func():
            return None


def test_chaos_retry_nan_chaos_retrier_rejects_nan_max_attempts_expected():
    """Chaos test: Inject NaN for max_attempts in Retrier."""
    with pytest.raises(ValueError, match="finite"):
        Retrier(max_attempts=float("nan"))


def test_chaos_retry_nan_chaos_retrier_rejects_nan_initial_delay_expected():
    """Chaos test: Inject NaN for initial_delay in Retrier."""
    with pytest.raises(ValueError, match="finite"):
        Retrier(initial_delay=float("nan"))


def test_chaos_retry_nan_chaos_retry_on_exception_rejects_nan_max_attempts_expected():
    """Chaos test: Inject NaN for max_attempts in retry_on_exception."""
    with pytest.raises(ValueError, match="finite"):

        @retry_on_exception((ValueError,), max_attempts=float("nan"))
        def my_func():
            return None


def test_chaos_retry_nan_chaos_retry_config_rejects_nan_max_delay_expected():
    """Chaos test: Inject NaN for max_delay in RetryConfig."""
    with pytest.raises(ValueError, match="finite"):
        RetryConfig(max_delay=float("nan"))


def test_chaos_retry_nan_chaos_retry_config_rejects_inf_exponential_base_expected():
    """Chaos test: Inject Inf for exponential_base in RetryConfig."""
    with pytest.raises(ValueError, match="finite"):
        RetryConfig(exponential_base=float("inf"))


def test_chaos_retry_nan_chaos_retry_config_rejects_nan_jitter_factor_expected():
    """Chaos test: Inject NaN for jitter_factor in RetryConfig."""
    with pytest.raises(ValueError, match="finite"):
        RetryConfig(jitter_factor=float("nan"))
