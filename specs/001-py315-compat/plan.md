# Implementation Plan: Python 3.15 Integration and Runtime Compatibility

**Branch**: `001-py315-compat` | **Date**: 2026-10-27 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-py315-compat/spec.md` and ratified design from `docs/designs/python_315_compatibility.md`.

## Summary

Establishes official compatibility, static version detection (`PY315`), packaging metadata classifiers, and continuous integration validation for Python 3.15 (PEP 790). The design introduces `PY315: Final[bool] = PY_VERSION >= (3, 15)` in `src/taipanstack/core/compat.py`, exports it via `__all__`, relies on existing `_get_version_tier()` mapping to `VersionTier.CUTTING_EDGE`, updates `pyproject.toml` classifiers, and configures GitHub Actions with failure isolation (`continue-on-error: true`).

## Technical Context

**Language/Version**: Python 3.11, 3.12, 3.13, 3.14, and 3.15 (targeting PEP 790 release October 9, 2026).

**Primary Dependencies**: None (core standard library `sys.version_info` detection). Third-party dependencies (`orjson`, `uvloop`, `argon2-cffi`, `msgpack`) consumed from upstream PyPI wheels.

**Storage**: N/A

**Testing**: `pytest`, `pytest-cov`, `mypy --strict`, `ruff`

**Target Platform**: Linux, macOS, Windows

**Project Type**: Core foundational framework / library

**Performance Goals**: Zero runtime performance overhead for version constants (evaluated at module import time).

**Constraints**: Strict backward compatibility with Python 3.11-3.14. 100% test coverage mandatory (`make all`). No `Any` escapes or type-ignores (`mypy --strict`). Zero dead code.

**Scale/Scope**: 4 files modified (`src/taipanstack/core/compat.py`, `tests/test_compat_standard_expected.py`, `pyproject.toml`, `.github/workflows/ci-push-validate.yml`), 1 documentation file (`README.md`).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

* **Pillar 1: Strict Static Typing**: Compliant. `PY315: Final[bool]` is strictly typed. All tests strictly typed. Zero `Any` escapes.
* **Pillar 2: Explicit Contracts**: Compliant. Exported in `__all__`.
* **Pillar 3: 100% Test Coverage**: Compliant. Real constant assertion + simulated mock test on pre-3.15 interpreters covers 100% lines and branches.
* **Pillar 4: YAGNI & Simplicity**: Compliant. Speculative `has_frozendict` stripped; `_get_version_tier()` left untouched because `(3, 15) >= (3, 14)` evaluates to `True` natively.

## Project Structure

### Documentation (this feature)

```text
specs/001-py315-compat/
├── spec.md              # Feature specification
├── plan.md              # This file
└── tasks.md             # Implementation tasks
```

### Source Code Layout

```text
src/
└── taipanstack/
    └── core/
        └── compat.py    # Add PY315 constant and __all__ export

tests/
└── test_compat_standard_expected.py  # Add PY315 constant test & simulated mock test

pyproject.toml           # Add Python 3.15 classifier
README.md                # Update Python version badge
.github/workflows/
└── ci-push-validate.yml # Add 3.15 to matrix with continue-on-error: true
```

## Phasing & Verification Strategy

- **Phase 1**: Core Runtime Detection (`src/taipanstack/core/compat.py`)
  - Checkpoint 1: `poetry run ruff check src/taipanstack/core/compat.py`, `poetry run mypy src/taipanstack/core/compat.py --strict`
- **Phase 2**: Test Suite Expansion & Mock Verification (`tests/test_compat_standard_expected.py`)
  - Checkpoint 2: `poetry run pytest tests/test_compat_standard_expected.py -v --cov=taipanstack.core.compat --cov-report=term-missing`
- **Phase 3**: Package Metadata & Documentation (`pyproject.toml`, `README.md`)
  - Checkpoint 3: `poetry check`, `git diff pyproject.toml README.md`
- **Phase 4**: CI Workflow Configuration (`.github/workflows/ci-push-validate.yml`)
  - Checkpoint 4: YAML syntax validation
- **Phase 5**: Full Quality Gate Check
  - Checkpoint 5: `make all`, `NO_MKDOCS_2_WARNING=1 poetry run mkdocs build --strict`
