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

    def test_backward_compat_shims_circuit_breaker_shim_exports_expected(
        self,
    ) -> None:
        """Old utils.circuit_breaker path re-exports all symbols."""
        assert CircuitBreaker is not None
        assert CircuitBreakerConfig is not None
        assert CircuitBreakerDecorator is not None
        assert CircuitBreakerError is not None
        assert CircuitBreakerState is not None
        assert CircuitState is not None
        assert circuit_breaker is not None

    def test_backward_compat_shims_circuit_breaker_shim_matches_canonical_expected(
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

    def test_backward_compat_shims_retry_shim_exports_expected(self) -> None:
        """Old utils.retry path re-exports all public retry symbols."""
        assert Retrier is not None
        assert RetryConfig is not None
        assert RetryDecorator is not None
        assert RetryError is not None
        assert calculate_delay is not None
        assert retry is not None
        assert retry_on_exception is not None

    def test_backward_compat_shims_retry_shim_matches_canonical_expected(
        self,
    ) -> None:
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

    def test_backward_compat_shims_resilience_shim_exports_expected(
        self,
    ) -> None:
        """Old utils.resilience path re-exports all public decorator symbols."""
        assert AsyncResultFunc is not None
        assert FallbackDecorator is not None
        assert ResultFunc is not None
        assert TimeoutDecorator is not None
        assert fallback is not None
        assert timeout is not None

    def test_backward_compat_shims_resilience_shim_matches_canonical_expected(
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
