# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

## [2.0.0] - 2026-02-03

### Changed
- **BREAKING**: Renamed project from "Stack" to "TaipanStack"
- **BREAKING**: All imports changed from `stack.*` to `taipanstack.*`
- Renamed `stack_bootstrapper.py` to `taipanstack_bootstrapper.py`
- Updated all documentation with new project name
- Added PyPI package configuration

### Added
- PyPI package metadata and URLs
- Package entry points for distribution

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

[0.3.0]: https://github.com/gabrielima7/TaipanStack/compare/v0.2.9...v0.3.0
[0.2.9]: https://github.com/gabrielima7/TaipanStack/compare/v0.2.8...v0.2.9
[0.2.8]: https://github.com/gabrielima7/TaipanStack/compare/v2.0.0...v0.2.8
[2.0.0]: https://github.com/gabrielima7/TaipanStack/compare/v0.1.0...v2.0.0
[Unreleased]: https://github.com/gabrielima7/TaipanStack/compare/v0.3.0...HEAD
[0.1.0]: https://github.com/gabrielima7/TaipanStack/releases/tag/v0.1.0
