"""Backward-compatibility shim for resilience decorators.

This module re-exports the public decorators and helper types from the canonical
``taipanstack.resilience.resilience`` module. Importing from this path remains
supported for compatibility, but new code should use the canonical module.

.. deprecated::
    Import from ``taipanstack.resilience.resilience`` instead.
"""

from taipanstack.resilience.resilience import (
    AsyncResultFunc,
    FallbackDecorator,
    ResultFunc,
    TimeoutDecorator,
    fallback,
    timeout,
)

__all__ = [
    "AsyncResultFunc",
    "FallbackDecorator",
    "ResultFunc",
    "TimeoutDecorator",
    "fallback",
    "timeout",
]
