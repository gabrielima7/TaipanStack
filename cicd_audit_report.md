# TaipanStack CI/CD Pipeline Audit Report

## 1. Insights from `agents.md` regarding deployment and operations
The `agents.md` explicitly mandates a Zero-Bypass culture. Operations require strict typing (no `Any`), explicit error handling via the `Result` pattern, and layered isolation (Import Linter). Continuous validation via `make all` must enforce 100% test coverage with no exceptions or skipping mechanisms allowed. The CI pipelines must reflect real execution using genuine inputs and enforce security and code health across every commit and PR. Memory directives indicated a deleted `ci-push-benchmark.yml` violated the Zero Bypass rule by dropping the performance regression guard.

## 2. Deleted Pipelines/Steps and Justification
None of the existing pipelines or steps were permanently deleted during this refactor because they all align with the necessary jobs defined in `agents.md`. However, I discovered that the `ci-push-benchmark.yml` had been wrongfully deleted in previous changes, which bypasses the performance regression check. It has been successfully restored to enforce a `105%` alert threshold.

## 3. New Naming Convention
A strict naming convention was verified and standardized across all pipeline jobs and steps:
- **`[Setup]`**: Setting up environments (e.g., checkout, Python, Poetry cache).
- **`[Build]`**: Building packages and containers (e.g., Docker, Poetry build).
- **`[Test]`**: Running unit tests, benchmarks, integration, and property tests.
- **`[Lint]`**: Code quality checks, import checks, formatting, type checking, structure outputs, and artifact uploads (except security).
- **`[Audit]`**: Security and dependency auditing (e.g., Bandit, Pip-Audit, Semgrep, SBOM generation).
- **`[Deploy]`**: Releasing artifacts, PyPI uploads, GitHub Pages documentation, and SBOM signing.
- **`[Artifact]`**: Naming identifiers for job artifacts (e.g., HTML Coverage, Performance, SBOM).

## 4. Summary of Self-Correction Loops
1.  **Issue:** `ci-push-benchmark.yml` was absent from the current `main` commit.
    **Fix:** Restored `ci-push-benchmark.yml` from a previous Git commit (`3012123`).
2.  **Issue:** `ci-push-benchmark.yml` had an `alert-threshold` of `"150%"`, making it too permissive for the 5% degradation limit specified in memory.
    **Fix:** Using `sed`, updated the threshold to `"105%"`.
3.  **Validation:** Verified the absence of bypass strings such as `continue-on-error: true` or `echo "pass"`. Executed `make all` and verified all tests, lint checks, typecheck, and security checks executed fully and effectively.

## 5. Final CI/CD Configuration Files
Here are the restored/fixed configurations (others remain standard and correct):

### .github/workflows/ci-push-benchmark.yml
```yaml
# =============================================================================
# TaipanStack — Performance Regression Guard
# =============================================================================
# Runs pytest-benchmark on every push/PR and fails CI if any benchmark
# degrades more than 5% compared to the main branch baseline.
# =============================================================================

name: ci-push-benchmark

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

concurrency:
  group: ci-push-benchmark-${{ github.ref }}
  cancel-in-progress: false

permissions:
  contents: write # needed to push benchmark data to gh-pages
  pull-requests: write # needed to comment on PRs

jobs:
  benchmark:
    name: "[Test] Run Benchmarks"
    runs-on: ubuntu-latest

    steps:
      - name: "[Setup] Checkout code"
        uses: actions/checkout@v4

      - name: "[Setup] Set up Python"
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: "[Setup] Install Poetry"
        run: pipx install poetry

      - name: "[Setup] Configure Poetry"
        run: poetry config virtualenvs.in-project true

      - name: "[Setup] Cache dependencies"
        uses: actions/cache@v4
        with:
          path: .venv
          key: bench-${{ runner.os }}-poetry-${{ hashFiles('**/poetry.lock') }}
          restore-keys: |
            bench-${{ runner.os }}-poetry-

      - name: "[Setup] Install dependencies"
        run: poetry install --with dev --sync

      - name: "[Test] Run benchmarks"
        run: |
          poetry run pytest tests/test_benchmarks_operations.py \
            --benchmark-only \
            --benchmark-json=benchmark-result.json \
            --benchmark-min-rounds=100 \
            --benchmark-warmup=on \
            --no-cov \
            -v

      # ── Bootstrap gh-pages if it doesn't exist on remote ───────────
      - name: "[Deploy] Ensure gh-pages branch exists"
        run: |
          # Check if gh-pages exists on the REMOTE (not locally)
          if git ls-remote --exit-code --heads origin gh-pages > /dev/null 2>&1; then
            echo "✅ Remote gh-pages branch already exists, fetching..."
            git fetch origin gh-pages:gh-pages
          else
            echo "🆕 Creating gh-pages branch for the first time..."
            git config user.name "github-actions[bot]"
            git config user.email "github-actions[bot]@users.noreply.github.com"
            git checkout --orphan gh-pages
            git reset --hard
            git commit --allow-empty -m "chore: initialize gh-pages for benchmarks"
            git push origin gh-pages
            # Return to main: fetch remote tracking ref first, then recreate local branch
            git fetch origin main:main 2>/dev/null || git checkout -B main "refs/remotes/origin/main"
          fi

      # ── Compare & Store ──────────────────────────────────────────────
      - name: "[Test] Store benchmark result"
        uses: benchmark-action/github-action-benchmark@v1
        with:
          name: "[Artifact] TaipanStack Performance"
          tool: pytest
          output-file-path: benchmark-result.json
          # Push baseline data to gh-pages on main branch pushes
          auto-push: ${{ github.event_name == 'push' && github.ref == 'refs/heads/main' }}
          gh-pages-branch: gh-pages
          benchmark-data-dir-path: dev/bench
          # Fail CI if performance degrades more than 5% (accounts for runner variance)
          alert-threshold: "105%"
          fail-on-alert: true
          # Comment on PR with comparison
          comment-on-alert: true
          github-token: ${{ secrets.GITHUB_TOKEN }}
          # Alert when threshold exceeded
          alert-comment-cc-users: "@gabrielima7"
```

All CI pipelines now enforce the zero-bypass rule and maintain 100% functional integrity.
