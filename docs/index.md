---
description: "TaipanStack — modern, secure Python foundation with Result types, security guards, and DevSecOps tooling."
hide:
  - navigation
---

# 🐍 TaipanStack

**The Modern Python Foundation** — Launch secure, high-performance Python applications in seconds.

[![CI](https://github.com/gabrielima7/TaipanStack/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/gabrielima7/TaipanStack/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen?style=flat&logo=codecov)](https://github.com/gabrielima7/TaipanStack)
[![PyPI](https://img.shields.io/pypi/v/taipanstack?style=flat&logo=pypi&logoColor=white)](https://pypi.org/project/taipanstack/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](https://github.com/gabrielima7/TaipanStack/blob/main/LICENSE)

---

## ✨ Why TaipanStack?

> **"Write less, build better."**

TaipanStack is a battle-tested foundation for production-grade Python projects that combines **security**, **performance**, and **developer experience** into a single, cohesive toolkit.

<div class="grid cards" markdown>

-   :shield: **Security First**

    ---

    Path traversal protection, command injection guards, input sanitizers & validators, secret detection, SBOM + SLSA attestation.

-   :zap: **High Performance**

    ---

    `uvloop` async event loop, `orjson` fast JSON, `Pydantic v2` validation, pytest-benchmark regression detection.

-   :dart: **Rust-Style Error Handling**

    ---

    `Ok`/`Err` Result types, explicit error propagation, pattern matching, no silent failures.

-   :wrench: **Developer Experience**

    ---

    Pre-configured quality tools, **100% code coverage** (1030 tests), architecture enforcement, hardened Docker template.

</div>

---

## 🚀 Quick Start

### From PyPI

```bash
pip install taipanstack
```

### From Source

```bash
git clone https://github.com/gabrielima7/TaipanStack.git
cd TaipanStack
poetry install --with dev
```

### Verify Installation

```bash
# Run tests with 100% coverage
make test

# Check architecture contracts
make lint-imports

# Run security scans
make security
```

---

## 📚 API Highlights

### Result Types

```python
from taipanstack.core.result import Result, Ok, Err, safe

@safe
def divide(a: int, b: int) -> float:
    return a / b

match divide(10, 0):
    case Ok(value):
        print(f"Result: {value}")
    case Err(error):
        print(f"Error: {error}")
```

### Security Guards

```python
from taipanstack.security.guards import guard_path_traversal, guard_command_injection

safe_path = guard_path_traversal(user_input, base_dir="/app/data")
safe_cmd = guard_command_injection(["git", "clone", repo_url], allowed_commands=["git"])
```

### Retry + Circuit Breaker

```python
from taipanstack.utils.retry import retry
from taipanstack.utils.circuit_breaker import circuit_breaker

@circuit_breaker(failure_threshold=5, timeout=30)
@retry(max_attempts=3, on=(ConnectionError, TimeoutError))
def call_external_service() -> dict:
    return service.call()
```

### Intelligent Caching

```python
from taipanstack.utils.cache import cached
from taipanstack.core.result import Result

@cached(ttl=60)
async def get_user_data(user_id: int) -> Result[dict, Exception]:
    return await db.fetch(user_id) # Only Ok() results are cached
```

### Fallbacks & Timeouts

```python
from taipanstack.utils.resilience import fallback, timeout
from taipanstack.core.result import Result

@fallback(fallback_value={"status": "offline"}, exceptions=(TimeoutError,))
@timeout(seconds=5.0)
async def fetch_remote_status() -> Result[dict, Exception]:
    return await api.get_status()
```

---

## 📐 Architecture

```
                    ┌─────────────────────────────────────┐
                    │             Application             │
                    └─────────────────┬───────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          ▼                           ▼                           ▼
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│    Security     │       │     Config      │       │     Utils       │
│ guards, saniti- │       │    models,      │       │  logging, retry │
│ zers, validators│       │   generators    │       │ metrics, fs     │
└────────┬────────┘       └────────┬────────┘       └────────┬────────┘
         │                         │                         │
         └─────────────────────────┼─────────────────────────┘
                                   ▼
                    ┌─────────────────────────────────────┐
                    │              Core                   │
                    │    Result types, base patterns      │
                    └─────────────────────────────────────┘
```

[Read the full architecture guide →](architecture.md)

---

## 🔐 DevSecOps

| Category | Tools | Purpose |
|----------|-------|---------|
| **SAST** | Bandit, Semgrep + custom rules | Static Application Security Testing |
| **SCA** | Safety, pip-audit | Dependency vulnerability scanning |
| **SBOM** | Syft (CycloneDX) | Software Bill of Materials |
| **SLSA** | Cosign (Sigstore) | Artifact signing & attestation |
| **Types** | Mypy (strict) | Compile-time type checking |
| **Lint** | Ruff | Lightning-fast linting & formatting |
| **Arch** | Import Linter | Dependency rule enforcement |
| **Test** | Pytest, Hypothesis, mutmut | Property-based & mutation testing |
| **Perf** | pytest-benchmark | Performance regression detection |

---

## 📊 Live Reports

| Report | Description |
|--------|-------------|
| [🧪 Coverage Report](https://gabrielima7.github.io/TaipanStack/htmlcov/) | Full HTML coverage report — 100% (1030 tests) |
| [⚡ Benchmark Dashboard](https://gabrielima7.github.io/TaipanStack/dev/bench/) | Performance history & regression graphs |

---

## 🤝 Contributing

Contributions are welcome! See the [Contributing Guide](https://github.com/gabrielima7/TaipanStack/blob/main/CONTRIBUTING.md) for details.

## 📝 License

Open-sourced under the [MIT License](https://github.com/gabrielima7/TaipanStack/blob/main/LICENSE).
