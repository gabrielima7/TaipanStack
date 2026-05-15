# TaipanStack CI/CD Audit Report

## Context Analysis (`agents.md`)
- The project mandates a zero-bypass CI/CD process (`fail_under = 100`, no dummy checks).
- Testing needs to be real, typing is strict, and security controls are mandatory.
- Naming conventions require `ci-<trigger>-<action>.yml` for workflow files and `[Phase] Description` for jobs/steps.

## Deleted Pipelines & Steps
- No pipelines were permanently deleted; however, missing/untracked files like `ci-push-benchmark.yml` and its associated `tests/test_benchmarks_operations.py` were fully restored to prevent missing code paths.
- We intentionally preserved all checks (linting, testing, benchmarking, documentation deployment, SLSA release) but ensured they function properly and fail when they must.
- The `pytest-benchmark` dependency was explicitly added back into `pyproject.toml`'s dev dependencies to ensure the `ci-push-benchmark.yml` action could run without errors, fixing a true CI/CD failure where it reported `unrecognized arguments`.

## New Naming Convention Enforced
- `ci-push-main.yml` -> `ci-push-test.yml`
- `ci-workflow-run-docs.yml` -> `ci-workflow_run-deploy.yml`
- Step definitions inside workflows were already well aligned with the `[Setup]`, `[Lint]`, `[Test]`, `[Audit]`, `[Build]`, `[Deploy]`, and `[Artifact]` standards, so they were left intact.

## Self-Correction Loop
- Attempted to run the `ci-push-benchmark.yml`'s pytest command locally, which failed. The error clearly showed `unrecognized arguments: --benchmark-only`, exposing that `pytest-benchmark` was missing from `pyproject.toml`. Added it to the `dev` dependency group and re-installed.
- Modified the threshold for the benchmark workflow back to `105%` to adhere strictly to the 5% degradation limit memory guideline.
- Ran `make all` validation after restoring `test_benchmarks_operations.py`, proving that 100% test coverage and lint checks completely pass.

## Final Result
- Workflows are properly named.
- `make all` succeeds.
- CI/CD bypasses don't exist.
