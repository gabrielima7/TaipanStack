"""Adaptive resilience — self-tuning resilience patterns.

Sub-modules:
    adaptive_breaker: Circuit breaker with auto-tuning thresholds.
    adaptive_retry:   Retry strategy that learns optimal delays.
    bulkhead:         Concurrency isolation via semaphore.
    orchestrator:     Compose patterns into a single pipeline.
"""

from taipanstack.resilience.adaptive.adaptive_breaker import (
    AdaptiveCircuitBreaker,
    AdaptiveMetrics,
)
from taipanstack.resilience.adaptive.adaptive_retry import (
    AdaptiveRetry,
    RetryMetrics,
)
from taipanstack.resilience.adaptive.bulkhead import (
    Bulkhead,
    BulkheadFullError,
)
from taipanstack.resilience.adaptive.orchestrator import ResilienceOrchestrator

__all__ = (
    "AdaptiveCircuitBreaker",
    "AdaptiveMetrics",
    "AdaptiveRetry",
    "Bulkhead",
    "BulkheadFullError",
    "ResilienceOrchestrator",
    "RetryMetrics",
)
