## Daily Micro-Chaos Resilience Hardening: `taipanstack.resilience.retry`

### Target Component
The `RetryConfig` validation and `_calculate_base_delay` method within `src/taipanstack/resilience/retry.py`.

### Simulated Failure
Simulated a state/type corruption where an internal configuration property (e.g. `initial_delay`, `max_attempts`) is mutated into a non-numeric type (e.g., a `string`) at runtime. This causes type exceptions like `TypeError` during mathematical delay calculations, which previously crashed the retry mechanism entirely instead of safely degrading or logging the error.

### Code Adjustments Made
- **Test Addition:** Added `test_chaos_retry_type_mutation.py` to assert that `calculate_delay` handles state mutation types securely without crashing and correctly calculates a fallback delay. Tests explicitly run `calculate_delay(1, config)` and check the output value, verifying that it degrades gracefully.
- **Config Validation Fallback:** Updated `RetryConfig.__post_init__` to gracefully handle incorrect configuration types by catching `TypeError`s individually and overriding them with default finite values instead of completely resetting the whole configuration or throwing errors.
- **Graceful Calculation Degradation:** Refactored `_calculate_base_delay` and `_apply_jitter` using `try..except (TypeError, OverflowError)` to gracefully fall back to `0.0` or `config.max_delay` when calculating exponential delays on potentially mutated types, preventing fatal `TypeError`s like "can't multiply sequence by non-int of type 'float'".

### Verification
All tests run with 100% coverage, maintaining architectural rules, strict typing, and benchmark thresholds. Leftover python script files used for editing code have been removed.
