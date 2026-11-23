# CI/CD & Release Automation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement automated version bump with `.10` rollover, categorized GitHub release creation, PyPI/GHCR build & publication without cancelling running jobs, and a protected deploy step.

**Architecture:** A standalone Python script `scripts/bump_version.py` handles parsing and bumping versions adhering to the `.10` rollover rule (`x.y.10 -> x.(y+1).0`) with unit tests. GitHub Actions workflow `.github/workflows/ci-release-publish.yml` unifies validation, versioning commit with `[skip ci]`, tag creation, PyPI publish with Cosign/SBOM, Docker build to GHCR, and a protected `production` environment deploy stage.

**Tech Stack:** Python 3.11+, Poetry, GitHub Actions, PyPI Trusted Publishing, Sigstore Cosign, Syft (CycloneDX), Docker & GitHub Packages (GHCR), pytest.

**Spec:** `docs/superpowers/specs/2026-11-23-ci-cd-release-automation-design.md`

## Global Constraints
- Target version to update immediately: `v0.7.0`.
- Rollover rule: Patch numbers strictly up to 10 (`x.y.10 -> x.(y+1).0`).
- Concurrency: `cancel-in-progress: false` on publish/release pipelines.
- Deploy environment: `environment: production` depending on publish jobs.
- All version changes committed back to `main` must include `[skip ci]`.

## Review Focus
- Input `0.6.10` rolls over to `0.7.0`, not `0.6.11`.
- Input `0.7.0` increments to `0.7.1`.
- Tags with or without leading `v` prefix are handled consistently (`v0.7.0` vs `0.7.0`).
- Non-conforming semver strings raise a descriptive ValueError.
- Workflow prevents recursive triggering when committing back to `main` via `[skip ci]`.

---

### Task 1: Version Calculation Script and Unit Tests (Rollover .10)

**Files:**
- Create: `scripts/bump_version.py`
- Create: `tests/unit/test_version_bump.py`

**Interfaces:**
- Produces: `calculate_next_version(current_version: str) -> str`
- Produces: `update_project_files(new_version: str, dry_run: bool = False) -> None`

- [ ] **Step 1: Write failing unit test for `calculate_next_version`**

```python
# tests/unit/test_version_bump.py
import pytest
from scripts.bump_version import calculate_next_version

def test_bump_standard_patch():
    assert calculate_next_version("0.7.0") == "0.7.1"
    assert calculate_next_version("v0.7.0") == "0.7.1"
    assert calculate_next_version("0.6.9") == "0.6.10"

def test_bump_rollover_ten_to_minor():
    assert calculate_next_version("0.6.10") == "0.7.0"
    assert calculate_next_version("v0.6.10") == "0.7.0"
    assert calculate_next_version("1.2.10") == "1.3.0"

def test_invalid_version_raises():
    with pytest.raises(ValueError):
        calculate_next_version("invalid-version")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `poetry run pytest tests/unit/test_version_bump.py -v`
Expected: FAIL with ModuleNotFoundError or import error for `scripts.bump_version`.

- [ ] **Step 3: Implement `calculate_next_version` and CLI in `scripts/bump_version.py`**

Implement regex matching `^v?(\d+)\.(\d+)\.(\d+)$`.
If `patch < 10`: `patch += 1`, return `f"{major}.{minor}.{patch}"`.
If `patch >= 10`: `minor += 1`, `patch = 0`, return `f"{major}.{minor}.0"`.
Provide file updater for `pyproject.toml` and `src/taipanstack/__init__.py`.

- [ ] **Step 4: Run test to verify it passes**

Run: `poetry run pytest tests/unit/test_version_bump.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/bump_version.py tests/unit/test_version_bump.py
git commit -m "feat(version): add bump_version script with .10 rollover rule and tests"
```

---

### Task 2: Update Project Version to v0.7.0

**Files:**
- Modify: `pyproject.toml:3`
- Modify: `src/taipanstack/__init__.py:8`
- Modify: `CHANGELOG.md`
- Create: `docs/releases/v0.7.0.md`
- Modify: `mkdocs.yml`

**Interfaces:**
- Consumes: `0.7.0` version string from Task 1

- [ ] **Step 1: Write test verifying package version matches `0.7.0`**

In `tests/unit/test_version_sync.py`:
```python
import tomllib
from pathlib import Path
import taipanstack

def test_version_consistency():
    pyproject_path = Path("pyproject.toml")
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)
    toml_version = data["project"]["version"]
    assert toml_version == "0.7.0"
    assert taipanstack.__version__ == "0.7.0"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `poetry run pytest tests/unit/test_version_sync.py -v`
Expected: FAIL (`assert '0.6.4' == '0.7.0'`)

- [ ] **Step 3: Update version files to 0.7.0**

Update `pyproject.toml` version to `"0.7.0"`.
Update `src/taipanstack/__init__.py` `__version__ = "0.7.0"`.
Add `## [0.7.0] - 2026-11-23` in `CHANGELOG.md`.
Create `docs/releases/v0.7.0.md` and register in `mkdocs.yml`.

- [ ] **Step 4: Run test to verify it passes**

Run: `poetry run pytest tests/unit/test_version_sync.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml src/taipanstack/__init__.py CHANGELOG.md docs/releases/v0.7.0.md mkdocs.yml tests/unit/test_version_sync.py
git commit -m "chore(release): bump version to v0.7.0"
```

---

### Task 3: Release Categorization Configuration

**Files:**
- Create: `.github/release.yml`

**Interfaces:**
- Produces: GitHub Release note category definitions (`Features`, `Changes`, `Fixes`, `Removals`)

- [ ] **Step 1: Create `.github/release.yml` with required categories**

```yaml
changelog:
  categories:
    - title: "✨ Novas Funcionalidades"
      labels: ["feature", "enhancement", "feat"]
    - title: "🔄 Alterações"
      labels: ["change", "refactor", "chore", "perf"]
    - title: "🐛 Correções"
      labels: ["bug", "fix", "hotfix"]
    - title: "🗑️ Remoções e Depreciações"
      labels: ["deprecation", "removal", "breaking"]
```

- [ ] **Step 2: Validate yaml syntax**

Run: `python -c "import yaml; yaml.safe_load(open('.github/release.yml'))"`
Expected: No errors.

- [ ] **Step 3: Commit**

```bash
git add .github/release.yml
git commit -m "ci(release): add GitHub release category configuration"
```

---

### Task 4: Unified CI/CD & Delivery Workflow

**Files:**
- Modify: `.github/workflows/ci-release-publish.yml`

**Interfaces:**
- Consumes: `scripts/bump_version.py`
- Consumes: `.github/release.yml`

- [ ] **Step 1: Implement full pipeline in `.github/workflows/ci-release-publish.yml`**

Include:
- Triggers: `push: branches: [main]`, `push: tags: ['v*']`, `workflow_dispatch`.
- Concurrency: `group: release-${{ github.ref }}`, `cancel-in-progress: false`.
- Job `validate`: Python test suite matrix or fast validation on Python 3.11.
- Job `version-and-release`: Runs if on `main` branch. Calculates next version with `scripts/bump_version.py`, updates files, commits with `[skip ci]`, creates git tag `vX.Y.Z` and GitHub Release using `softprops/action-gh-release@v3` with categorized release notes.
- Job `pypi-publish`: Runs on `main` (after `version-and-release`) or on tag `v*`. `environment: pypi`. Poetry build, upload via `pypa/gh-action-pypi-publish`, SBOM with Syft, signing with Cosign.
- Job `ghcr-publish`: Runs on `main` or tag `v*`. `environment: production`. Builds Docker image from `Dockerfile` and pushes to `ghcr.io/${{ github.repository }}` tagged with the version and `latest`.
- Job `deploy`: `needs: [pypi-publish, ghcr-publish]`. `environment: production`. Verifies packages are accessible and updates release notes with final digests.

- [ ] **Step 2: Validate workflow yaml syntax**

Run: `python -c "import yaml; yaml.safe_load(open('.github/workflows/ci-release-publish.yml'))"`
Expected: Clean load with 0 errors.

- [ ] **Step 3: Test dry-run of version bump locally**

Run: `poetry run python scripts/bump_version.py --dry-run`
Expected: Displays current version and expected next version.

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/ci-release-publish.yml
git commit -m "ci: implement unified release, pypi, ghcr and protected deploy pipeline"
```
