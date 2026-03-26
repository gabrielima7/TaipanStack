"""Resilience module for TaipanStack.

Provides circuit breaker, retry, fallback, and timeout patterns
for building resilient applications. This is the canonical home
for all resilience-related utilities.
"""

from taipanstack.resilience.adaptive import (
    AdaptiveCircuitBreaker,
    AdaptiveMetrics,
    AdaptiveRetry,
    Bulkhead,
    BulkheadFullError,
    ResilienceOrchestrator,
    RetryMetrics,
)
from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitBreakerError,
    CircuitBreakerState,
    CircuitState,
    circuit_breaker,
)
from taipanstack.resilience.resilience import fallback, timeout
from taipanstack.resilience.retry import (
    Retrier,
    RetryConfig,
    RetryError,
    calculate_delay,
    retry,
    retry_on_exception,
)
from taipanstack.resilience.watchdogs import (
    BaseWatcher,
    ConfigWatcher,
    HealthPinger,
    HealthTarget,
    ResourceSnapshot,
    ResourceWatcher,
)

__all__ = (
    "AdaptiveCircuitBreaker",
    "AdaptiveMetrics",
    "AdaptiveRetry",
    "BaseWatcher",
    "Bulkhead",
    "BulkheadFullError",
    "CircuitBreaker",
    "CircuitBreakerConfig",
    "CircuitBreakerError",
    "CircuitBreakerState",
    "CircuitState",
    "ConfigWatcher",
    "HealthPinger",
    "HealthTarget",
    "ResilienceOrchestrator",
    "ResourceSnapshot",
    "ResourceWatcher",
    "Retrier",
    "RetryConfig",
    "RetryError",
    "RetryMetrics",
    "calculate_delay",
    "circuit_breaker",
    "fallback",
    "retry",
    "retry_on_exception",
    "timeout",
)
