# 🛡️ Sentinel: [Low] Fix cyclomatic complexity

## 🚨 Severity
Low

## 💡 Vulnerability
High cyclomatic complexity in `CircuitBreaker` and `Retrier` modules makes the code harder to test, maintain, and understand, violating Clean Code and SOLID principles. Also, the integration tests were failing due to unresolved version conflicts with the `cyclonedx-python-lib` dependency in `taipanstack_bootstrapper.py`.

## 🎯 Impact
Reduced technical debt and improved code maintainability without altering public API behavior. Integration pipeline is now fixed.

## 🔧 Fix
- Extracted nested logic in `CircuitBreaker._record_failure` into a dedicated helper `_get_failure_state_change`.
- Extracted logic in `CircuitBreaker._decrement_half_open` into a helper `_do_decrement_half_open`.
- Extracted logic in `retry.py`'s `_apply_jitter` into a helper `_do_apply_jitter`.
- Refactored `Retrier.__exit__` by extracting exception and attempt evaluation into `_is_retryable_exception` and `_should_retry_attempt`.
- Pinned `cyclonedx-python-lib>=11.7.0,<12.0.0` within `dev_deps` array in `taipanstack_bootstrapper.py` to fix pip-audit conflicts in CI.

## ✅ Verification
- 100% test coverage maintained.
- Linter and type checker passed.
- Cyclomatic complexity reduced across the modified modules.
- Bootstrapper resolves dependencies appropriately without conflicts.
