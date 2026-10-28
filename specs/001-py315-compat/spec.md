# Feature Specification: Python 3.15 Integration and Runtime Compatibility

**Feature Branch**: `001-py315-compat`

**Created**: 2026-10-27

**Status**: Approved

**Input**: User description: "implemente e integre a versão 3.15 do python ao projeto"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Deterministic Python 3.15 Runtime Detection (Priority: P1)

A developer running TaipanStack on a Python 3.15 interpreter imports `taipanstack.core.compat` to check version compatibility and inspect runtime features.

**Why this priority**: Foundational core requirement. Downstream components and applications require static constants (`PY315`) and runtime introspection (`get_features()`) to support Python 3.15 deterministically with zero runtime performance degradation and strict type checking.

**Independent Test**: Can be fully verified on pre-3.15 and 3.15 interpreters by running unit test assertions and mock simulation tests:
`poetry run pytest tests/test_compat_standard_expected.py -v --cov=taipanstack.core.compat --cov-report=term-missing`

**Acceptance Scenarios**:

1. **Given** a Python 3.15 interpreter, **When** evaluating `PY315` from `taipanstack.core.compat`, **Then** it evaluates to `True`, and `"PY315"` is present in `__all__`.
2. **Given** a Python 3.15 interpreter, **When** calling `get_features()`, **Then** `features.version` accurately reports `(3, 15, x)` and `features.tier` returns `VersionTier.CUTTING_EDGE`.
3. **Given** a pre-3.15 interpreter (3.11-3.14), **When** simulating Python 3.15 execution via patched `PY315` and `PY_VERSION` with `get_features(force_refresh=True)`, **Then** 100% branch and line coverage is achieved with zero regressions in existing version tier tests.

---

### User Story 2 - Package Metadata Alignment (Priority: P2)

A developer or automated package installer inspects TaipanStack's PyPI classifiers and repository documentation to verify Python 3.15 compatibility.

**Why this priority**: Ensures packaging tools, pip, and PyPI search accurately index TaipanStack as compatible with Python 3.15 without manual overrides.

**Independent Test**: Can be verified by running `poetry check` and inspecting package metadata classifiers in `pyproject.toml` and shield badges in `README.md`.

**Acceptance Scenarios**:

1. **Given** `pyproject.toml`, **When** inspected, **Then** `"Programming Language :: Python :: 3.15"` is present in the `classifiers` array under `[project]`.
2. **Given** `README.md`, **When** inspected, **Then** the Python version badge displays `3.11 | 3.12 | 3.13 | 3.14 | 3.15`.

---

### User Story 3 - Automated CI Pipeline Validation (Priority: P3)

A contributor opens a pull request, and GitHub Actions automatically executes the test suite against Python 3.15 runners.

**Why this priority**: Guarantees automated regression testing on Python 3.15 while protecting the repository from unbuilt upstream third-party C-extension wheels via failure isolation (`continue-on-error: true`).

**Independent Test**: Can be verified by linting `.github/workflows/ci-push-validate.yml` and confirming that the test matrix includes `"3.15"` with failure isolation.

**Acceptance Scenarios**:

1. **Given** `.github/workflows/ci-push-validate.yml`, **When** GitHub Actions executes `ci-test`, **Then** the test matrix includes `"3.15"`.
2. **Given** the 3.15 matrix job, **When** running in CI, **Then** it uses `continue-on-error: true` so upstream wheel delays do not block repository merges.

---

## Technical Constraints & Quality Gates

1. **Strict Static Typing**: All code and tests must pass `mypy --strict` with zero type ignores or `Any` escapes.
2. **100% Test Coverage**: `src/taipanstack/core/compat.py` must achieve 100% line and branch coverage.
3. **Zero Dead Code**: `_get_version_tier()` remains unchanged; `PY314` (`PY_VERSION >= (3, 14)`) automatically routes 3.15 to `VersionTier.CUTTING_EDGE`.
4. **YAGNI Compliance**: No speculative feature flags (e.g. `has_frozendict`) are introduced.
5. **Full Quality Gate**: `make all` and `NO_MKDOCS_2_WARNING=1 poetry run mkdocs build --strict` must succeed with zero warnings or errors.
