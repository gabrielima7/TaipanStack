## Description

This PR ensures 100% REAL test coverage across the `taipanstack` repository.

### Changes
- Removed multiple `# pragma: no branch` and `# pragma: no cover` comments from `src/taipanstack` files which were masking un-covered branches and lines.
- Updated `pyproject.toml` to remove bypass configuration for test coverage (removed `pragma: no cover` and `pragma: no branch`).
- Added new specific unit tests in `tests/test_very_last_operations.py` that effectively and successfully execute the branches previously ignored by pragmas.
- Ran and confirmed 100% true test coverage using `poetry run pytest --cov=src/taipanstack --cov-report=term-missing`.
- Ran full validation using `make all` ensuring code is fully compliant, securely designed, and maintaining expected behaviors.

### Covered Components
The following components had pragmatic overrides removed and were re-verified to have existing coverage:
- `src/taipanstack/core/optimizations.py`
- `src/taipanstack/resilience/circuit_breaker.py`
- `src/taipanstack/resilience/retry.py`
- `src/taipanstack/security/decorators.py`
- `src/taipanstack/security/guards.py`
- `src/taipanstack/security/sanitizers.py`
- `src/taipanstack/bridges/http_bridge.py`

### Verification
Tests were successfully executed using `make all` returning 100% test coverage with 0 bypassed lines and branches.
