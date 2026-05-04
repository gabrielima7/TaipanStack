# TaipanStack - Test Refactoring Report

## Insights from `agents.md`
- **100% Real Test Coverage**: Absolute compliance required. Tests must validate real operations and handle edge cases, instead of using `# pragma: no cover`, `contextlib.suppress`, or `pass` to suppress errors silently.
- **Strict Naming Conventions**: Test files must be named logically, mostly ending in `_operations.py` for convention unless testing distinct modules, and all test functions must be strictly descriptive to state their outcome, ending with suffixes like `_returns_ok`, `_returns_err`, `_returns_false`, or explicitly checking raises.
- **LBYL & Clean Error Handling**: The `Result` monad (`Ok`/`Err`) must be used for exceptions when applicable, and tests verify these returns rather than wrapping in standard try/excepts where avoidant behavior is implemented.

## Changes & Refactoring Actions

### Removed Bypasses
- **`test_fuzz_password_operations.py`**: Removed `contextlib.suppress(TypeError, ValueError)` in password hashing and verifying tests, explicitly verifying they do not randomly crash by catching expected exceptions properly and asserting a standard response or failure instead of silencing.
- **`test_fuzz_guard_command_generator_operations.py`**: Rewrote the generator tests to explicitly unpack the return `Ok` output or expect the raised `SecurityError` rather than silently catching it with `pass`.
- **`test_fuzz_guard_null_bytes_operations.py`**: Replaced `contextlib.suppress(SecurityError)` with an explicit outcome test verifying the function executes and either returns safely or explicitly catches `SecurityError`.
- **`test_fuzz_guard_ssrf_operations.py`**: Explicitly ensured the return value (`Ok` or `Err`) of `guard_ssrf` does not unhandled exception crash and properly asserts its return `Result` monad.

### Naming Convention Standardization
Renamed the following files from having non-standard suffixes (like `_expected` or no suffix at all) to strictly include `_operations.py`:
- `tests/test_chaos_bulkhead_resource_exhaustion.py` -> `..._operations.py`
- `tests/test_chaos_concurrency_resource_exhaustion.py` -> `..._operations.py`
- `tests/test_chaos_orchestrator_resource_exhaustion_expected.py` -> `..._operations.py`
- `tests/test_chaos_rate_limit_state_corruption.py` -> `..._operations.py`
- `tests/test_chaos_timeout_resource_exhaustion.py` -> `..._operations.py`
- `tests/test_fuzz_guard_command_generator.py` -> `..._operations.py`
- `tests/test_fuzz_guard_null_bytes.py` -> `..._operations.py`
- `tests/test_fuzz_guard_ssrf.py` -> `..._operations.py`
- `tests/test_fuzz_password_verification.py` -> `..._operations.py`

Correspondingly, rewrote the inner test functions inside these files (e.g., changing `test_bulkhead_semaphore_exhaustion_chaos` to `test_bulkhead_semaphore_exhaustion_chaos_returns_err`) to comply with the standard `test_<module>_<behavior>_<expected_result>` pattern.

## Self-Correction Loop
- Found that fixing test bypass methods initially reduced test coverage because exception blocks were no longer artificially checked when tests were structured properly. Re-introduced a specific explicit error check in the SSRF guard tester to ensure line branches on `guard_ssrf` for exceedingly long URLs (`test_guard_ssrf_exceeds_length_returns_err`) covered the `> MAX_URL_LENGTH` bounds.
- Reconfigured multiple hypothesis fuzz tests to capture the correct outputs to allow `make all` coverage constraints (100%) and formatting limits to pass perfectly with actual assertions without using test bypasses like `pass` and `suppress` and cleaned up artifacts from previous run.
