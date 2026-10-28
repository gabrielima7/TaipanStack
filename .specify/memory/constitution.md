<!--
Sync Impact Report:
- Version change: Initial template → 1.0.0
- List of modified principles:
  - PRINCIPLE_1: Created "I. Strict Concrete Typing (NO Any)"
  - PRINCIPLE_2: Created "II. Look-Before-You-Leap (LBYL) & Result Pattern (NO Exceptions)"
  - PRINCIPLE_3: Created "III. 100% Real Test Coverage (NO Cheating or Bypassing)"
  - PRINCIPLE_4: Created "IV. Enforced Clean Architecture & Unidirectional Layering"
  - PRINCIPLE_5: Created "V. Secure-by-Design & Fail-Closed DevSecOps"
- Added sections:
  - SECTION_2: Created "Continuous Validation & Quality Gates"
  - SECTION_3: Created "Asynchronous Concurrency & Resilience Standards"
- Removed sections: None
- Follow-up TODOs: None
-->

# TaipanStack Constitution

## Core Principles

### I. Strict Concrete Typing (NO Any)
The codebase MUST target modern Python (3.11+ up to 3.14) with strict static typing. Static type analysis with `mypy` MUST pass with `disallow_untyped_defs = true`, `strict_optional = true`, and `disallow_any_expr = true`. The use of `typing.Any` or any of its methods/aliases is strictly forbidden across all production code (`src/`). Every function, method, parameter, and return value MUST provide a concrete, unambiguous type annotation. When polymorphic type signatures are necessary, developers MUST use generic `TypeVar` with explicit constraints rather than unconstrained objects or untyped signatures.
*Rationale: Concrete typing eliminates runtime type degradation, ensures static verification of interfaces, and eliminates entire classes of runtime attribute and typing faults.*

### II. Look-Before-You-Leap (LBYL) & Result Pattern (NO Exceptions)
Exception throwing for control flow or recoverable business failures is strictly forbidden. The usage of `try/except` and `raise` blocks is prohibited in standard application logic; exceptions represent fatal, unrecoverable panics only. Operations MUST adopt Look-Before-You-Leap (LBYL) semantics by verifying preconditions, validating inputs, and asserting valid system state before invoking execution. All business outcomes and error paths MUST explicitly return `Result[T, E]` types (`Ok` or `Err`) from `taipanstack.core.result`. Consumers of `Result` types MUST exhaustively unpack results using pattern matching (`match/case`) or monadic combinators. Silent failures or swallowed errors are strictly prohibited.
*Rationale: Returning explicit Result monads turns hidden exception control jumps into statically inspectable, compiler-checked data flow and eliminates unhandled runtime crashes.*

### III. 100% Real Test Coverage (NO Cheating or Bypassing)
The project mandates an absolute 100% branch and line test coverage policy (`fail_under = 100`). Bypassing or artificially inflating coverage reports via `# pragma: no cover`, `@pytest.mark.skip`, empty `pass` statements, or omission filters is strictly forbidden. All tests MUST be functional, non-trivial, and assertive. In addition to standard deterministic unit and integration test suites, developers MUST implement property-based fuzz testing via `hypothesis` for sanitizers, guards, validators, and mathematical or stateful components.
*Rationale: Complete, un-cheated test suites guarantee zero regression tolerance and verify all reachable execution branches under both standard and adversarial inputs.*

### IV. Enforced Clean Architecture & Unidirectional Layering
The codebase strictly adheres to a unidirectional layered architecture enforced statically via Import Linter: `src/app/` → `security/` → `config/` → `bridges/` → `resilience/` → `utils/` → `core/`. Dependencies MUST flow strictly downward. The `taipanstack.core` layer is foundational and MUST NEVER import from upper layers (`security`, `utils`, `config`, `resilience`, `bridges`, or `app`). Submodules MUST strictly respect isolated contract boundaries as declared in `.importlinter`.
*Rationale: Architectural layer enforcement prevents circular dependencies, decouples core domain mechanics from external I/O bridges, and ensures high modularity and maintainability.*

### V. Secure-by-Design & Fail-Closed DevSecOps
Security mechanisms MUST be fail-closed by design: invalid, ambiguous, or malicious input MUST immediately result in explicit rejection. All external inputs, filesystem access (`guard_path_traversal`), CLI executions (`guard_command_injection`), and environment variables MUST pass through `taipanstack.security` boundaries. Subprocess environments MUST be isolated using `allowed_env_vars` to prevent secret leakage. Credentials and sensitive attributes in models MUST utilize Pydantic `SecretStr` or `SecretBytes` to prevent leakage into logs, serialization, or representations. Every change MUST undergo AST static security scanning (Bandit, Semgrep) and dependency vulnerability scanning (`pip-audit`), supplemented by SBOM (CycloneDX) and SLSA provenance attestations upon release.
*Rationale: Fail-closed security and automated DevSecOps pipelines guarantee comprehensive defense-in-depth across the entire software supply chain.*

## Continuous Validation & Quality Gates
Every code change MUST pass all quality gates prior to merge. Developers and automated agents MUST execute `make all` to verify that linting, formatting (`ruff` with 88-character limit and double quotes), static typing (`mypy`), dead-code analysis (`vulture`), architectural contracts (`import-linter`), security checks (`bandit`, `pip-audit`), and unit tests (100% coverage) succeed with zero errors. Any documentation changes MUST pass `poetry run mkdocs build --strict` without warnings. Cyclomatic complexity for any routine MUST not exceed a McCabe index of 10.
*Rationale: Uniform quality gates ensure that no regression in security, typing, style, or performance enters the main branch.*

## Asynchronous Concurrency & Resilience Standards
Production execution MUST leverage high-throughput asynchronous execution using `uvloop` (where platform support permits) and `orjson` serialization initialized via `taipanstack.core.optimizations.apply_optimizations()`. Network bridges and external database connectors MUST integrate resilience mechanisms, including circuit breakers (`taipanstack.resilience.circuit_breaker`), exponential backoff retries (`taipanstack.resilience.retry`), and adaptive bulkheads. Asynchronous routines MUST NOT execute blocking synchronous calls directly on the event loop.
*Rationale: Enforcing robust concurrency and resilience patterns prevents thread starvation, cascades of failure, and latency degradation under high-load scenarios.*

## Governance
This Constitution is the supreme architectural, engineering, and quality specification for TaipanStack. It supersedes informal practices, unratified conventions, and conflicting implementation patterns. Every pull request and review MUST explicitly verify compliance with this Constitution.

Amendments to this Constitution require:
1. A formal proposal detailing motivation, architectural impact, and migration plan.
2. Approval by project maintainers via pull request review.
3. An increment to `CONSTITUTION_VERSION` in compliance with Semantic Versioning:
   - MAJOR bump: Incompatible governance changes, removal or semantic weakening of principles.
   - MINOR bump: Addition of new principles, new sections, or substantive expansions of guidance.
   - PATCH bump: Non-semantic clarifications, typographical corrections, or formatting updates.
4. An update to `LAST_AMENDED_DATE` matching the amendment adoption date.

Automated CI gates act as strict constitutional enforcement: any PR failing typing, coverage, architectural linting, or security scanners MUST NOT be merged. Operational development guidelines documented in `docs/agents.md` and `docs/architecture.md` serve as mandatory procedural extensions of this Constitution.

**Version**: 1.0.0 | **Ratified**: 2026-10-27 | **Last Amended**: 2026-10-27
