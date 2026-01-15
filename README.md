<div align="center">

# ⚡ Stack
### The Modern Python Foundation

[![CI](https://github.com/gabrielima7/Stack/actions/workflows/ci.yml/badge.svg)](https://github.com/gabrielima7/Stack/actions)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Coverage](https://img.shields.io/badge/Coverage-97%25-brightgreen)](https://github.com/gabrielima7/Stack)
[![Code Style](https://img.shields.io/badge/Code%20Style-Ruff-000000)](https://github.com/astral-sh/ruff)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

*Launch secure, high-performance Python applications in seconds.*

[Features](#-features) • [Quick Start](#-quick-start) • [Structure](#-project-structure) • [DevSecOps](#-devsecops) • [Contributing](#-contributing)

</div>

---

## 🚀 Features

Stack provides a battle-tested foundation for production-grade Python projects, combining speed, security, and developer experience.

- **🛡️ Security First**: Built-in defenses against path traversal, command injection, and more.
- **⚡ High Performance**: Optimized with `uvloop`, `orjson`, and `Pydantic v2`.
- **🔧 Developer Experience**: Pre-configured `Ruff`, `Mypy`, and `Poetry` for seamless workflows.
- **🏗️ Robust Architecture**: Solid patterns for logging, metrics, retry logic, and circuit breakers.
- **🎯 Result Types**: Rust-style `Ok`/`Err` pattern for explicit error handling.
- **📐 Architecture Enforcement**: Import Linter contracts to maintain clean boundaries.

## 🏁 Quick Start

Get your environment up and running in moments.

### Prerequisites
- Python 3.10+
- [Poetry](https://python-poetry.org/)

### Installation

```bash
git clone https://github.com/gabrielima7/Stack.git
cd Stack
poetry install --with dev
```

### Running Tests
Ensure everything is working correctly:

```bash
make test          # Run tests with coverage
make all           # Run all quality checks
make lint-imports  # Verify architecture
```

## 📂 Project Structure

A clean, opinionated structure designed for scalability.

```text
Stack/
├── src/stack/
│   ├── core/         # Result types, functional patterns
│   ├── config/       # Configuration management
│   ├── security/     # Guards, sanitizers, and validators
│   └── utils/        # Resilient utilities (filesystem, subprocess, etc.)
├── tests/            # Comprehensive test suite (97% coverage)
├── pyapp/            # Standalone executable builder (PyApp)
├── .importlinter     # Architecture contracts
└── pyproject.toml    # Modern dependency management
```

## 🔐 DevSecOps

Stack integrates security and quality checks throughout the development lifecycle:

| Category | Tools |
|----------|-------|
| **SAST** | Bandit, Semgrep |
| **SCA** | Safety, pip-audit |
| **Type Safety** | Mypy (strict mode) |
| **Linting** | Ruff |
| **Architecture** | Import Linter |
| **Testing** | Pytest, Hypothesis |

### Result Types (Error Handling)

```python
from stack.core.result import safe, Ok, Err

@safe
def divide(a: int, b: int) -> float:
    return a / b

match divide(10, 0):
    case Err(e): print(f"Error: {e}")
    case Ok(v): print(f"Result: {v}")
```

## 🛠️ Built With

The best-in-class tools powering your stack:

| Core | Quality |
|------|---------|
| **Pydantic V2** | **Ruff** (Linting & Formatting) |
| **Orjson** | **Mypy** (Static Typing) |
| **Uvloop** | **Bandit** (Security Analysis) |
| **Structlog** | **Pytest** (Testing Framework) |
| **Result** | **Import Linter** (Architecture) |

## 🤝 Contributing

We welcome contributions! Please check our [Contributing Guide](CONTRIBUTING.md) for details.

## 📝 License

This project is open-sourced under the [MIT License](LICENSE).
