### SRE Chaos: Rate Limit Type Mutation Hardening

**Target Component:** `src/taipanstack/utils/rate_limit.py` (RateLimiter)
**Property Data Generated:** Malformed subclass types (`EvilFloat` inheriting from `float`) with overridden magic methods (e.g. `__rsub__`, `__truediv__`) that raise `RuntimeError`s during math operations.
**Adjustments Made:** Replaced the permissive `isinstance(var, (int, float))` with strict type checking (`type(var) in (int, float)`). This hardens the token bucket math by aggressively guarding against external state corruption and subclass injections, guaranteeing graceful degradation instead of uncaught exceptions.
