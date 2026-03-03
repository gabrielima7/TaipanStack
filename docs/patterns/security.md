# Security Patterns — Practical Guide

> This guide demonstrates how to combine `@safe`, `guard_ssrf`, `guard_path_traversal`, and `@retry` in a real-world FastAPI endpoint. The examples use FastAPI syntax purely for illustration; all utilities are framework-agnostic.

---

## Why Layer Security Primitives?

TaipanStack's security model is **composable by design**. Each guard or decorator handles one orthogonal concern:

| Primitive | Responsibility |
|---|---|
| `@safe` | Catches unexpected exceptions → `Result` |
| `guard_ssrf` | Rejects URLs resolving to private/internal IPs |
| `guard_path_traversal` | Prevents filesystem escape via `../` patterns |
| `@retry` | Resilient retries with structured logging |

By combining them you get **defence-in-depth** without coupling your business logic to error-handling boilerplate.

---

## Example 1 — Safe External HTTP Fetch

```python
from __future__ import annotations

import httpx
from fastapi import FastAPI, HTTPException
from result import Err, Ok

from taipanstack.core.result import safe
from taipanstack.security.guards import SecurityError, guard_ssrf
from taipanstack.utils.retry import retry

app = FastAPI(title="TaipanStack Demo")


# 1. @retry — automatic backoff on network errors (structlog auto-logs each attempt)
# 2. @safe  — converts any remaining exception into Err so the endpoint stays clean
@retry(max_attempts=3, initial_delay=0.5, on=(httpx.TransportError,))
@safe
async def fetch_external(url: str) -> bytes:
    """Fetch content from a validated external URL."""
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.content


@app.get("/proxy")
async def proxy_endpoint(url: str) -> dict[str, str]:
    """Proxy an external URL — protected against SSRF."""
    # Step 1: SSRF guard — reject private/metadata IPs at the perimeter
    ssrf_result = guard_ssrf(url)
    if isinstance(ssrf_result, Err):
        raise HTTPException(status_code=400, detail=str(ssrf_result.err()))

    # Step 2: Fetch with retry + safe wrapper
    fetch_result = await fetch_external(ssrf_result.ok())
    match fetch_result:
        case Ok(content):
            return {"size": str(len(content)), "url": url}
        case Err(exc):
            raise HTTPException(status_code=502, detail=f"Upstream error: {exc}")
```

!!! tip "What happens on `http://169.254.169.254/latest/meta-data/`?"
    `guard_ssrf` resolves the hostname to `169.254.169.254`, matches it against the `169.254.0.0/16` link-local network, and immediately returns `Err(SecurityError(...))`. The `fetch_external` call is **never made**.

---

## Example 2 — Safe File Upload with Path Traversal Protection

```python
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile

from taipanstack.core.result import safe
from taipanstack.security.guards import SecurityError, guard_path_traversal

app = FastAPI()

UPLOAD_BASE = Path("/var/app/uploads").resolve()


@safe
def write_upload(filename: str, data: bytes) -> Path:
    """Write an uploaded file inside the uploads directory."""
    # guard_path_traversal raises SecurityError if filename tries to escape
    safe_path = guard_path_traversal(filename, base_dir=UPLOAD_BASE)
    safe_path.write_bytes(data)
    return safe_path


@app.post("/upload")
async def upload_file(file: UploadFile) -> dict[str, str]:
    """Accept and store a user-uploaded file."""
    data = await file.read()
    result = write_upload(file.filename or "unnamed", data)

    match result:
        case Ok(path):
            return {"stored_at": str(path)}
        case Err(SecurityError() as e):
            raise HTTPException(status_code=400, detail=f"Security violation: {e}")
        case Err(exc):
            raise HTTPException(status_code=500, detail=f"Write error: {exc}")
```

!!! warning "Never trust user-supplied filenames"
    A filename like `../../etc/cron.d/backdoor` would be caught by `guard_path_traversal` before `write_bytes` is ever reached.

---

## Example 3 — Combining All Three in One Endpoint

```python
from __future__ import annotations

from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException
from result import Err, Ok

from taipanstack.core.result import safe
from taipanstack.security.guards import guard_path_traversal, guard_ssrf
from taipanstack.utils.retry import retry

app = FastAPI()

CACHE_DIR = Path("/var/app/cache").resolve()


@retry(max_attempts=3, initial_delay=1.0, on=(httpx.TransportError,))
@safe
async def download_and_cache(url: str, filename: str) -> Path:
    """Download a remote resource and cache it to disk safely."""
    # SSRF guard: rejects internal URLs
    ssrf_check = guard_ssrf(url)
    if isinstance(ssrf_check, Err):
        msg = f"SSRF blocked: {ssrf_check.err()}"
        raise ValueError(msg)

    # Path traversal guard: rejects filenames escaping CACHE_DIR
    dest = guard_path_traversal(filename, base_dir=CACHE_DIR)

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(url)
        response.raise_for_status()

    dest.write_bytes(response.content)
    return dest


@app.post("/cache")
async def cache_remote_file(url: str, filename: str) -> dict[str, str]:
    """Download a public URL and store it in the server cache."""
    result = await download_and_cache(url, filename)
    match result:
        case Ok(path):
            return {"cached": str(path), "bytes": str(path.stat().st_size)}
        case Err(exc):
            raise HTTPException(status_code=400, detail=str(exc))
```

---

## Structlog Auto-Logging

Starting from **v0.3.3**, `@retry` and `CircuitBreaker` emit structured log events automatically when `structlog` is installed and **no manual callback is configured**:

```text
# Retry log (JSON output via structlog)
{
  "event": "retry_attempted",
  "function": "download_and_cache",
  "attempt": 1,
  "max_attempts": 3,
  "error": "[Errno 110] Connection timed out",
  "delay_seconds": 1.0,
  "level": "warning",
  "timestamp": "2026-03-03T16:00:00Z"
}

# Circuit breaker log
{
  "event": "circuit_state_changed",
  "circuit": "download_and_cache",
  "old_state": "closed",
  "new_state": "open",
  "failure_count": 5,
  "level": "warning"
}
```

You can override this behaviour at any time by passing `on_retry` or `on_state_change` callbacks — when a callback is set, the auto-log is suppressed and control passes to your handler.

---

## Summary

```mermaid
flowchart TD
    A[Incoming Request] --> B{guard_ssrf}
    B -- Err --> C[Return 400 SSRF Blocked]
    B -- Ok --> D{@retry wrapper}
    D --> E[@safe wrapper]
    E --> F{guard_path_traversal}
    F -- SecurityError --> G[Raise ValueError → Err]
    F -- Path ok --> H[Business Logic]
    H --> I[Ok result]
    G --> J[Err propagated to endpoint]
    I --> K[Return 200 Response]
    J --> L[Return 400/500 Response]
```
