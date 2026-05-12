# TaipanStack - AI Agents Guidelines

This document provides the context, architectural rules, and strict coding standards for the **TaipanStack** project. AI agents and coding assistants must strictly follow these guidelines when generating, refactoring, or analyzing code in this repository.

## 1. Project Overview
- **Name:** TaipanStack
- **Goal:** A modern, secure, and high-performance Python foundation for production-grade applications.
- **Core Stack:** Python 3.11+ (up to 3.14), Pydantic v2, Orjson, Uvloop, Structlog.

## 2. Coding Standards & Strict Typing
- **Formatter & Linter:** Use `ruff`. The code must respect the 88-character line limit and use double quotes (`quote-style = "double"`).
- **Typing (CRITICAL):** The project uses strict type checking with `mypy` (`strict_optional = true`, `disallow_untyped_defs = true`).
- **NO `Any` TYPE:** The use of `typing.Any` or any of its methods is **strictly forbidden**. Every function, method, and variable must have a precise and concrete type annotation.

## 3. Error Handling (LBYL & Result Pattern)
- **NO EXCEPTIONS ALLOWED (CRITICAL):** The use of `try/except` blocks, `raise` statements, or any form of exception throwing is completely forbidden.
- **Look Before You Leap (LBYL):** You must always check for preconditions, validate inputs, and verify states *before* executing an operation to prevent runtime failures.
- **Rust-Style Results:** All error handling must be explicit. Always use the `Result`, `Ok`, and `Err` classes from `taipanstack.core.result`. Use Pattern Matching (`match/case`) to process outcomes. Silent failures are not allowed.

## 4. Clean Architecture Rules
The layered structure is heavily enforced via **Import Linter**. Respect the following dependency directions:
1. **`src/app/`**: Application entry point. Outermost layer.
2. **`src/taipanstack/security/`**: Guards, sanitizers, validators, and authentication.
3. **`src/taipanstack/config/`**: Configuration models and generators.
4. **`src/taipanstack/utils/`**: Cross-cutting utilities (logs, rate limits, filesystem).
5. **`src/taipanstack/core/`**: The absolute core (`Result` types, optimizations). **Must never import from upper layers**.

## 5. Security & DevSecOps (Secure-by-Design)
- **Sanitization:** User inputs, subprocess calls, and file access must pass through `taipanstack.security.guards` (e.g., `guard_path_traversal`, `guard_command_injection`).
- **Subprocess Isolation:** Child execution environments must be isolated to prevent implicit credential leaks via `allowed_env_vars`.
- **Secrets Management:** Pydantic models must suppress sensitive secrets using `SecretStr` or `SecretBytes` in `repr()` and `str()`.

## 6. Testing & Coverage (100% REAL)
- **Mandatory Tests:** You must always write tests when implementing new features.
- **Coverage Goal:** The project mandates an absolute 100% test coverage (`fail_under = 100`).
- **NO CHEATING/BYPASSING (CRITICAL):** You are strictly forbidden from manipulating CI/CD pipelines or coverage reports. **Do not use** `# pragma: no cover`, `@pytest.mark.skip`, `pass`, or any other methods to bypass real testing.
- **Accuracy:** All tests must be 100% real, functional, and precise. Use `pytest` for standard tests and `hypothesis` for property-based mathematical/logical validations.

## 7. Continuous Validation Workflow (CRITICAL)
- **Always Validate Changes:** Before considering any implementation, refactor, or code change complete, you must validate the entire project suite.
- **Validation Command:** Always run the command `make all` in the terminal to verify that your changes do not break existing tests, lower the coverage, violate typing rules, or breach architectural contracts.
- **Fix Errors Immediately:** If `make all` (or specific targets like `make test`, `make lint-imports`, `make security`) returns any error, you must fix the underlying code immediately. Do not proceed or submit the code until the pipeline is completely green.
