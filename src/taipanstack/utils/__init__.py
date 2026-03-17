"""Utility modules for Stack."""

from .cache import cached
from .concurrency import OverloadError, limit_concurrency
from .context import (
    correlation_id_var,
    correlation_scope,
    get_correlation_id,
    set_correlation_id,
)
from .filesystem import ensure_dir, safe_read, safe_write
from .logging import (
    REDACTED_VALUE,
    SENSITIVE_KEY_PATTERNS,
    get_logger,
    log_operation,
    setup_logging,
)
from .rate_limit import RateLimiter, RateLimitError, rate_limit
from .resilience import fallback, timeout
from .retry import Retrier, RetryConfig, RetryError, retry
from .serialization import default_encoder
from .subprocess import SafeCommandResult, run_safe_command  # nosec B404

__all__ = (
    "REDACTED_VALUE",
    "SENSITIVE_KEY_PATTERNS",
    "OverloadError",
    "RateLimitError",
    "RateLimiter",
    "Retrier",
    "RetryConfig",
    "RetryError",
    "SafeCommandResult",
    "cached",
    "correlation_id_var",
    "correlation_scope",
    "default_encoder",
    "ensure_dir",
    "fallback",
    "get_correlation_id",
    "get_logger",
    "limit_concurrency",
    "log_operation",
    "rate_limit",
    "retry",
    "run_safe_command",
    "safe_read",
    "safe_write",
    "set_correlation_id",
    "setup_logging",
    "timeout",
)
