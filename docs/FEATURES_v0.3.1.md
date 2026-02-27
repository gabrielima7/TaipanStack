# TaipanStack v0.3.1 — Feature Documentation

## Overview

v0.3.1 is a **patch release** focused on polishing, type safety, observability, and developer experience. It introduces **0 breaking changes** and delivers improvements across 5 areas: advanced type hinting, monitoring callbacks, security edge-case hardening, version alignment, and documentation.

---

## 1. Advanced Type Hinting (Generics & Overloads)

**Files**:
- [`src/taipanstack/core/result.py`](../../src/taipanstack/core/result.py)
- [`src/taipanstack/utils/retry.py`](../../src/taipanstack/utils/retry.py)
- [`src/taipanstack/utils/circuit_breaker.py`](../../src/taipanstack/utils/circuit_breaker.py)

Strengthened type annotations for strict-mode compatibility with `mypy` and `pyright`.

### What Changed

| Module | Change | Benefit |
|--------|--------|---------|
| `result.py` | `@overload` signatures for `unwrap_or` and `unwrap_or_else` | Type checkers now narrow `T` vs `U` based on `Ok`/`Err` input |
| `result.py` | New `TypeVar U` for default values | Default can be a different type than the Ok value |
| `retry.py` | `Retrier.__exit__` uses `type[BaseException]`, `TracebackType` | Matches Python data model spec for context managers |
| `circuit_breaker.py` | Explicit `return False` sentinel in `_should_attempt()` | All code paths return a value — satisfies strict checkers |

### Before / After

```python
# BEFORE: mypy cannot narrow the return type
value: int | str = unwrap_or(Ok(42), "default")  # type: int | str

# AFTER: mypy narrows correctly based on the Result variant
value: int = unwrap_or(Ok(42), "default")         # type: int ✅
value: str = unwrap_or(Err("fail"), "default")     # type: str ✅
```

### Verification

```bash
# Passes with zero errors on all 24 source files
poetry run mypy src/ --strict
```

---

## 2. Observability & Monitoring Callbacks

**Files**:
- [`src/taipanstack/utils/retry.py`](../../src/taipanstack/utils/retry.py)
- [`src/taipanstack/utils/circuit_breaker.py`](../../src/taipanstack/utils/circuit_breaker.py)

Added optional callback injection points for custom monitoring without breaking the existing API.

### Retry: `on_retry` Callback

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `on_retry` | `Callable[[int, int, Exception, float], None] \| None` | `None` | Called on each retry with `(attempt, max_attempts, exception, delay)` |

```python
from taipanstack.utils.retry import retry

def log_to_datadog(attempt: int, max_attempts: int, exc: Exception, delay: float) -> None:
    statsd.increment("retry.attempt", tags=[f"attempt:{attempt}"])

@retry(
    max_attempts=3,
    on=(ConnectionError,),
    on_retry=log_to_datadog,
)
def fetch_data(url: str) -> dict:
    return requests.get(url).json()
```

### Circuit Breaker: `on_state_change` Callback

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `on_state_change` | `Callable[[CircuitState, CircuitState], None] \| None` | `None` | Called on state transitions with `(old_state, new_state)` |

```python
from taipanstack.utils.circuit_breaker import circuit_breaker, CircuitState

def alert_on_open(old: CircuitState, new: CircuitState) -> None:
    if new == CircuitState.OPEN:
        slack.send(f"🚨 Circuit opened! {old.value} → {new.value}")

@circuit_breaker(
    failure_threshold=5,
    timeout=60,
    on_state_change=alert_on_open,
)
def call_payment_api(amount: float) -> dict:
    return gateway.charge(amount)
```

### Enriched Log Messages

| Transition | Log Message Example |
|------------|-------------------|
| CLOSED → OPEN | `"Circuit payments opened after 5 failures (threshold=5)"` |
| OPEN → HALF_OPEN | `"Circuit payments entering half-open state (was open for 30.1s, failures=5)"` |
| HALF_OPEN → CLOSED | `"Circuit payments closed after recovery (2 consecutive successes)"` |
| HALF_OPEN → OPEN | `"Circuit payments reopened after failure in half-open (total failures=6)"` |

---

## 3. Security Edge-Case Hardening

**Files**:
- [`src/taipanstack/security/guards.py`](../../src/taipanstack/security/guards.py)
- [`src/taipanstack/security/sanitizers.py`](../../src/taipanstack/security/sanitizers.py)
- [`src/taipanstack/security/validators.py`](../../src/taipanstack/security/validators.py)

All public security functions now validate input types at runtime, raising clear `TypeError` instead of crashing with cryptic Python errors.

### Functions Hardened

| Function | Guard Added | Error Raised |
|----------|------------|-------------|
| `guard_path_traversal(path)` | `path` must be `str \| Path` | `TypeError` |
| `guard_command_injection(cmd)` | All items must be `str` | `TypeError` (with index) |
| `guard_env_variable(name)` | `name` must be `str`, non-empty | `TypeError` / `SecurityError` |
| `sanitize_string(value)` | `value` must be `str` | `TypeError` |
| `sanitize_filename(filename)` | `filename` must be `str` | `TypeError` |
| `validate_project_name(name)` | `name` must be `str` | `TypeError` |
| `validate_email(email)` | `email` must be `str` | `TypeError` |
| `validate_url(url)` | `url` must be `str` | `TypeError` |
| `validate_python_version(ver)` | `ver` must be `str` | `TypeError` |

### Error Message Quality

```python
# BEFORE: Cryptic error
sanitize_string(None)
# AttributeError: 'NoneType' object has no attribute 'strip'

# AFTER: Clear TaipanStack error
sanitize_string(None)
# TypeError: value must be str, got NoneType

# Command injection with index context
guard_command_injection(["git", "clone", 123])
# TypeError: All command arguments must be strings, got int at index 2

# Empty env variable name
guard_env_variable("   ")
# SecurityError: [env_variable] Environment variable name cannot be empty or whitespace
```

---

## 4. Version Alignment & CI/CD

**Files**:
- [`pyproject.toml`](../../pyproject.toml)
- [`src/taipanstack/__init__.py`](../../src/taipanstack/__init__.py)

### Version Fix

| File | Before | After |
|------|--------|-------|
| `pyproject.toml` | `version = "0.3.0"` | `version = "0.3.1"` |
| `__init__.py` | `__version__ = "2.0.0"` ⚠️ | `__version__ = "0.3.1"` ✅ |

> **Note**: The `"2.0.0"` value was a legacy artifact from the project rename (Stack → TaipanStack). Now both sources of truth are aligned.

### CI Pipeline Status

The existing CI workflow (`ci.yml`) with its **12 jobs** was reviewed and requires no changes:

```
✓ Test Matrix        → Python 3.11–3.14 × (Ubuntu, macOS, Windows)
✓ Linux Distros      → Ubuntu, Fedora, openSUSE, Arch, Alpine
✓ Code Quality       → Ruff check & format
✓ Type Check         → Mypy --strict
✓ Security           → Bandit + Semgrep (custom rules)
✓ Architecture       → Import Linter contracts
✓ Property Testing   → Hypothesis fuzzing
✓ Mutation Testing   → mutmut
✓ Benchmarks         → pytest-benchmark regression
✓ Docker Build       → Hardened container validation
✓ Docstring Coverage → interrogate
✓ Dry Run + Integration
```

---

## 5. Documentation & Developer Experience

**Files**:
- [`README.md`](../../README.md)
- [`CHANGELOG.md`](../../CHANGELOG.md)

### New README Examples

Two practical examples were added showing how to combine TaipanStack primitives:

#### Result + Circuit Breaker

```python
from taipanstack.core.result import safe, Ok, Err
from taipanstack.utils.circuit_breaker import CircuitBreaker

breaker = CircuitBreaker(failure_threshold=3, timeout=60, name="payments")

@breaker
@safe
def charge_customer(customer_id: str, amount: float) -> dict:
    return payment_gateway.charge(customer_id, amount)

result = charge_customer("cust_123", 49.99)
match result:
    case Ok(receipt):
        print(f"Payment successful: {receipt}")
    case Err(error):
        print(f"Payment failed safely: {error}")
```

#### Result + Retry with Monitoring

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

profile = unwrap_or(fetch_user_profile("usr_456"), {"name": "Unknown"})
```

---

## Quality Summary

| Metric | v0.3.0 | v0.3.1 |
|--------|--------|--------|
| **Total tests** | 664 | 664 |
| **Coverage** | 100% | 100% |
| **mypy --strict** | ✅ | ✅ (+ overloads) |
| **Type-guarded functions** | 0 | 9 |
| **Monitoring callbacks** | 0 | 2 |
| **Breaking changes** | — | **0** |
| **Files modified** | — | 10 |
