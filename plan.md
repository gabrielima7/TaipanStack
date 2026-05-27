1. **Explore & Chaos Test Design**: Designed a micro-chaos experiment that corrupts `CircuitBreaker` internal state (`last_failure_time` set to NaN, `timeout` mutated to a string).
2. **Reproduce Crash**: Wrote test in `tests/test_chaos_circuit_breaker.py` to prove that the source code crashes with `ValueError: could not convert string to float: 'corrupted'` instead of gracefully degrading.
3. **Hardening `CircuitBreaker` (`src/taipanstack/resilience/circuit_breaker.py`)**:
   - Modify `_calculate_elapsed_time` to include `try...except (TypeError, ValueError)` block when converting `self.config.timeout` to float, safely falling back to a default timeout (e.g., 30.0).
   - Ensure `isinstance(timeout, (int, float))` checks are robust against mutated configuration.
4. **Test Suite Verification**: Run the entire test suite `poetry run pytest` (including the chaos test). Check that coverage remains at 100%. Ensure no other modules broke.
5. **Pre-commit Steps**: Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.
6. **Submit PR**: Provide a descriptive commit message highlighting the chaos test and the resilience refactoring to avoid system crashes under severe configuration mutations.
