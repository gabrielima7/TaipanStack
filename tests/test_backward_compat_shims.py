"""Tests for backward-compatibility shims in taipanstack.utils.

Ensures the old import paths (utils.circuit_breaker, utils.retry,
utils.resilience) still work via re-export shims.
"""

from taipanstack.utils.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitBreakerError,
    CircuitBreakerState,
    CircuitState,
    circuit_breaker,
)


class TestBackwardCompatShims:
    """Verify backward-compat shims re-export correctly."""

    def test_circuit_breaker_shim_exports(self) -> None:
        """Old utils.circuit_breaker path re-exports all symbols."""
        assert CircuitBreaker is not None
        assert CircuitBreakerConfig is not None
        assert CircuitBreakerError is not None
        assert CircuitBreakerState is not None
        assert CircuitState is not None
        assert circuit_breaker is not None

    def test_circuit_breaker_shim_matches_canonical(self) -> None:
        """Shim symbols are identical to the canonical resilience module."""
        from taipanstack.resilience.circuit_breaker import (
            CircuitBreaker as CanonicalCB,
        )
        from taipanstack.resilience.circuit_breaker import (
            CircuitState as CanonicalCS,
        )

        assert CircuitBreaker is CanonicalCB
        assert CircuitState is CanonicalCS
