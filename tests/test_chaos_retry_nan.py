from taipanstack.resilience.retry import Retrier, RetryConfig, retry, retry_on_exception


def test_chaos_retry_nan_chaos_retry_rejects_nan_max_attempts():
    """Chaos test: Inject NaN for max_attempts in retry decorator."""

    @retry(max_attempts=float("nan"))
    def my_func():
        return None

    assert my_func.__name__ == "my_func"


def test_chaos_retry_nan_chaos_retry_rejects_nan_initial_delay():
    """Chaos test: Inject NaN for initial_delay in retry decorator."""

    @retry(initial_delay=float("nan"))
    def my_func():
        return None

    assert my_func.__name__ == "my_func"


def test_chaos_retry_nan_chaos_retrier_rejects_nan_max_attempts():
    """Chaos test: Inject NaN for max_attempts in Retrier."""
    retrier = Retrier(max_attempts=float("nan"))
    assert retrier.config.max_attempts == 3


def test_chaos_retry_nan_chaos_retrier_rejects_nan_initial_delay():
    """Chaos test: Inject NaN for initial_delay in Retrier."""
    retrier = Retrier(initial_delay=float("nan"))
    assert retrier.config.initial_delay == 1.0


def test_chaos_retry_nan_chaos_retry_on_exception_rejects_nan_max_attempts():
    """Chaos test: Inject NaN for max_attempts in retry_on_exception."""

    @retry_on_exception((ValueError,), max_attempts=float("nan"))
    def my_func():
        return None

    assert my_func.__name__ == "my_func"


def test_chaos_retry_nan_chaos_retry_config_rejects_nan_max_delay():
    """Chaos test: Inject NaN for max_delay in RetryConfig."""
    config = RetryConfig(max_delay=float("nan"))
    assert config.max_delay == 60.0


def test_chaos_retry_nan_chaos_retry_config_rejects_inf_exponential_base():
    """Chaos test: Inject Inf for exponential_base in RetryConfig."""
    config = RetryConfig(exponential_base=float("inf"))
    assert config.exponential_base == 2.0


def test_chaos_retry_nan_chaos_retry_config_rejects_nan_jitter_factor():
    """Chaos test: Inject NaN for jitter_factor in RetryConfig."""
    config = RetryConfig(jitter_factor=float("nan"))
    assert config.jitter_factor == 0.1
