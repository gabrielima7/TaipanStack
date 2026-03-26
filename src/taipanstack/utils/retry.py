"""Backward-compatibility shim for the retry module.

This module re-exports all public symbols from the canonical
``taipanstack.resilience.retry`` module. Importing from this path remains
supported for compatibility, but new code should use the canonical module.

.. deprecated::
    Import from ``taipanstack.resilience.retry`` instead.
"""

from taipanstack.resilience.retry import (
    Retrier,
    RetryConfig,
    RetryDecorator,
    RetryError,
    calculate_delay,
    retry,
    retry_on_exception,
)

__all__ = [
    "Retrier",
    "RetryConfig",
    "RetryDecorator",
    "RetryError",
    "calculate_delay",
    "retry",
    "retry_on_exception",
]
