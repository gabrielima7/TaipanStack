<div align="center">

# ⚡ Stack
### The Modern Python Foundation

[![CI](https://github.com/gabrielima7/Stack/actions/workflows/ci.yml/badge.svg)](https://github.com/gabrielima7/Stack/actions)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Code Style](https://img.shields.io/badge/Code%20Style-Ruff-000000)](https://github.com/astral-sh/ruff)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

*Launch secure, high-performance Python applications in seconds.*

[Features](#-features) • [Quick Start](#-quick-start) • [Structure](#-project-structure) • [Contributing](#-contributing)

</div>

---

## 🚀 Features

Stack provides a battle-tested foundation for production-grade Python projects, combining speed, security, and developer experience.

- **🛡️ Security First**: Built-in defenses against path traversal, command injection, and more.
- **⚡ High Performance**: Optimized with `uvloop`, `orjson`, and `Pydantic v2`.
- **🔧 Developer Experience**: Pre-configured `Ruff`, `Mypy`, and `Poetry` for seamless workflows.
- **🏗️ Robust Architecture**: Solid patterns for logging, metrics, retry logic, and circuit breakers.

## 🏁 Quick Start

Get your environment up and running in moments.

### Prerequisites
- Python 3.10+
- [Poetry](https://python-poetry.org/)

### Installation

```bash
git clone https://github.com/gabrielima7/Stack.git
cd Stack
poetry install
```

### Running Tests
Ensure everything is working correctly:

```bash
poetry run pytest
```

## 📂 Project Structure

A clean, opinionated structure designed for scalability.

```text
Stack/
├── src/stack/
│   ├── config/       # Configuration management
│   ├── security/     # Guards, sanitizers, and validators
│   └── utils/        # Resilient utilities (filesystem, subprocess, etc.)
├── tests/            # Comprehensive test suite (97% coverage)
└── pyproject.toml    # Modern dependency management
```

## 🛠️ Built With

The best-in-class tools powering your stack:

| Core | Quality |
|------|---------|
| **Pydantic V2** | **Ruff** (Linting & Formatting) |
| **Orjson** | **Mypy** (Static Typing) |
| **Uvloop** | **Bandit** (Security Analysis) |
| **Structlog** | **Pytest** (Testing Framework) |

## 🤝 Contributing

We welcome contributions! Please check our [Contributing Guide](CONTRIBUTING.md) for details.

## 📝 License

This project is open-sourced under the [MIT License](LICENSE).
