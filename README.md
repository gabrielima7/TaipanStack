<div align="center">

# 🐍 TaipanStack

### **The Modern Python Foundation**

*Launch secure, high-performance Python applications in seconds.*

[![CI](https://github.com/gabrielima7/TaipanStack/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/gabrielima7/TaipanStack/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen?style=flat&logo=codecov)](https://github.com/gabrielima7/TaipanStack)
[![Code Style](https://img.shields.io/badge/Code%20Style-Ruff-D7FF64?style=flat&logo=ruff&logoColor=black)](https://github.com/astral-sh/ruff)
[![Type Checked](https://img.shields.io/badge/Type%20Checked-Mypy-blue?style=flat)](http://mypy-lang.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)
[![Security](https://img.shields.io/badge/Security-Bandit%20%7C%20Semgrep-red?style=flat)](SECURITY.md)
[![SBOM](https://img.shields.io/badge/SBOM-CycloneDX-informational?style=flat&logo=owasp)](https://github.com/gabrielima7/TaipanStack/actions/workflows/sbom-slsa.yml)
[![SLSA](https://img.shields.io/badge/SLSA-Sigstore-blueviolet?style=flat)](https://github.com/gabrielima7/TaipanStack/actions/workflows/sbom-slsa.yml)
[![PyPI](https://img.shields.io/pypi/v/taipanstack?style=flat&logo=pypi&logoColor=white)](https://pypi.org/project/taipanstack/)

---

[**Features**](#-features) • [**Quick Start**](#-quick-start) • [**Architecture**](#-architecture) • [**DevSecOps**](#-devsecops) • [**API**](#-api-highlights) • [**Contributing**](#-contributing)

</div>

---

## ✨ Why TaipanStack?

> **"Write less, build better."**

TaipanStack is a battle-tested foundation for production-grade Python projects that combines **security**, **performance**, and **developer experience** into a single, cohesive toolkit.

<table>
<tr>
<td width="50%">

### 🛡️ Security First
- Path traversal protection
- Command injection guards
- Input sanitizers & validators
- Secret detection integration
- **SBOM + SLSA** supply-chain attestation

</td>
<td width="50%">

### ⚡ High Performance
- `uvloop` async event loop
- `orjson` fast JSON serialization
- `Pydantic v2` validation
- Performance benchmarks with regression detection

</td>
</tr>
<tr>
<td width="50%">

### 🎯 Rust-Style Error Handling
- `Ok`/`Err` Result types
- Explicit error propagation
- Pattern matching support
- No silent failures

</td>
<td width="50%">

### 🔧 Developer Experience
- Pre-configured quality tools
- **100% code coverage** (1002 tests)
- Architecture enforcement
- Hardened Docker template

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** (supports 3.11, 3.12, 3.13, 3.14)
- **Poetry** ([install guide](https://python-poetry.org/docs/#installation))

### Installation

#### From PyPI

```bash
pip install taipanstack
```

#### From Source

```bash
# Clone the repository
git clone https://github.com/gabrielima7/TaipanStack.git
cd TaipanStack

# Install dependencies
poetry install --with dev

# Run quality checks
make all
```

### Verify Installation

```bash
# Run tests with 100% coverage (1002 tests)
make test

# Check architecture contracts
make lint-imports

# Run security scans
make security

# Run property-based fuzzing
make property-test

# Run performance benchmarks
make benchmark
```

---

## 📐 Architecture

TaipanStack follows a clean, layered architecture with strict dependency rules enforced by **Import Linter**.

```
                    ┌─────────────────────────────────────┐
                    │             Application             │
                    │          (src/app/main.py)          │
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

### Project Structure

```text
TaipanStack/
├── src/
│   ├── app/              # Application entry point
│   └── taipanstack/
│       ├── core/         # 🎯 Result types, functional patterns
│       ├── config/       # ⚙️ Configuration models & generators
│       ├── security/     # 🛡️ Guards, sanitizers, validators
│       └── utils/        # 🔧 Logging, metrics, retry, filesystem
├── tests/                # ✅ 1002 tests, 100% coverage
├── .semgrep/             # 🔍 Custom SAST rules
├── .github/              # 🔄 CI/CD + SBOM/SLSA workflows
├── Dockerfile            # 🐳 Hardened multi-stage container
└── pyproject.toml        # 📋 Modern dependency management
```

---

## 🔐 DevSecOps

TaipanStack integrates security and quality at every level:

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
| **Containers** | Docker (Alpine, rootless) | Hardened-by-default images |

### CI Pipeline

```yaml
# Runs on every push/PR
✓ Test Matrix     → Python 3.11-3.14 × (Ubuntu, macOS, Windows)
✓ Linux Distros   → Ubuntu, Debian, Fedora, openSUSE, Arch, Alpine
✓ Code Quality    → Ruff check & format
✓ Type Check      → Mypy strict mode
✓ Security        → Bandit + Semgrep (custom rules)
✓ Architecture    → Import Linter contracts
✓ Benchmarks      → Performance regression (>5% = fail)
✓ SBOM + SLSA     → Supply-chain attestation on release
```

---

## 📚 API Highlights

### Result Types (Rust-Style Error Handling)

```python
from taipanstack.core.result import Result, Ok, Err, safe

@safe
def divide(a: int, b: int) -> float:
    return a / b

# Explicit error handling with pattern matching
match divide(10, 0):
    case Ok(value):
        print(f"Result: {value}")
    case Err(error):
        print(f"Error: {error}")
```

### Security Guards

```python
from taipanstack.security.guards import guard_path_traversal, guard_command_injection

# Prevent path traversal attacks
safe_path = guard_path_traversal(user_input, base_dir="/app/data")

# Prevent command injection
safe_cmd = guard_command_injection(
    ["git", "clone", repo_url],
    allowed_commands=["git"]
)
```

### Retry with Exponential Backoff

```python
from taipanstack.utils.retry import retry

@retry(max_attempts=3, on=(ConnectionError, TimeoutError))
async def fetch_data(url: str) -> dict:
    return await http_client.get(url)
```

### Circuit Breaker

```python
from taipanstack.utils.circuit_breaker import circuit_breaker

@circuit_breaker(failure_threshold=5, timeout=30)
def call_external_service() -> Response:
    return service.call()
```

### 🔗 Combining Result + Circuit Breaker

```python
from taipanstack.core.result import safe, Ok, Err
from taipanstack.utils.circuit_breaker import CircuitBreaker

breaker = CircuitBreaker(failure_threshold=3, timeout=60, name="payments")

@breaker
@safe
def charge_customer(customer_id: str, amount: float) -> dict:
    return payment_gateway.charge(customer_id, amount)

# Both circuit protection AND explicit error handling
result = charge_customer("cust_123", 49.99)
match result:
    case Ok(receipt):
        print(f"Payment successful: {receipt}")
    case Err(error):
        print(f"Payment failed safely: {error}")
```

### 🔗 Combining Result + Retry with Monitoring

```python
from taipanstack.core.result import safe, unwrap_or
from taipanstack.utils.retry import retry

@retry(
    max_attempts=3,
    on=(ConnectionError, TimeoutError),
    on_retry=lambda attempt, max_a, exc, delay: print(
        f"⚠️  Attempt {attempt}/{max_a} failed, retrying in {delay:.1f}s..."
    ),
)
@safe
def fetch_user_profile(user_id: str) -> dict:
    return api_client.get(f"/users/{user_id}")

# Retry handles transient failures, Result handles business errors
profile = unwrap_or(fetch_user_profile("usr_456"), {"name": "Unknown"})
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

## 🐳 Docker

```bash
# Build hardened image
docker build -t taipanstack:latest .

# Run (rootless, read-only)
docker run --rm --read-only taipanstack:latest
```

Security features: multi-stage build, Alpine base (<50MB), non-root `appuser` (UID 1000), healthcheck, no shell in runtime.

---

## 🛠️ Tech Stack

<table>
<tr>
<th>Runtime</th>
<th>Quality</th>
<th>DevSecOps</th>
</tr>
<tr>
<td>

- Pydantic v2
- Orjson
- Uvloop
- Structlog
- Result

</td>
<td>

- Ruff
- Mypy
- Bandit
- Pytest + Hypothesis
- mutmut
- pytest-benchmark

</td>
<td>

- GitHub Actions
- Syft + Cosign (SBOM/SLSA)
- Dependabot
- Pre-commit
- Poetry
- Docker (Alpine, rootless)

</td>
</tr>
</table>

---

## 🤝 Contributing

Contributions are welcome! Please check our [Contributing Guide](CONTRIBUTING.md) for details on:

- 🐛 Bug reports
- ✨ Feature requests
- 📝 Documentation improvements
- 🔧 Pull requests

---

## 📝 License

This project is open-sourced under the [MIT License](LICENSE).

---

<div align="center">

**Made with ❤️ for the Python community**

[⬆ Back to Top](#-taipanstack)

</div>
