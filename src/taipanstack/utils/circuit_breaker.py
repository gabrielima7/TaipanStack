"""Backward-compatibility shim for the circuit breaker module.

This module re-exports all symbols from the canonical
``taipanstack.resilience.circuit_breaker`` module.  Import from this
path continues to work, but new code should import from the canonical
location directly.

.. deprecated::
    Import from ``taipanstack.resilience.circuit_breaker`` instead.
"""

from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitBreakerDecorator,
    CircuitBreakerError,
    CircuitBreakerState,
    CircuitState,
    circuit_breaker,
)

__all__ = [
    "CircuitBreaker",
    "CircuitBreakerConfig",
    "CircuitBreakerDecorator",
    "CircuitBreakerError",
    "CircuitBreakerState",
    "CircuitState",
    "circuit_breaker",
]
