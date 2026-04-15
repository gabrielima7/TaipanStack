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

    Path traversal protection, command injection guards, subprocess isolation, adaptive limiters, adaptive resilience pipeline, input sanitizers & validators, secret detection, SBOM + SLSA attestation.

-   :zap: **High Performance**

    ---

    `uvloop` async event loop, `orjson` fast JSON, `Pydantic v2` validation, pytest-benchmark regression detection.

-   :dart: **Rust-Style Error Handling**

    ---

    `Ok`/`Err` Result types, explicit error propagation, pattern matching, no silent failures.

-   :wrench: **Developer Experience**

    ---

    Pre-configured quality tools, **100% code coverage** (1205 tests), architecture enforcement, hardened Docker template.

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

### 🔗 Adaptive Resilience Pipeline

```python
from taipanstack.core.result import Result, Ok, Err
from taipanstack.resilience.adaptive import ResilienceOrchestrator, AdaptiveCircuitBreaker
from taipanstack.resilience.retry import RetryConfig

# Compose an intelligent pipeline: Bulkhead -> Breaker -> Retry -> Timeout -> Fallback
orch = (
    ResilienceOrchestrator("billing_api")
    .with_bulkhead(max_concurrent=10, max_queue=50) # Prevent resource exhaustion
    .with_circuit_breaker(AdaptiveCircuitBreaker("billing", target_error_rate=0.1)) # Auto-tunes thresholds

    .with_retry(RetryConfig(max_attempts=3, initial_delay=0.1))
    .with_fallback({"status": "unavailable"})
)

async def process_billing() -> Result[dict, Exception]:
    # The orchestrator handles all concurrency, retry, circuit breaking, and fallbacks
    return await orch.execute(stripe_gateway.charge)
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
| [🧪 Coverage Report](https://gabrielima7.github.io/TaipanStack/htmlcov/) | Full HTML coverage report — 100% (1205 tests) |
| [⚡ Benchmark Dashboard](https://gabrielima7.github.io/TaipanStack/dev/bench/) | Performance history & regression graphs |

---

## 🤝 Contributing

Contributions are welcome! See the [Contributing Guide](https://github.com/gabrielima7/TaipanStack/blob/main/CONTRIBUTING.md) for details.

## 📝 License

Open-sourced under the [MIT License](https://github.com/gabrielima7/TaipanStack/blob/main/LICENSE).
