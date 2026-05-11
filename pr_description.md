## Improvement to Test Coverage

### Description
Proactively improved the test coverage of the `taipanstack` repository by replacing artificial coverage pragmas (`# pragma: no branch`) with genuine test-driven validations.

### Files Modified & Pragmas Addressed
- **`src/taipanstack/core/optimizations.py`**:
  - Removed artificial `# pragma: no branch` for experimental optimization flags check.
  - Test added to ensure the correct output logic is triggered when experimental optimization configurations do not trigger empty skipped lists.
- **`src/taipanstack/security/sanitizers.py`**:
  - Removed `# pragma: no branch` directives in the fallback path logic for `_clean_path_parts`.
  - Tests written (`test_security_sanitizers_path_safe_part_empty` and `test_security_sanitizers_path_part_dot`) to invoke `sanitize_filename` directly bypassing safe branch logic via custom mocking side effect simulating specific edge case unsafe returns like `<bar!>`. Using `Path` correctly allows the same code to run smoothly on both UNIX and Windows, preserving full compatibility!
- Other occurrences were successfully removed as the respective branches were adequately tested but previously suppressed via pragmas unnecessarily (`src/taipanstack/security/guards.py`, `src/taipanstack/security/decorators.py`, `src/taipanstack/resilience/circuit_breaker.py`, `src/taipanstack/resilience/retry.py`, `src/taipanstack/bridges/http_bridge.py`).

### Verification & Pre-flight Steps Taken
- Local test suites verified successfully using `make all`.
- Verified 100% genuine code coverage reporting, handling the cross platform checks!
- Executed `poetry run pytest --cov=src/taipanstack --cov-report=term-missing` validating the full code coverage compliance post pragmas cleanups.
