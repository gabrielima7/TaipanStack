# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.9] - 2026-03-11

### Security
- **Critical**: Patched path traversal vulnerabilities in filesystem utilities (#160).
- **Masking**: Added automatic sensitive data masking in structured logs (#162).
- **Types**: Implemented `SafeHtml` and `SafeSqlIdentifier` natively compatible with FastAPI/Pydantic schemas.
- **JWT**: Disallowed 'none' algorithm in JWT decoding (#169).
- **Optimization**: Unified sensitive environment variable patterns (#167).

### Core Features
- **Observability**: Added `correlation_id` tracking via `contextvars` integrating distributed tracing into `structlog`.
- **Resilience**: New `@fallback` and `@timeout` decorators for safe error interception and execution timeouts.
- **Cache**: New `@cached(ttl)` decorator that memoizes only successful results (`Ok`).

### QA / Testing
- **Robustness**: Stabilized concurrency tests using event-based synchronization (#165).
- **Coverage**: Added new test cases for path sanitization, SQL identifiers, and long file extensions (#168, #166, #163, #159).

### Performance
- **Hashing**: Optimized file hashing chunk iteration using `functools.partial` (#164).

### Refactoring
- **Chore**: Removed unnecessary elif branches (#161).
- **Observability**: Padronized logging infrastructure using internal utilities (#162).

## [0.3.8] - 2026-03-10

### Added
- **Resilience**: New Bulkhead Pattern decorator `@limit_concurrency` using thread and async semaphores with timeouts avoiding overload cascades.
- **Security/Observability**: Native integration of `SecureBaseModel` built on top of Pydantic v2 and `structlog` automatically redacting internal model sensitive data upon dumping logic.
- **Serialization**: Native `orjson` default encoding via `default_encoder` directly translating `<Ok/Err>` outputs natively to optimized JSON.
- **Resilience**: Complete strict-typed First-Class Native Async (`async def`) execution coverage inside the `@rate_limit` token-bucket decorator.

### Performance
- **Security Guards**: Implemented O(N) regex evaluation for path traversal patterns, replacing sequential loop checks for better throughput (#156).
- **Logging**: Optimized sensitive key masking in structured logs with pre-compiled regex mapping (#157).

### Refactoring
- **Pre-commit**: Modularized the pre-commit configuration generator with better isolation and dedicated unit tests (#158).

### QA / Testing
- **Filesystem**: Expanded security coverage for `get_file_hash` and `ensure_dir` path traversal guards (#153, #154).
- **Resilience**: Added explicit edge-case validation for `retry_on_exception` wrapper (#155).

## [0.3.7] - 2026-03-09

### Security
- **Critical**: Patched path traversal bypass via symlink resolution in `guard_path_traversal` (PR #150).

### Performance
- **Security Guards**: Optimized `guard_path_traversal` by pre-computing lowercase path strings and refactoring traversal pattern lookups (PR #145).
- **Decorators**: Implemented `inspect.signature` caching in `@validate_inputs` and `@require_type` decorators to reduce overhead on frequent calls (PR #143).

### QA / Testing
- **Coverage**: Added rigorous test cases for `normalize_ext` in `guard_file_extension` to ensure secure handling of mixed-case extensions (PR #147).
- **Robustness**: Enhanced `check_command_exists` to gracefully handle `None` or empty string inputs with automated test verification (PR #146).

### Refactoring
- **Resilience**: Unified `RetryError` escalation logic into a centralized internal helper to improve maintainability of retry decorators (PR #141).

## [0.3.6] - 2026-03-05

### QA / Testing
- **Async Wrapper**: Comprehensive `pytest.mark.asyncio` testing for `@retry`, `circuit_breaker`, and `@safe` with 100% coverage guarantees.
- **Validations**: Added tests for inner guards logic (`normalize_ext`) and configuration validations (`validate_project_dir`).

### Security
- **Critical Fix**: Patched critical symlink path traversal bypass in `guard_path_traversal`.
- **JWT**: Resolved `InsecureKeyLengthWarning` in JWT test suites with upgraded 32-byte minimum limits.

### Code Health & Refactoring
- **Lint & Types**: Resolved MyPy strict typing (`overload` protocols), Bandit security warnings (`B404`, `B603`), and Ruff lintings (`E501`, `F811`).
- **Maintainability**: Unified test suite retry logging parameter scopes into a resilient testing environment.

## [0.3.5] - 2026-03-04

### Changed
- **Release**: Re-release of `v0.3.4` contents as `v0.3.5` — the original `v0.3.4` tag was accidentally published to PyPI in an incomplete state. Since PyPI does not allow overwriting existing versions, this patch release contains the exact same intended changes as `v0.3.4`.

## [0.3.4] - 2026-03-04

### Security
- **Critical**: Fixed plaintext password storage in `UserService.create_user` — passwords are now hashed before being stored (PR #93)
- **New**: `taipanstack.security.password` module with `hash_password`, `verify_password`, and `generate_secure_token` functions

### Added
- **Resilience**: Native `async def` support for `@retry` and `@circuit_breaker` using `inspect.iscoroutinefunction` and exact `@overload` type hints.
- **Security**: New Pydantic v2 compatible validation types (`SafeUrl`, `SafePath`, `SafeCommand`, `SafeProjectName`) in `taipanstack.security.types`.
- **Observability**: New `mask_sensitive_data_processor` for `structlog` to automatically intercept and redact sensitive keys (password, token, etc.).
- **Security**: New `src/taipanstack/security/password.py` module with bcrypt-based hashing, constant-time verification, and cryptographically secure token generation
- **Test/Security**: Tests for the new `password` module (`tests/test_security_password.py`)
- **Test/Validators**: `test_invalid_ip_rejected` now verifies exception chaining (`exc_info.value.__cause__`) for `validate_ip_address` (PR #128)
- **Test/Validators**: `validate_url` now explicitly evaluates `.port` attribute to catch lazy `urlparse` evaluation for out-of-range ports (PRs #115, #126)
- **Test/Validators**: Coverage for `validate_port` with non-int strings and large integer strings exceeding CVE-2020-10735 limits (PR #114)
- **Test/Coverage**: `get_optimization_level` now has test coverage for integer string size limit (CVE-2020-10735) edge case (PR #129)
- **Test/Result**: `@safe` and `@safe_from` decorators now have explicit tests for base `Exception` catching (PRs #127, #117)
- **Test/Result**: `safe_from` has test for explicitly raised `ValueError` (PR #119)
- **Test/Logging**: `log_operation` has coverage for `expected_exceptions` catching and re-raising (PR #116)
- **Test/Filesystem**: Path traversal `SecurityError` without `base_dir` now covered in `safe_read`, `safe_write`, `ensure_dir`, `safe_delete` (PR #120)

### Changed
- **Performance**: `generate_pre_commit_config` now uses list accumulation + `"".join()` instead of string `+=` concatenation — ~10–15% faster on large configs (PR #130)
- **Code Health**: Removed unused `compat` imports (`PY311`, `PY312`, `PY313`, `PY314`, `PY_VERSION`, `PythonFeatures`, `VersionTier`, etc.) from `taipanstack.core` public API (PR #99)
- **Code Health**: Removed unused imports from root `taipanstack/__init__.py` (PR #100)
- **Code Health**: `utils/__init__.py` now defines proper `__all__` to control public API and fix unused-import lint errors (PR #98)
- **Code Health**: Removed redundant `from __future__ import annotations` across multiple files (PR #112)
- **Code Health**: Preserved valid config package public API exports in `taipanstack.config.__init__` (PR #102)
- **Test/SSRF**: `test_unresolvable_hostname_returns_err` updated to use platform-independent `gaierror` mocking and assert value truncation (PR #122)

### Fixed
- **CI**: Added `zypper removerepo repo-openh264 || true` before package install on openSUSE Leap runners (PR #116 related)
- **Dependencies**: Bumped GitHub Actions group (`actions/checkout`, `actions/setup-python`, etc.) to latest versions (PR #95)

## [0.3.3] - 2026-03-03

### Added
- **Core/Result**: `@safe` decorator now supports `async def` functions — wraps coroutines so that `await safe_fn()` returns `Result[T, Exception]` instead of raising. Uses `inspect.iscoroutinefunction` internally and two `@overload` signatures to preserve precise type narrowing in mypy/pyright strict mode.
- **Security**: `guard_ssrf(url)` function in `security.guards` — parses the URL, resolves the hostname via DNS, and blocks requests to private/loopback/link-local/reserved IP ranges (RFC-1918, `127.0.0.0/8`, `169.254.0.0/16` AWS metadata, IPv6 ULA/loopback). Returns `Err(SecurityError)` on SSRF detection; raises `TypeError` on non-string input.
- **Resilience**: `@retry` now emits a structured `structlog.warning("retry_attempted", ...)` automatically on each retry attempt when no `on_retry` callback is provided and `structlog` is installed. Degrades gracefully to nothing when structlog is absent.
- **Resilience**: `CircuitBreaker._notify_state_change` now emits a structured `structlog.warning("circuit_state_changed", ...)` automatically on every state transition when no `on_state_change` callback is set and `structlog` is installed.
- **QA**: `pytest-asyncio` added to dev dependencies (`asyncio_mode = "auto"` configured in `pyproject.toml`).
- **Docs**: New `docs/patterns/security.md` — practical guide combining `@safe`, `@guard_ssrf`, `@guard_path_traversal`, and `@retry` in a FastAPI endpoint example.

### Changed
- **Performance**: Optimized `guard_command_injection` by combining string type validation and dangerous pattern check into a single loop, improving execution time by ~5% (PR #80).
- **Refactoring**: Simplified `validate_project_name` by decomposing complex logic into smaller, independent private helpers (`_validate_type`, `_check_project_name_chars`, etc.) (PR #79).
- **QA/Mutation**: `[tool.mutmut]` `paths_to_mutate` expanded to include `security/validators.py` and `security/guards.py`; `tests_dir` updated correspondingly.

## [0.3.2] - 2026-03-02

### Added
- **Docs**: MkDocs Material documentation portal
- **Docs**: Comprehensive API Reference and Architecture portal integration

### Changed
- **Performance/CI**: Raised performance regression threshold to 150% in `benchmark-action`

### Fixed
- **Docs**: Corrected accessibility bugs (axe-core warnings), missing `labels`, and replaced `autocapitalize`
- **Security**: Fixed potential XSS vulnerabilities in security module docstrings
- **Types**: Fixed type annotation for `_TRAVERSAL_PATTERNS` to respect pyright strict mode

## [0.3.1] - 2026-02-27

### Added
- **Type Hinting**: `@overload` signatures for `unwrap_or` and `unwrap_or_else` in `result.py` — enables precise type narrowing in mypy/pyright strict mode
- **Observability**: Optional `on_retry` callback parameter for the `retry()` decorator — receives `(attempt, max_attempts, exception, delay)` on each retry
- **Observability**: Optional `on_state_change` callback for `CircuitBreaker` and `circuit_breaker()` decorator — receives `(old_state, new_state)` on every state transition
- **Security**: Runtime `TypeError` guards in all security functions (`guard_path_traversal`, `guard_command_injection`, `guard_env_variable`, `sanitize_string`, `sanitize_filename`, `validate_project_name`, `validate_email`, `validate_url`, `validate_python_version`)
- **Security**: `guard_env_variable` now rejects empty/whitespace-only variable names with `SecurityError`
- **Security**: `guard_command_injection` validates all items in the command sequence are strings
- Practical usage examples in README combining Result types with Circuit Breaker and Retry

### Changed
- Enriched circuit breaker log messages with failure count, elapsed time, and threshold context
- `Retrier.__exit__` now uses proper `type[BaseException]` and `TracebackType` annotations per Python data model
- `CircuitBreaker._should_attempt()` has explicit return on all code paths for strict type checker compliance

### Fixed
- **Version mismatch**: `__init__.py` had `__version__ = "2.0.0"` (legacy from project rename) — now aligned to `"0.3.1"` matching `pyproject.toml`

## [0.3.0] - 2026-02-26

### Added
- **Sec — SBOM & SLSA**: GitHub Actions workflow generating CycloneDX SBOM via `syft` and signing artifacts with `cosign` (Sigstore keyless OIDC)
- **Sec — Custom SAST Rules**: Semgrep YAML rules enforcing explicit `Err()` handling in Result pattern matches and detecting discarded `@safe` return values
- **Ops — Docker Hardened-by-Default**: Multi-stage Dockerfile (slim builder → Alpine runtime), rootless `appuser`, healthcheck, `.dockerignore`
- **QA — Property-Based Testing**: Hypothesis-powered fuzz tests (500 examples each) covering all sanitizer functions — discovered 5 real edge cases
- **QA — Mutation Testing**: Enhanced `mutmut` configuration with `dict_synonyms`; added `mutmut` and `pytest-benchmark` to dev dependencies
- **QA/Ops — Performance Regression**: GitHub Actions workflow with `pytest-benchmark` + `benchmark-action` failing CI on >5% degradation vs. main baseline
- **QA — 100% Code Coverage**: 664 tests covering 1,586 statements and 448 branches with `fail_under = 100`
- Benchmark test suite (`test_benchmarks.py`) covering sanitizers and Result type utilities
- Comprehensive feature documentation (`docs/FEATURES_v0.3.0.md`)

### Fixed
- **Security**: `cosign verify-blob` in `sbom-slsa.yml` used `".*"` wildcards for certificate identity and OIDC issuer — now restricted to `gabrielima7/TaipanStack` identity and GitHub Actions OIDC issuer

### Changed
- Bumped version from `0.2.9` to `0.3.0`
- CI Semgrep step now includes custom TaipanStack rules (`.semgrep/taipanstack-rules.yml`)
- Added `benchmark` and `property-test` Makefile targets
- Coverage `fail_under` raised from 80% to 100%

## [0.2.9] - 2026-02-25

### Added
- GitHub Actions: Publish to PyPI workflow (Trusted Publishing / OIDC)
- GitHub Actions: Pull Request Labeler workflow with path-based label mapping
- GitHub Actions: Stale issues and PRs management workflow
- GitHub Actions: Greetings workflow for first-time contributors
- `docs/api.md` — API reference documentation for core modules
- `docs/architecture.md` — Architecture and design philosophy documentation

### Changed
- Translated `taipanstack_bootstrapper.py` fully to English (strings, comments, docstrings)
- Translated `tests/test_stack_script.py` fully to English
- Converted all docstrings to imperative mood for D401 Ruff compliance
- Fixed deprecated `[project.license]` table format in `pyproject.toml`
- Updated `Makefile` safety command to ignore disputed CVE-2022-42969 (`py 1.11.0`)

### Security
- Acknowledged NLTK Zip Slip vulnerability (CVE via `safety` transitive dep) — not exploitable in TaipanStack (nltk is never imported)

## [0.2.8] - 2026-02-19

### Fixed
- Fixed import ordering (I001) in `test_final_coverage.py` and `test_ultra_final.py` for ruff 0.15+ compatibility

## [0.2.7] - 2026-02-19

### Fixed
- CI: Resolved stale venv cache on Windows for Python 3.13/3.14 by using full Python version in cache key
- CI: Suppressed pip `externally-managed-environment` stderr noise on ubuntu-24.04

### Security
- Updated `cryptography` 46.0.3 → 46.0.5 (resolves Dependabot security alert)

## [0.2.6] - 2026-02-17

### Security
- Prefixed unused signal handler params with underscore (`_signum`, `_frame`)
- Prefixed unused context manager param with underscore (`_exc_tb`)
- Added security comment for safe `random.uniform` usage (non-cryptographic jitter)
- Updated safety policy to ignore disputed CVE-2022-42969 (`py 1.11.0`)

## [0.2.5] - 2026-02-16

### Fixed
- CI: Invalidated stale CI cache with `taipanstack-v2` prefix
- Removed `restore-keys` fallback that caused stale cache restore from old "Stack" project caches
- Regenerated `poetry.lock` to ensure clean state

## [0.2.4] - 2026-02-15

### Fixed
- CI: Added `--sync` flag to `poetry install` to fix stale virtualenv cache missing pytest
- All Linux container tests pass (Alpine, Fedora, Arch, openSUSE)

## [0.2.3] - 2026-02-14

### Fixed
- Regenerated `poetry.lock` to fix CI `pytest not found` error
- Poetry lock was out of sync causing CI to install only 8 packages instead of full dev dependencies

## [0.2.2] - 2026-02-13

### Changed
- Improved test coverage from 89% to 96.62% with polyfactory integration
- Enhanced test coverage using polyfactory for test data generation
- Achieved 642 passing tests

## [0.2.1] - 2026-02-12

### Fixed
- Fixed UP042: Changed `VersionTier` to inherit from `StrEnum`
- Fixed PLW0108: Inlined lambdas in `test_result_module.py`

### Changed
- Added comprehensive tests for `core.compat` (85% coverage)
- Added comprehensive tests for `core.optimizations` (91% coverage)
- Added comprehensive tests for `config.version_config` (100% coverage)
- Test coverage improved from 89.01% to 96.62% (642 tests)

## [0.2.0] - 2026-02-03

### Changed
- **BREAKING**: Renamed project from "Stack" to "TaipanStack"
- **BREAKING**: All imports changed from `stack.*` to `taipanstack.*`
- Renamed `stack_bootstrapper.py` to `taipanstack_bootstrapper.py`
- Updated all documentation with new project name
- Added PyPI package configuration

### Added
- PyPI package metadata and URLs
- Package entry points for distribution
- `polyfactory` (>=2.0.0) for test data generation
- `pydantic-settings` (>=2.0.0) for configuration management
- Python version-aware optimization system
- 569 tests passing with 89% coverage

## [Unreleased]

### Added
- MIT License for legal clarity
- Comprehensive CONTRIBUTING.md guide
- CHANGELOG.md following Keep a Changelog format
- .editorconfig for consistent editor settings
- Makefile with common development commands
- .vscode/settings.json with recommended Python settings
- .env.example template for environment variables
- GitHub issue templates (bug report, feature request)
- GitHub pull request template
- CI/CD badges to README
- Multi-OS and multi-Python version testing in CI
- Security scanning jobs in CI (Bandit, Safety)
- Type checking job in CI (Mypy)
- Git initialization check and auto-init
- Automatic project structure generation (src/, tests/, docs/)
- Dynamic Python version detection for Mypy
- Connectivity check before installing dependencies
- Post-setup validation
- Example Python files with proper type hints
- detect-secrets pre-commit hook
- Optional production dependencies via --install-runtime-deps flag

### Changed
- Updated pre-commit tool versions to latest
- Updated Ruff configuration to v0.8+ syntax
- Improved Pytest configuration with proper coverage settings
- Made production dependencies (pydantic, orjson, uvloop) optional
- Enhanced CI/CD workflow with matrix testing

### Fixed
- Hardcoded Python version in Mypy configuration
- Generic coverage configuration in Pytest
- Missing backup files extension in .gitignore

## [0.1.0] - 2025-11-26

### Added
- Initial release of TaipanStack bootstrapper
- Poetry project initialization
- Ruff, Mypy, Bandit, Safety, Semgrep integration
- Pre-commit hooks configuration
- Dependabot configuration
- Basic CI/CD pipeline
- Comprehensive test suite
- Documentation in README

[0.3.6]: https://github.com/gabrielima7/TaipanStack/compare/v0.3.5...v0.3.6
[0.3.5]: https://github.com/gabrielima7/TaipanStack/compare/v0.3.4...v0.3.5
[0.3.4]: https://github.com/gabrielima7/TaipanStack/compare/v0.3.3...v0.3.4
[0.3.3]: https://github.com/gabrielima7/TaipanStack/compare/v0.3.2...v0.3.3
[0.3.2]: https://github.com/gabrielima7/TaipanStack/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/gabrielima7/TaipanStack/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/gabrielima7/TaipanStack/compare/v0.2.9...v0.3.0
[0.2.9]: https://github.com/gabrielima7/TaipanStack/compare/v0.2.8...v0.2.9
[0.2.8]: https://github.com/gabrielima7/TaipanStack/compare/v0.2.7...v0.2.8
[0.2.7]: https://github.com/gabrielima7/TaipanStack/compare/v0.2.6...v0.2.7
[0.2.6]: https://github.com/gabrielima7/TaipanStack/compare/v0.2.5...v0.2.6
[0.2.5]: https://github.com/gabrielima7/TaipanStack/compare/v0.2.4...v0.2.5
[0.2.4]: https://github.com/gabrielima7/TaipanStack/compare/v0.2.3...v0.2.4
[0.2.3]: https://github.com/gabrielima7/TaipanStack/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/gabrielima7/TaipanStack/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/gabrielima7/TaipanStack/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/gabrielima7/TaipanStack/compare/v0.1.0...v0.2.0
[Unreleased]: https://github.com/gabrielima7/TaipanStack/compare/v0.3.9...HEAD
[0.3.9]: https://github.com/gabrielima7/TaipanStack/compare/v0.3.8...v0.3.9
[0.3.8]: https://github.com/gabrielima7/TaipanStack/compare/v0.3.7...v0.3.8
[0.3.7]: https://github.com/gabrielima7/TaipanStack/compare/v0.3.6...v0.3.7
[0.1.0]: https://github.com/gabrielima7/TaipanStack/releases/tag/v0.1.0
