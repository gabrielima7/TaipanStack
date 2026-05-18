"""Tests for backward-compatibility shims in taipanstack.utils.

Ensures the old import paths (utils.circuit_breaker, utils.retry,
utils.resilience) still work via re-export shims.
"""

from taipanstack.utils.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitBreakerDecorator,
    CircuitBreakerError,
    CircuitBreakerState,
    CircuitState,
    circuit_breaker,
)
from taipanstack.utils.resilience import (
    AsyncResultFunc,
    FallbackDecorator,
    ResultFunc,
    TimeoutDecorator,
    fallback,
    timeout,
)
from taipanstack.utils.retry import (
    Retrier,
    RetryConfig,
    RetryDecorator,
    RetryError,
    calculate_delay,
    retry,
    retry_on_exception,
)


class TestBackwardCompatShims:
    """Verify backward-compat shims re-export correctly."""

    def test_backward_compat_shims_circuit_breaker_shim_exports(self) -> None:
        """Old utils.circuit_breaker path re-exports all symbols."""
        assert CircuitBreaker is not None
        assert CircuitBreakerConfig is not None
        assert CircuitBreakerDecorator is not None
        assert CircuitBreakerError is not None
        assert CircuitBreakerState is not None
        assert CircuitState is not None
        assert circuit_breaker is not None

    def test_backward_compat_shims_circuit_breaker_shim_matches_canonical(
        self,
    ) -> None:
        """Shim symbols are identical to the canonical resilience module."""
        from taipanstack.resilience.circuit_breaker import (
            CircuitBreaker as CanonicalCB,
        )
        from taipanstack.resilience.circuit_breaker import (
            CircuitState as CanonicalCS,
        )

        assert CircuitBreaker is CanonicalCB
        assert CircuitState is CanonicalCS

    def test_backward_compat_shims_retry_shim_exports(self) -> None:
        """Old utils.retry path re-exports all public retry symbols."""
        assert Retrier is not None
        assert RetryConfig is not None
        assert RetryDecorator is not None
        assert RetryError is not None
        assert calculate_delay is not None
        assert retry is not None
        assert retry_on_exception is not None

    def test_backward_compat_shims_retry_shim_matches_canonical(self) -> None:
        """Retry shim symbols are identical to the canonical module."""
        from taipanstack.resilience.retry import (
            Retrier as CanonicalRetrier,
        )
        from taipanstack.resilience.retry import (
            RetryConfig as CanonicalRetryConfig,
        )
        from taipanstack.resilience.retry import (
            RetryDecorator as CanonicalRetryDecorator,
        )
        from taipanstack.resilience.retry import (
            RetryError as CanonicalRetryError,
        )
        from taipanstack.resilience.retry import (
            calculate_delay as canonical_calculate_delay,
        )
        from taipanstack.resilience.retry import (
            retry as canonical_retry,
        )
        from taipanstack.resilience.retry import (
            retry_on_exception as canonical_retry_on_exception,
        )

        assert Retrier is CanonicalRetrier
        assert RetryConfig is CanonicalRetryConfig
        assert RetryDecorator is CanonicalRetryDecorator
        assert RetryError is CanonicalRetryError
        assert calculate_delay is canonical_calculate_delay
        assert retry is canonical_retry
        assert retry_on_exception is canonical_retry_on_exception

    def test_backward_compat_shims_resilience_shim_exports(self) -> None:
        """Old utils.resilience path re-exports all public decorator symbols."""
        assert AsyncResultFunc is not None
        assert FallbackDecorator is not None
        assert ResultFunc is not None
        assert TimeoutDecorator is not None
        assert fallback is not None
        assert timeout is not None

    def test_backward_compat_shims_resilience_shim_matches_canonical(
        self,
    ) -> None:
        """Resilience shim symbols are identical to the canonical module."""
        from taipanstack.resilience.resilience import (
            AsyncResultFunc as CanonicalAsyncResultFunc,
        )
        from taipanstack.resilience.resilience import (
            FallbackDecorator as CanonicalFallbackDecorator,
        )
        from taipanstack.resilience.resilience import (
            ResultFunc as CanonicalResultFunc,
        )
        from taipanstack.resilience.resilience import (
            TimeoutDecorator as CanonicalTimeoutDecorator,
        )
        from taipanstack.resilience.resilience import (
            fallback as canonical_fallback,
        )
        from taipanstack.resilience.resilience import (
            timeout as canonical_timeout,
        )

        assert AsyncResultFunc is CanonicalAsyncResultFunc
        assert FallbackDecorator is CanonicalFallbackDecorator
        assert ResultFunc is CanonicalResultFunc
        assert TimeoutDecorator is CanonicalTimeoutDecorator
        assert fallback is canonical_fallback
        assert timeout is canonical_timeout


# Migrated from tests/test_chaos_retry_callback_operations.py
import sys

import pytest

from taipanstack.resilience.retry import retry


def test_chaos_retry_callback_retry_chaos_faulty_callback():
    def faulty_callback(attempt, max_attempts, exc, delay):
        raise ValueError("Simulated callback failure")

    @retry(max_attempts=3, on_retry=faulty_callback)
    def failing_service():
        raise RuntimeError("Service failure")

    with pytest.raises(Exception, match="All 3 attempts failed for failing_service"):
        failing_service()

    state = {"calls": 0}

    @retry(max_attempts=3, on_retry=faulty_callback)
    def recovering_service():
        state["calls"] += 1
        if state["calls"] < 2:
            raise RuntimeError("Temporary failure")
        return "success"

    assert recovering_service() == "success"


def test_chaos_retry_callback_retry_chaos_faulty_callback_without_structlog(
    monkeypatch,
):
    monkeypatch.setattr(
        sys.modules["taipanstack.resilience.retry"], "_HAS_STRUCTLOG", False
    )

    def faulty_callback(attempt, max_attempts, exc, delay):
        raise ValueError("Simulated failure without structlog")

    @retry(max_attempts=3, on_retry=faulty_callback)
    def failing_service():
        raise RuntimeError("Service failure")

    with pytest.raises(Exception, match="All 3 attempts failed for failing_service"):
        failing_service()


# Migrated from tests/test_chaos_retry_nan_operations.py

from taipanstack.resilience.retry import Retrier, RetryConfig, retry_on_exception


def test_chaos_retry_rejects_nan_max_attempts():
    """Chaos test: Inject NaN for max_attempts in retry decorator."""
    with pytest.raises(ValueError, match="finite"):

        @retry(max_attempts=float("nan"))
        def my_func():
            return None


def test_chaos_retry_rejects_nan_initial_delay():
    """Chaos test: Inject NaN for initial_delay in retry decorator."""
    with pytest.raises(ValueError, match="finite"):

        @retry(initial_delay=float("nan"))
        def my_func():
            return None


def test_chaos_retrier_rejects_nan_max_attempts():
    """Chaos test: Inject NaN for max_attempts in Retrier."""
    with pytest.raises(ValueError, match="finite"):
        Retrier(max_attempts=float("nan"))


def test_chaos_retrier_rejects_nan_initial_delay():
    """Chaos test: Inject NaN for initial_delay in Retrier."""
    with pytest.raises(ValueError, match="finite"):
        Retrier(initial_delay=float("nan"))


def test_chaos_retry_on_exception_rejects_nan_max_attempts():
    """Chaos test: Inject NaN for max_attempts in retry_on_exception."""
    with pytest.raises(ValueError, match="finite"):

        @retry_on_exception((ValueError,), max_attempts=float("nan"))
        def my_func():
            return None


def test_chaos_retry_config_rejects_nan_max_delay():
    """Chaos test: Inject NaN for max_delay in RetryConfig."""
    with pytest.raises(ValueError, match="finite"):
        RetryConfig(max_delay=float("nan"))


def test_chaos_retry_config_rejects_inf_exponential_base():
    """Chaos test: Inject Inf for exponential_base in RetryConfig."""
    with pytest.raises(ValueError, match="finite"):
        RetryConfig(exponential_base=float("inf"))


def test_chaos_retry_config_rejects_nan_jitter_factor():
    """Chaos test: Inject NaN for jitter_factor in RetryConfig."""
    with pytest.raises(ValueError, match="finite"):
        RetryConfig(jitter_factor=float("nan"))


# Migrated from tests/test_chaos_retry_type_mutation.py
import math

from taipanstack.resilience.retry import calculate_delay


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


def test_calculate_delay_type_mutation() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "initial_delay", "string_mutation")
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_calculate_delay_type_mutation_max_delay() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "max_delay", "string_mutation")
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_calculate_delay_type_mutation_exponential_base() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "exponential_base", "string_mutation")
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_calculate_delay_type_mutation_jitter_factor() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "jitter_factor", "string_mutation")
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_calculate_delay_type_mutation_delay_initial_delay() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "initial_delay", "string_mutation")
    object.__setattr__(config, "max_delay", "string_mutation")
    delay = calculate_delay(1, config)
    assert delay == 0.0


def test_calculate_delay_type_mutation_delay_all_fails() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "initial_delay", "string_mutation")
    object.__setattr__(config, "max_delay", "string_mutation")
    object.__setattr__(config, "exponential_base", "string_mutation")
    delay = calculate_delay(1, config)
    assert delay == 0.0


def test_calculate_delay_type_mutation_delay_all_fails2() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "initial_delay", "string_mutation")
    object.__setattr__(config, "exponential_base", 1)
    object.__setattr__(config, "max_delay", "string_mutation")
    delay = calculate_delay(1, config)
    assert delay == 0.0


def test_calculate_delay_type_mutation_delay_all_fails3() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "max_delay", 1.0)
    object.__setattr__(config, "exponential_base", "string_mutation")
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_calculate_delay_type_mutation_delay_all_fails4() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "max_delay", "string_mutation")
    object.__setattr__(config, "exponential_base", 2.0)
    delay = calculate_delay(1, config)
    assert delay == 0.0


def test_calculate_delay_type_mutation_delay_all_fails5() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "max_delay", 1.0)
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_calculate_delay_type_mutation_delay_all_fails6() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "initial_delay", "string_mutation")
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_apply_jitter_mutation_delay() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "jitter_factor", "string_mutation")
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_apply_jitter_mutation_delay2() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "jitter_factor", 1.0)
    object.__setattr__(config, "jitter", "string_mutation")
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_calculate_delay_type_mutation_delay_all_fails7() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "exponential_base", 1)
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_calculate_delay_type_mutation_delay_all_fails8() -> None:
    config = RetryConfig(initial_delay=1.0, max_attempts=3, max_delay=60.0)
    object.__setattr__(config, "exponential_base", 2.0)
    delay = calculate_delay(1, config)
    assert math.isfinite(delay)


def test_retry_config_init_type_mutation() -> None:
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


# Migrated from tests/test_utils_retry_chaos_coverage_operations.py
import secrets


def test_utils_retry_chaos_coverage_retry_chaos_jitter_nan(
    monkeypatch,
) -> None:
    import pytest

    # Test line 133 -> 139 where math.isfinite(jitter_amount) is False
    with pytest.raises(ValueError, match="finite"):
        RetryConfig(initial_delay=1.0, jitter=True, jitter_factor=float("inf"))


def test_utils_retry_chaos_coverage_retry_chaos_jitter_exception(
    monkeypatch,
) -> None:
    # Test lines 136-137 exception logging
    config = RetryConfig(initial_delay=1.0, jitter=True, jitter_factor=0.1)

    # Monkeypatch secrets.SystemRandom.uniform to raise an Exception
    class FakeRandom:
        def uniform(self, a, b):
            raise ValueError("Simulated exception")

    monkeypatch.setattr(secrets, "SystemRandom", FakeRandom)

    delay = calculate_delay(1, config)
    assert delay == 1.0


def test_utils_retry_chaos_coverage_retry_chaos_delay_negative() -> None:
    # Test line 140 (delay < 0 -> return 0.0)
    config = RetryConfig(initial_delay=-10.0, jitter=False)
    delay = calculate_delay(1, config)
    assert delay == 0.0


def test_utils_retry_chaos_coverage_retry_chaos_jitter_nan_2(
    monkeypatch,
) -> None:
    # Test line 134 -> 140 where math.isfinite(jitter_amount) is False
    config = RetryConfig(initial_delay=1.0, jitter=True)
    object.__setattr__(config, "jitter_factor", float("inf"))
    delay = calculate_delay(1, config)
    assert delay == 1.0


# Migrated from tests/test_utils_retry_chaos_operations.py
"""Chaos test for retry calculation resiliency."""


def test_utils_retry_chaos_retry_chaos_extreme_attempt() -> None:
    """Simulate a severe failure with a huge attempt number.

    A massively large attempt number can cause an OverflowError
    during exponential backoff calculation. The system should gracefully
    fallback to the max delay.
    """
    config = RetryConfig(
        initial_delay=1.0,
        exponential_base=2.0,
        max_delay=60.0,
    )
    # Attempting to calculate delay for a very high attempt number
    # This might throw OverflowError if attempt is huge
    delay = calculate_delay(2000, config)

    # Due to jitter it might be slightly higher than max_delay,
    # but the base delay before jitter should be clamped to max_delay.
    # jitter is uniform(-jitter_amount, jitter_amount), max jitter_factor is 0.1
    # So max possible value is 60.0 * 1.1 = 66.0
    assert delay <= 66.0
    assert delay >= 0.0


def test_utils_retry_chaos_retry_chaos_nan_inf_config() -> None:
    """Simulate NaN or Inf values in the retry configuration.

    If configuration parameters accidentally become NaN or Inf,
    the calculated delay could become NaN, crashing time.sleep() with ValueError,
    or blocking infinitely with Inf.
    """
    import pytest

    with pytest.raises(ValueError, match="finite"):
        RetryConfig(
            initial_delay=float("nan"),
            max_delay=float("inf"),
        )

    # Also test an explicit inf config value
    with pytest.raises(ValueError, match="finite"):
        RetryConfig(
            initial_delay=float("inf"),
            max_delay=60.0,
        )


def test_utils_retry_chaos_coverage_retry_chaos_base_delay_nan() -> None:
    # Test line 121-123.
    # The config now catches this, so we bypass config to hit calculate delay directly.
    config = RetryConfig()
    object.__setattr__(config, "initial_delay", float("nan"))
    object.__setattr__(config, "max_delay", float("nan"))
    delay = calculate_delay(2, config)
    assert delay == 0.0


def test_utils_retry_chaos_coverage_retry_chaos_jitter_exception_2() -> None:
    # Test line 134-140. Jitter exception.
    import pytest

    config = RetryConfig(jitter=True)
    with pytest.MonkeyPatch.context() as m:
        import secrets

        def mock_uniform(*args, **kwargs):
            raise ValueError("Mocked jitter exception")

        m.setattr(secrets.SystemRandom, "uniform", mock_uniform)

        delay = calculate_delay(2, config)
        assert delay == config.initial_delay * config.exponential_base


def test_utils_retry_chaos_coverage_retry_chaos_base_delay_finite() -> None:
    # Test line 122->125 where delay is NOT finite but max_delay IS finite.
    config = RetryConfig(max_delay=60.0, jitter=False)
    object.__setattr__(config, "initial_delay", float("nan"))
    delay = calculate_delay(2, config)
    assert delay == 60.0
