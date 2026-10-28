# Tasks: Python 3.15 Integration and Runtime Compatibility

**Input**: Design documents from `/specs/001-py315-compat/` and `docs/designs/python_315_compatibility.md`

**Prerequisites**: `plan.md` (required), `spec.md` (required for user stories), `constitution.md`

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (`[US1]`, `[US2]`, `[US3]`)
- Exact file paths included in every description

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Environment verification and baseline health check

- [X] T001 Verify active worktree and clean baseline environment (`git status`, `poetry env info`)
- [X] T002 Run baseline quality gate to confirm green status before changes (`poetry run ruff check src/ tests/`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Confirm baseline compatibility test suite behavior before applying Python 3.15 extensions

**⚠️ CRITICAL**: Must confirm current baseline tests pass with 100% coverage prior to adding 3.15 branches.

- [X] T003 Verify existing compat constants and baseline test coverage (`poetry run pytest tests/test_compat_standard_expected.py -v --cov=taipanstack.core.compat`)

**Checkpoint**: Foundation verified - User story implementation can now begin.

---

## Phase 3: User Story 1 - Deterministic Python 3.15 Runtime Detection (Priority: P1) 🎯 MVP

**Goal**: Introduce `PY315: Final[bool] = PY_VERSION >= (3, 15)` in `src/taipanstack/core/compat.py`, export it via `__all__`, ensure `VersionTier.CUTTING_EDGE` natively covers Python 3.15 without changes to `_get_version_tier()`, and verify 100% test coverage with real assertions and simulated mock tests.

**Independent Test**: `poetry run pytest tests/test_compat_standard_expected.py -v --cov=taipanstack.core.compat --cov-report=term-missing` and `poetry run mypy src/taipanstack/core/compat.py --strict`

### Tests for User Story 1 🧪
- [X] T004 [US1] Add unit test `test_compat_standard_compat_py315_constant` and `__all__` assertion in `tests/test_compat_standard_expected.py`
- [X] T005 [US1] Add simulated Python 3.15 mock test `test_compat_standard_compat_features_mock_315` in `tests/test_compat_standard_expected.py`

### Implementation for User Story 1
- [X] T006 [US1] Declare constant `PY315: Final[bool] = PY_VERSION >= (3, 15)` and add `"PY315"` to `__all__` in `src/taipanstack/core/compat.py`
- [X] T007 [US1] Run unit tests and strict type checking to verify 100% branch and statement coverage (`poetry run pytest tests/test_compat_standard_expected.py -v --cov=taipanstack.core.compat --cov-report=term-missing` and `poetry run mypy src/taipanstack/core/compat.py --strict`)

**Checkpoint**: User Story 1 is fully functional and testable independently.

---

## Phase 4: User Story 2 - Package Metadata Alignment (Priority: P2)

**Goal**: Update package classifiers in `pyproject.toml` and documentation shield badges in `README.md` to officially declare Python 3.15 support.

**Independent Test**: `poetry check` passes cleanly, and `git diff` confirms exact badge text in `README.md`.

### Implementation for User Story 2
- [X] T008 [P] [US2] Append `"Programming Language :: Python :: 3.15"` to `classifiers` array under `[project]` in `pyproject.toml`
- [X] T009 [P] [US2] Update Python version shield badge to include `3.15` in `README.md`
- [X] T010 [US2] Validate packaging metadata and configuration with `poetry check`

**Checkpoint**: User Stories 1 and 2 work independently and packaging metadata is validated.

---

## Phase 5: User Story 3 - Automated CI Pipeline Validation (Priority: P3)

**Goal**: Add `"3.15"` to the test matrix in `.github/workflows/ci-push-validate.yml` with failure isolation (`continue-on-error: true`).

**Independent Test**: YAML syntax validation passes, and matrix includes `"3.15"`.

### Implementation for User Story 3
- [X] T011 [US3] Add `"3.15"` to `strategy.matrix.python-version` with `continue-on-error: true` in `.github/workflows/ci-push-validate.yml`
- [X] T012 [US3] Validate CI workflow YAML syntax and matrix configuration in `.github/workflows/ci-push-validate.yml`

**Checkpoint**: All user stories are implemented and CI matrix incorporates failure-isolated Python 3.15 runner jobs.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Repository-wide quality gates, formatting, strict static typing, and documentation build.

- [X] T013 Run full static analysis and formatting check across repository (`poetry run ruff check src/ tests/ taipanstack_bootstrapper.py` and `poetry run ruff format --check src/ tests/ taipanstack_bootstrapper.py`)
- [X] T014 Run repository-wide strict static type checking (`poetry run mypy src/ --strict`)
- [X] T015 Run full strict documentation build (`NO_MKDOCS_2_WARNING=1 poetry run mkdocs build --strict`)
- [X] T016 Execute master quality gate check (`make all`)

---

## Dependencies & Execution Order

### Phase Dependencies
- **Setup (Phase 1)**: No dependencies - starts immediately.
- **Foundational (Phase 2)**: Depends on Setup - verifies baseline test coverage.
- **User Story 1 (Phase 3)**: Core runtime compatibility and test coverage. (MVP)
- **User Story 2 (Phase 4)**: Package metadata & README badge (depends on US1).
- **User Story 3 (Phase 5)**: CI matrix configuration (depends on US1).
- **Polish (Phase 6)**: Final verification across all phases (`make all`, mkdocs).

### Parallel Opportunities
- T008 (`pyproject.toml`) and T009 (`README.md`) can execute in parallel.
- US2 and US3 can proceed concurrently once US1 completes.

---

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Complete Phase 1: Setup (T001, T002)
2. Complete Phase 2: Foundational (T003)
3. Complete Phase 3: User Story 1 (T004-T007)
4. **Validate MVP**: `poetry run pytest tests/test_compat_standard_expected.py -v --cov=taipanstack.core.compat`

### Incremental Delivery
1. Core runtime detection (`src/taipanstack/core/compat.py`) + tests -> MVP!
2. Packaging metadata (`pyproject.toml`) + `README.md` -> PyPI readiness
3. CI test matrix (`.github/workflows/ci-push-validate.yml`) -> Automated verification
4. Master gate check (`make all`) -> Production merge readiness
