"""
Observability Context Module.

Provides context variables and context managers for tracing and observability,
such as the correlation ID.
"""

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar

__all__ = [
    "correlation_id_var",
    "correlation_scope",
    "get_correlation_id",
    "set_correlation_id",
]

# Context variables for observability
correlation_id_var: ContextVar[str | None] = ContextVar(
    "correlation_id",
    default=None,
)


def get_correlation_id() -> str | None:
    """Get the current correlation ID.

    Returns:
        The correlation ID if set, otherwise None.

    """
    return correlation_id_var.get()


def set_correlation_id(correlation_id: str | None) -> None:
    """Set the correlation ID for the current context.

    Args:
        correlation_id: The correlation ID string, or None to clear.

    """
    correlation_id_var.set(correlation_id)


@contextmanager
def correlation_scope(correlation_id: str | None) -> Iterator[None]:
    """Context manager to set the correlation ID and restore it after.

    Args:
        correlation_id: The correlation ID to set for the duration of the scope.

    Yields:
        None

    """
    token = correlation_id_var.set(correlation_id)
    try:
        yield
    finally:
        correlation_id_var.reset(token)
