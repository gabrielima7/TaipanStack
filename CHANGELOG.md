# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[2.0.0]: https://github.com/gabrielima7/TaipanStack/compare/v0.1.0...v2.0.0
[Unreleased]: https://github.com/gabrielima7/TaipanStack/compare/v2.0.0...HEAD
[0.1.0]: https://github.com/gabrielima7/TaipanStack/releases/tag/v0.1.0
