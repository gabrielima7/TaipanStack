🛡️ Sentinel: [Medium] Fix type mutation and NaN propagation in rate_limit.py

🚨 Severity: Medium
💡 Vulnerability: The token bucket rate limiter in `src/taipanstack/utils/rate_limit.py` was vulnerable to type corruption and `NaN`/`Inf` injection via the `time.monotonic()` delta calculations (`now - self.last_update`). A malicious actor or system anomaly (like a backward NTP clock jump) leading to a `NaN` elapsed time would poison the bucket state, preventing legitimate requests from proceeding.
🎯 Impact: Denial of Service (DoS) due to poisoned bucket tokens. If `time_window` or elapsed time evaluates to `NaN`, subsequent consumption attempts fail closed permanently until the application restarts.
🔧 Fix: Refactored the `_add_tokens` method in `RateLimiter` to securely calculate the `raw_elapsed` time first. We added a strict `math.isfinite(raw_elapsed)` guard before applying the delta or updating `self.last_update`. This ensures the bucket state gracefully handles the corrupted input without failing. Additionally, the existing tests (`test_utils_rate_limit_chaos_nan_inf_time`) were updated to correctly assert the rejection (`False`) on invalid token addition.
✅ Verification: `make all` passes successfully. The 100% test coverage and static analysis (Mypy/Ruff) remain strictly maintained.
