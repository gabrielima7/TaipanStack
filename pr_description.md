# Cyclomatic Complexity Reduction

Modules Refactored:
- src/taipanstack/resilience/retry.py (Retrier._should_retry)
- src/taipanstack/utils/rate_limit.py (RateLimiter._validate_finite)
- src/taipanstack/resilience/adaptive/adaptive_breaker.py (AdaptiveCircuitBreaker.metrics)

Architectural Strategies:
- Extracted validation logic into helper functions to reduce nesting and duplication.
- Reused existing max_attempts calculation helper.

Metrics Impact:
- Significantly reduced McCabe cyclomatic complexity scores for top offending functions.
