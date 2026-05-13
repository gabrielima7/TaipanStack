# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.8] - 2026-05-08

### Security
- **Fix (High)**: Restored missing type guard for `password_hash` in `verify_password` to prevent potential type confusion (Commit f83b6745).
- **Fix (Medium)**: Enhanced durability of atomic writes by hardening file handle synchronization (PR #688).

### Resilience
- **Hardening**: Hardened `RateLimiter` and `CircuitBreaker` against state corruption and type mutations via chaos testing (PR #689, #684, #703).
- **Fix**: Handled `TypeError` edge cases in `CircuitBreaker` state transitions (PR #691).
- **Performance**: Implemented concurrent execution for async health checks in `HealthPinger` (PR #694).

### Refactoring & Clean Code
- **Complexity**: Major reduction of cyclomatic complexity across core modules, subprocess utilities, and web bridges (PR #706, #692, #686).
- **Typing**: Enforced explicit static type-guards and removed structural matching for better maintainability (PR #705).
- **Chore**: Standardized and refactored CI/CD pipelines for authenticity and zero-bypass execution (PR #690).

### QA & Testing
- **Coverage**: Improved branch coverage for implicit Python match and if/elif statements (PR #708).
- **Test Suite**: Expanded to **1,334 passing tests** with 100% verified coverage.
- **Chaos**: Introduced dedicated chaos tests for circuit breaker and rate limiter state corruption.

### Documentation
- **Synchronization**: Synchronized test counts and version metadata across all documentation portals (PR #707, #693, #687).
- **New**: Integrated `agents.md` guidelines into the official documentation.

## [0.4.7] - 2026-05-04

### Security
- **Fix (High)**: Resolved TOCTOU vulnerability in filesystem operations by enforcing atomic checks (PR #663).
- **Fix (High)**: Hardened `guard_ssrf` against `UnicodeError` via fuzzing and strict normalization (PR #667).
- **Fix (High)**: Hardened `verify_password` against malformed Argon2 hashes (PR #661).

### Resilience
- **Feat**: Implemented system resource exhaustion handling in `Bulkhead` to prevent thundering herds (PR #662).
- **Hardening**: Injected system resource exhaustion in adaptive orchestrator and hardened semaphore acquisition (PR #668).

### Refactoring & Clean Code
- **Complexity**: Significantly reduced cyclomatic complexity across core resilience, circuit breaker, and compat modules (PR #680, #676, #666, #670).
- **Typing**: Enhanced ASGI static typing in `web_bridge` using `TypeAlias` (PR #682).
- **Typing**: Standardized internal Pydantic model typing and fixed unused arguments (PR #669).

### CI/CD & Dependencies
- **Optimization**: Optimized and strictly validated CI/CD pipelines to enforce zero-bypass execution (PR #675, #664).
- **Fix**: Restored benchmark alert-threshold to 200% to accommodate GitHub runner variance (PR #664).

### QA & Testing
- **Audit**: Comprehensive test suite audit, refactor, and standardization for environment isolation (PR #683, #671, #665).
- **Coverage**: Achieved true 100% genuine code coverage by resolving remaining coverage bypasses (PR #674).
- **Test Suite**: Reached **1,314 passing tests** with 100% verified coverage.
- **Synchronization**: Synchronized test count metrics across all documentation portals (PR #681, #672).

## [0.4.6] - 2026-04-30

### Security
- **Fix (Critical)**: Resolved TOCTOU vulnerability in `tempfile.mkstemp` by ensuring atomic creation and strict permissions (PR #651).
- **Fix (High)**: Patched Denial of Service (DoS) vulnerability in `guard_file_extension` by hardening extension stripping logic (PR #658).
- **Fix (High)**: Remedied unbounded cache growth DoS in the `@cached` decorator by implementing a bounded cache with LRU (Least Recently Used) eviction policy (PR #646).
- **Fix (Medium)**: Prevented empty generator bypass in `guard_command_injection` ensuring strict iterator validation (PR #640).
- **Hardening**: Reinforced `RateLimiter` resilience against massive forward time jumps (NTP syncs/chaos) via monotonic state tracking (PR #642).
- **Audit**: Resolved global Semgrep security findings and standardized `nosem` exclusions across the core (PR #659).

### Resilience
- **Hardening**: Hardened the `@timeout` decorator against thread exhaustion in high-concurrency environments (PR #638).
- **Hardening**: Reinforced the `limit_concurrency` bulkhead pattern against resource exhaustion during extreme load spikes (PR #652).

### Refactoring & Clean Code
- **Complexity**: Significantly reduced cyclomatic complexity across sanitizers, subprocess utilities, and resilience modules (PR #649).
- **Coverage**: Achieved the ultimate quality milestone: **true 100% genuine code coverage** by eliminating all remaining `pragma: no cover` bypasses (PR #644, #654).
- **Typing**: Removed deprecated internal Pydantic `IncEx` imports and modernized type aliases (PR #641).
- **Adaptive**: Streamlined adaptive resilience components by removing unused `_window_size` attributes (PR #637).
- **Chore**: Removed unused `ensure_ascii` argument from `model_dump_json` calls to align with Pydantic v2 best practices (PR #660).

### CI/CD & Dependencies
- **Audit**: Standardized and audited all CI/CD pipelines to enforce zero-bypass execution and restored critical mutation-testing/docker-build jobs (PR #643, #653, #639).
- **Dependencies**: Upgraded `cryptography` to `>=46.0.7` and bumped the GitHub Actions group to latest versions (PR #647, #648).

### QA & Testing
- **Test Suite**: Expanded the test suite to **1,290 passing tests** with 100% coverage verified.
- **Synchronization**: Synchronized test counts and version metadata across all documentation portals (PR #655).

## [0.4.5] - 2026-04-27

### Security
- **Hardening**: Reinforced `RateLimiter` against state corruption and `NaN` poisoning (PR #622).
- **Hardening**: Shielded `CircuitBreaker` against `NaN`/`Inf` poisoning and state counter corruption (PR #627, #630).
- **Hardening**: Hardened `sanitize_path` against massive string DoS vectors (PR #635).

### Performance
- **Optimization**: Optimized `@safe` and `collect_results` decorators by hoisting internal type checks and reducing closure overhead (Commit 14d069b5).

### Resilience
- **Complexity**: Significantly reduced cyclomatic complexity in `CircuitBreaker`, `Retry`, and `RateLimiter` modules (PR #628, #632).

### Refactoring & Typing
- **Strict Typing**: Eliminated remaining `Any` usage and resolved all `type: ignore` directives across core modules (PR #624).
- **Clean Code**: Reduced cyclomatic complexity in security guards and standardized internal utilities (PR #625).
- **CI/CD**: Audited and standardized CI/CD pipelines to remove legacy bypasses and enforce strict naming (PR #631).

### QA & Testing
- **Coverage**: Achieved true **100% genuine code coverage** by eliminating all `pragma: no cover` bypasses (PR #636).
- **Test Suite**: Reached **1,253 passing tests** with verified 100% coverage.
- **CI Fixes**: Resolved `pip-audit` strictly treating editable installs as failures and stabilized benchmark concurrency (Commit 897bcb1e).

### Documentation
- **Alignment**: Synchronized project version and release notes across all auxiliary files (PR #633, Commit 2562439b).
- **MkDocs**: Resolved strict build warnings in Pydantic model docstrings (PR #626).

## [0.4.4] - 2026-04-24


### Security
- **Fix (High)**: Hardened `guard_file_extension` against null bytes (`\x00`) and trailing whitespace/dots bypasses (PR #619).
- **Fix (High)**: Handled unhandled `RuntimeError` on symlink loops in `guard_path_traversal` (PR #589).
- **Hardening**: Enforced `math.isfinite` validation in `RetryConfig` to prevent NaN/Inf induced infinite loops or crashes (PR #618).
- **Hardening**: Mitigated potential thread exhaustion in timeout decorators (PR #578).
- **Fuzzing**: Extensive security guards stress testing and stress-testing via Hypothesis (PR #597).
- **Fuzzing**: Detected and mitigated ReDoS in `sanitize_filename` via Hypothesis fuzzing (PR #605).
- **Audit**: Addressed critical `pip` vulnerability (CVE-2026-3219) via explicit `pip-audit` ignore-vuln strategy and detailed documentation.
- **Audit**: Addressed transitive legacy dependency vulnerability (PYSEC-2022-42969) in `py` library.
- **Dependencies**: Upgraded `pytest` to `9.0.3` to remediate CVE-2025-71176.

### Resilience
- **Chaos**: Integrated `Result` monad into `CircuitBreaker` state change notifications (PR #593).
- **Chaos**: Resolved unhandled errors in `CircuitBreaker` during untracked state transitions (PR #598).
- **Chaos**: Resolved micro-chaos issues in `Retry` monad propagation (PR #592).

### Performance & CI/CD
- **CI/CD**: Streamlined GitHub Actions by removing redundant container distribution tests and cleaning up bypass scripts (PR #610, #614).
- **CI/CD**: Optimized infrastructure isolation and hardened pipeline execution model (PR #599).
- **Docs**: Fixed MkDocs configuration and Mermaid syntax rendering issues (PR #613).

### Changed & Refactoring
- **Typing**: Eliminated remaining `Any` usage in `taipanstack.security.models` enforcing strict Pydantic model dump signatures (PR #615).
- **Typing**: Comprehensive static typing improvements in security models and core utilities (PR #585, #601).
- **Clean Code**: Synchronized and standardized bootstrapper naming references across tests and documentation (PR #616, #596).
- **Complexity**: Significantly reduced cyclomatic complexity across security guards and internal utilities (PR #591, #594, #606).
- **Docs**: Resolved deprecated imports in documentation examples and synchronized test count (PR #586, #587).

### QA & Testing
- **Coverage**: Achieved true 100% test coverage by resolving coverage bypasses and removing `pragma: no cover` (PR #579, #590, #611).
- **Coverage**: Fixed bridge component test coverage for database and HTTP fallback states (PR #620).
- **Refactoring**: Comprehensive test suite refactor and standardization for environment isolation (PR #595, #600).
- **Tests**: Reached 1237 passing tests with 100% code coverage.

## [0.4.3] - 2026-04-14

### Security
- **Fix (High)**: Patched URL validation bypasses and DoS edge cases in `validate_url` (PR #487).
- **Fix (High)**: Mitigated `urlparse` SSRF risks and unbounded sleep delays in `guard_ssrf`.
- **Fix (High)**: Resolved URL length DoS vulnerability in `guard_ssrf` via Hypothesis fuzzing (PR #544).
- **Fix (Medium)**: Hardened `validate_python_version` and `validate_email` against extreme inputs and DoS vectors (PR #423, #526, #551).
- **Fix (Medium)**: Hardened `RateLimiter` against time corruption and state poisoning (PR #489).
- **Fix (Medium)**: Remedied DoS vector in `run_safe_command` timeout (PR #490).
- **Hardening**: Enforced `math.isfinite` checks on all timeout parameters across decorators and circuit breakers (PR #558).
- **SAST**: Introduced custom Semgrep rules for Pydantic secrets, unsafe temp file removal, path traversal, and insecure hashing/deserialization (PR #486, #507).
- **Hardening**: Patched `ensure_dir` and added Semgrep rules for insecure `mkdir` modes (PR #420).

### Resilience
- **Hardening**: Enforced finite thresholds in `CircuitBreaker` states to prevent NaN-induced logic corruption (PR #537).
- **Hardening**: Stabilized retry exponential backoff against chaos anomalies and state drifting (PR #450).
- **Hardening**: Hardened `@timeout` decorator against NaN and negative bounds (PR #254).
- **Chore**: Eliminated unused `AdaptiveTimeout` dead code (PR #510).

### Performance
- **Optimization**: Optimized path and filename sanitization hot paths by hoisting regex initialization.
- **Optimization**: Optimized `@safe` and `@safe_from` decorators by hoisting type casts and reducing closure overhead (PR #532).
- **Optimization**: Batch performance improvements across core and security modules (PR #452).

### Changed & Refactoring
- **Refactoring (Breaking)**: Strictly typed the entire codebase and completely eliminated `Any` usages (PR #465, #543).
- **Refactoring**: Modernized `src/taipanstack/core/result.py` with modern container type checks (PR #518).
- **Refactoring**: Adopted `match/case` syntax in security models for better maintainability.
- **Complexity**: Significantly reduced cyclomatic complexity across bridges and filesystem utilities (PR #453, #494).
- **Dead Code**: Removed `guard_hash_algorithm` and other orphaned filesystem helpers (PR #527).

### QA & CI/CD
- **Coverage**: Achieved true 100% test coverage in core `result` module with 1205 passing tests (PR #481).
- **CI/CD**: Standardized workflows, removed bypasses, and enforced strict execution naming (PR #531, #546).
- **Tests**: Corrected JWT fuzzer properties and fixed Hypothesis health checks in CI (PR #547).

## [0.4.2] - 2026-03-31

### Security
- **Fix (Critical)**: Fixed OS command injection vulnerability by hardening the security guards against command concatenation and shell escape sequences (PR #385).
- **Fix (Critical)**: Isolated subprocess environment variables to prevent sensitive data leakage and credential exposure (PR #403).
- **Fix (Critical)**: Remedied sensitive data exposure in User Domain Model by redacting password hashes from public serialization schemas (PR #402).
- **Fix (High)**: Patched DoS vulnerability in PBKDF2 legacy verification by enforcing `MAX_LEGACY_ITERATIONS` limit (PR #411).
- **Fix (High)**: Hardened the `@cached` decorator against cache collision vulnerabilities (PR #388).
- **Fix (Medium)**: Enforced mandatory network timeout defaults across all bridge components to prevent resource exhaustion (PR #381).
- **Fix (Medium)**: Resolved unhandled exceptions during `CircuitBreaker` state change callbacks (PR #380).
- **Fix**: Prevented crash during log redaction when processing non-string dictionary keys (PR #378).
- **Fix**: Improved exception serialization resilience for "Dataclass Exceptions" in the secure system (PR #409).
- **Hardening**: Prevented silent path mutation in `safe_write` by raising `SecurityError` on unsafe character sequences (PR #408).
- **Hardening**: Prevented potential type masking during password verification routines (PR #391).

### Performance
- **Optimization**: Implemented lazy evaluation for `find_files` utility to prevent memory bottlenecks during large directory crawls (PR #394).

### Changed & Refactoring
- **Refactoring**: Standardized filesystem error classes to use idiomatic dataclass properties for better maintainability (PR #401).
- **Refactoring**: Removed generic linter suppressions and resolved legacy code quality warnings (PR #398).
- **Chore**: Enabled `ResourceWarning` in pytest configuration to proactively detect leaked file handles and sockets (PR #393).
- **Fix**: Resolved `UnicodeDecodeError` in subprocess execution by hardening output decoding logic (PR #407).
- **Fix**: Fixed Pygments crash in documentation generation during mkdocstrings processing (PR #386).
- **Optimization**: Reduced cyclomatic complexity in security sanitizer modules (PR #384).

## [0.4.1] - 2026-03-30

### Security
- **Fix (Critical)**: Patched arbitrary code loading vulnerability via `importlib` and hardened Module Imports to prevent unvalidated loading and SSRF (PR #365).
- **Fix**: Mitigated PyJWT `NotImplementedError` bypass protecting token parsing (PR #359).
- **Hardening**: Hardened cache decorator against unhashable inputs preventing cache poisoning (PR #350).
- **SAST**: Introduced new custom Semgrep rules for continuous security coverage (PR #367).

### Performance
- **Optimization**: Core results and security sanitizers optimized for higher throughput (PR #375).

### Resilience & Refactoring
- **Typing**: Added strict Generic Static Typing in the Resilience Adaptive Suite (PR #373).
- **Complexity**: Reduced cyclomatic complexity across `http_bridge` and `sanitizers` (PR #369).
- **Exceptions**: Resolved unhandled `BaseException` propagation in timeout threads (PR #366).
- **Dead Code**: Cleaned up legacy/dead code from optimizations and config generators (PR #360, #374).
- **Modernization**: Upgraded `Result` type unwrapping in core using `match/case` structural pattern matching (PR #358).

### Docs & QA
- **Coverage**: Achieved 100% test coverage including branch coverage within `src/taipanstack/` (PR #362).
- **Docs**: Synchronized global test count to 1184 passing tests in architecture docs (PR #364).

## [0.4.0] - 2026-03-26

### Added
- **Taipan Bridges**: A universal integration layer for external dependencies.
  - `_imports.py`: Safe lazy dependency loading returning `Result`.
  - `http_bridge.py`: ASGI `SafeHttpClient` and `safe_request` integrating `httpx` with natively enforced SSRF protection, circuit breaker, and retry.
  - `db_bridge.py`: `ResilientDatabase` for SQLAlchemy and `ResilientRedis` with auto-repair and timeouts.
  - `web_bridge.py`: Framework-agnostic ASGI `TaipanMiddleware` delivering rate-limiting, missing JSON responses, and strict security headers injected.
- **Watchdogs (Active Monitoring)**:
  - `HealthPinger`: Proactively pings external dependencies and preemptively opens Circuit Breakers on failure.
  - `ResourceWatcher`: Enforces process-level CPU/RAM limits protecting against exhaustion.
  - `ConfigWatcher`: Checks for configuration alterations via SHA-256 fingerprinting.
- **Adaptive Resilience**: Self-healing components that tune parameters in real-time.
  - `AdaptiveCircuitBreaker`: Learns success rate and dynamically adjusts the failure threshold over a rolling window.
  - `AdaptiveRetry`: Analyzes backoff effectiveness and intelligently sets optimal retry delays.
  - `AdaptiveTimeout`: Uses EMA (Exponential Moving Average) to automatically set request timeouts based on recent response latencies.
  - `Bulkhead`: Async concurrency isolation and queue limiting to prevent thundering herd scenarios.
  - `ResilienceOrchestrator`: A fluent builder to orchestrate a combination of components (Bulkhead → Breaker → Retry → Fallback) in a unified pipeline.

### Security
- **Hardening**: Hardened `guard_hash_algorithm` against potential bypass mechanisms (PR #318).
- **SAST**: Injected new custom Semgrep rules to actively audit Insecure YAML and weak Hashing algorithms (PR #326).
- **Dos**: Remedied a security vulnerability where enormous bcrypt hashes could induce an unhandled `OverflowError` in Password Verification routing (PR #307).
- **Dependencies**: Regenerated the Poetry lockfile and upgraded the resolved `requests` version to `2.33.0`, remediating the insecure temporary file reuse advisory reported by Dependabot.
- **Dependencies**: Kept `Pygments` pinned at `2.19.2`, the newest upstream release currently available, and documented the remaining local-only ReDoS risk until an upstream fix is published.

### Performance
- **Optimization**: Execution speed of `sanitize_filename` was significantly boosted for high I/O volume environments (PR #322).

### Changed & Refactoring
- **Typing**: Replaced generic `Coroutine`/`Any` signatures in core utilities with strict `Awaitable`, resolving static lint warnings (PR #323).
- **Coverage**: Introduced native Edge Cases validating the contextual resolutions of `Retrier.__exit__` promoting better overall stability (PR #327).
- Refactored `taipanstack.utils.retry` and `taipanstack.utils.circuit_breaker` into a dedicated `taipanstack.resilience` layer.
- Restored `taipanstack.utils.retry` and `taipanstack.utils.resilience` as backward-compatibility shims that exactly re-export the canonical `taipanstack.resilience` symbols.
- Restored `Retrier` loop semantics in `taipanstack.resilience.retry` so manual retry loops preserve the accumulated suppressed-attempt counter.
- Added new import-linter contract `bridges-isolation` to ensure `taipanstack.bridges` does not couple with application configurations.
- Upgraded `Makefile` security scanning ignoring Pygments CVE-2026-4539 to avoid false positives.
- Hardened Linux distro CI provisioning by refreshing openSUSE metadata with retries and initializing the Arch Linux keyring before full upgrades.

### QA / Testing
- Achieved validation over 1164 passing tests enforcing 100% test coverage threshold on the new architectural modules.

## [0.3.11] - 2026-03-23

### Security
- **Fix (ReDoS)**: Prevented unhandled regex backreference processing in `sanitize_filename` avoiding string manipulation DoS vectors (PR #294).
- **Fix (Recursion Error)**: Prevented `RecursionError` DoS in `_mask_data` when handling deeply nested JSON payloads (PR #284).
- **SAST Rules**: Added custom Semgrep rules to comprehensively detect command injection, XXE, and DoS patterns (PR #272).
- **Hardening (JWT)**: Hardened JWT parsers against malformed input types using Hypothesis fuzzing (PR #275).

### Resilience
- **Chaos Mitigation**: Hardened `CircuitBreaker` `HALF_OPEN` state against Thundering Herd attacks by capping simultaneous attempts (PR #285).

### Refactoring
- **Typing**: Enhanced static typing in core decorators using generic Protocols (PR #288).
- **Modernization**: Adopted native `result` library methods, replacing deprecated `unwrap_or` and `unwrap_or_else` wrappers (PR #273).
- **Modernization**: Modernized `core/optimizations.py` using `match/case` structural pattern matching (PR #283).
- **Modernization**: Modernized type aliases and unions in `resilience.py` (PR #274).
- **Code Quality**: Reduced cyclomatic complexity in security guards (PR #270).

### QA / Testing
- **Coverage**: Improved test coverage for retry utility loop exhaustion (PR #268).
- **Coverage**: Removed `pragma: no cover` in sanitizers for stricter tracking (PR #286).

### Docs
- **Documentation**: Synced all documentation with latest releases and updated architecture test count to 1006 tests (PR #271, #280, #289).

## [0.3.10] - 2026-03-20

### Security
- **Critical Fix**: Patched ReDoS vulnerability by enforcing `\Z` anchor instead of `$` in all string validators (#255).
- **Hardening**: Restricted hash algorithms to secure ones (`sha256`, `sha512`) in internal utilities (#181).
- **Hardening**: Enhanced filesystem path traversal validation with stricter canonicalization and expanded test coverage (#179).
- **Privacy**: Prevented accidental credential leakage in subprocess error messages and asynchronous logging streams (#175).
- **Privacy**: Implemented `SecureBaseModel` for all internal user-related schemas to ensure automatic sensitive data redaction (#177).
- **Dependencies**: Bumped `authlib` and `pyjwt` to latest versions to patch upstream CVEs.

### Performance
- **Optimization**: Optimized `sanitize_string` using precompiled regex patterns, reducing overhead by ~20% on high-throughput sanitization (#245).
- **Optimization**: Refactored `guard_ssrf` to use `ipaddress` built-ins for faster network range evaluation (#178).

### Resilience
- **Robustness**: Hardened `RateLimiter` against backward clock jumps (NTP syncs) by using monotonic references (#252).
- **Fix**: Resolved edge-case chaos in `retry` delay calculation when negative attempt counts were passed (#229).

### Refactoring
- **Code Quality**: Reduced cyclomatic complexity in security guards and sanitizers for better maintainability (#253).
- **Modernization**: Refactored `utils/cache.py` and `default_encoder` to use Python 3.10+ structural pattern matching (`match/case`) (#250, #227).
- **Strict Typing**: Renamed unused logging parameters and removed legacy `# noqa` comments to align with strict mypy/ruff rules (#172, #174).

### QA / Testing
- **Coverage**: Achieved 100% code coverage with 1006 passing tests (#254).
- **Reliability**: Replaced deprecated `.ok()` and `.err()` usages with `.ok_value` and `.err_value` across the entire test suite (#248).
- **Edge Cases**: Added explicit validation for empty content handling in `safe_write` filesystem utility (#225).
- **Bootstrapper**: Improved testing isolation for `_setup_pre_commit` and core bootstrapper logic (#176).

## [0.3.9] - 2026-03-11

### Added
- **Observability**: New `taipanstack.utils.context` module with `correlation_id_var` and `correlation_scope` integrated into `structlog` for distributed tracing.
- **Resilience**: New decorators `@fallback` and `@timeout` in `taipanstack.utils.resilience` supporting both sync and async functions rigorously typed with the `Result` monad and `ParamSpec`.
- **Caching**: Intelligent caching decorator `@cached` with TTL support that seamlessly ignores `Err()` results while caching only `Ok()` outcomes.
- **Security**: New Pydantic v2 compatible security types `SafeHtml` and `SafeSqlIdentifier` in `taipanstack.security.types`.

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
- Translated `tests/test_taipanstack_script.py` fully to English
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

[Unreleased]: https://github.com/gabrielima7/TaipanStack/compare/v0.4.8...HEAD
[0.4.8]: https://github.com/gabrielima7/TaipanStack/compare/v0.4.7...v0.4.8
[0.4.7]: https://github.com/gabrielima7/TaipanStack/compare/v0.4.6...v0.4.7
[0.4.6]: https://github.com/gabrielima7/TaipanStack/compare/v0.4.5...v0.4.6
[0.4.5]: https://github.com/gabrielima7/TaipanStack/compare/v0.4.4...v0.4.5
[0.4.4]: https://github.com/gabrielima7/TaipanStack/compare/v0.4.3...v0.4.4
[0.4.3]: https://github.com/gabrielima7/TaipanStack/compare/v0.4.2...v0.4.3
[0.4.2]: https://github.com/gabrielima7/TaipanStack/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/gabrielima7/TaipanStack/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/gabrielima7/TaipanStack/compare/v0.3.11...v0.4.0
[0.3.11]: https://github.com/gabrielima7/TaipanStack/compare/v0.3.10...v0.3.11
[0.3.10]: https://github.com/gabrielima7/TaipanStack/compare/v0.3.9...v0.3.10
[0.3.9]: https://github.com/gabrielima7/TaipanStack/compare/v0.3.8...v0.3.9
[0.3.8]: https://github.com/gabrielima7/TaipanStack/compare/v0.3.7...v0.3.8
[0.3.7]: https://github.com/gabrielima7/TaipanStack/compare/v0.3.6...v0.3.7
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
[0.1.0]: https://github.com/gabrielima7/TaipanStack/releases/tag/v0.1.0
