1. **Understand the Goal**: The task requires daily "micro-chaos" experiment on resilience mechanisms in `taipanstack/utils/circuit_breaker.py`, `retry.py`, `rate_limit.py`, or `resilience.py`. I need to design a highly specific adversarial chaos test (e.g., type mutation), implement it in the `tests/` directory, and refactor the targeted source code to add strict exception handling if it fails.
2. **Current Chaos Test Failure**: The test `test_chaos_circuit_breaker_type_mutation_failure_exceptions` fails. It tests what happens when `cb.config.failure_exceptions` is mutated to a string (`"corrupted"`). When `cb._process_result` or the wrapped function's `try...except` block accesses `self.config.failure_exceptions` which is a string instead of a tuple of exception classes, it will crash.
3. **Refactor `CircuitBreaker`**:
   - `_process_result`: We need to wrap the `isinstance(err_val, self.config.failure_exceptions)` in a try-except block to catch `TypeError` and handle it gracefully (e.g., consider it a failure if the type is corrupted, or default to checking against `Exception`).
   - `_record_failure`: Wrap `isinstance(exc, self.config.excluded_exceptions)` in a try-except to catch `TypeError`.
   - `__call__`: The `try...except self.config.failure_exceptions` block will fail if `failure_exceptions` is not a valid tuple of exceptions. We need to catch `Exception` instead and then check `isinstance` internally. Or we can catch `Exception as e` and then safely evaluate if it's a failure exception. Wait, we can't do `except self.config.failure_exceptions` if it might be corrupted. We should do:
     ```python
     try:
         result = ...
     except Exception as e:
         is_failure = True
         try:
             is_failure = isinstance(e, self.config.failure_exceptions)
         except TypeError:
             pass
         if is_failure:
             self._record_failure(e)
         raise
     ```
     Ah, `CircuitBreakerConfig` is a frozen dataclass, but its fields can be mutated via `object.__setattr__`. This is exactly what the chaos tests simulate.
4. **Implementation Details**:
   - Update `_record_failure` to handle corrupted `excluded_exceptions`.
   - Update `_process_result` to handle corrupted `failure_exceptions`.
   - Update `__call__` async wrapper and sync wrapper to handle corrupted `failure_exceptions` in the `except` block.
5. **Testing**: Run the test suite and verify no regressions.
