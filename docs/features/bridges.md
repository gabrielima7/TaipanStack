# Taipan Bridges

TaipanStack introduces an agnostic, optionally loadable integration layer called **Taipan Bridges**, which connects your existing framework tools (like FastAPI, Litestar, SQLAlchemy, and Redis) directly with the native resilience and security features of TaipanStack.

---

## The SafeHTTPClient

When making external connections, developers often use raw `httpx`, risking vulnerabilities such as **SSRF** (Server-Side Request Forgery) and lack of circuit breaking for degraded dependencies.

**Taipan Bridges** elegantly intercepts `httpx` and integrates:
1. `guard_ssrf` on every request.
2. Exponential Retry.
3. Circuit Breakers.

### Usage

```python
from taipanstack.bridges.http_bridge import SafeHttpClient
from taipanstack.core.result import Ok, Err

async def call_external_api():
    async with SafeHttpClient(name="external-api", ssrf_protection=True) as client:
        # Resolves URL, checks if IP is private/reserved, limits timeouts, and retries.
        result = await client.get("https://api.github.com/users/gabrielima7")

        match result:
            case Ok(response):
                print("Data:", response.json())
            case Err(e):
                print("Securely blocked or failed:", e)
```

---

## Web Bridge (ASGI)

You can protect your **FastAPI** or **Litestar** application simply by mounting `TaipanMiddleware`.

This middleware:
- Unifies unhandled error mapping to strict `{ "status": "error" }` JSON preventing info leaks.
- Supports Rate Limiting via `RateLimiter`.
- Injects essential security headers (`X-Frame-Options`, `X-Content-Type-Options`, `Strict-Transport-Security`, `Content-Security-Policy`).

### Usage (FastAPI)

```python
from fastapi import FastAPI
from taipanstack.bridges.web_bridge import TaipanMiddleware, SecurityHeadersConfig

app = FastAPI()

# Add the middleware with strict headers and a JSON 429 rate limit payload
app.add_middleware(
    TaipanMiddleware,
    security_headers=True,
    headers_config=SecurityHeadersConfig(
        x_frame_options="DENY",
        content_security_policy="default-src 'self'"
    )
)
```

### Response Mapping

Returning `Result` types in API handlers is made simple with `result_to_response`:

```python
from taipanstack.bridges.web_bridge import result_to_response
from fastapi.responses import JSONResponse

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # Returns {"status": "success", "data": {...}} or {"status": "error", "error": "..."}
    return JSONResponse(result_to_response(fetch_user(user_id)))
```

---

## DB Bridge (Resilient Database)

Direct database queries suffer from locking, connection drops, and thundering herd scenarios. `ResilientDatabase` protects SQLAlchemy and Redis instances transparently.

### Usage

```python
from taipanstack.bridges.db_bridge import ResilientDatabase
from taipanstack.resilience.circuit_breaker import CircuitBreaker

# Provide your async SQLAlchemy session
resilient_db = ResilientDatabase(
    session=db_session,
    circuit_breaker=CircuitBreaker(name="postgres-db", failure_threshold=5)
)

async def make_query():
    # Will be blocked automatically if DB trips the breaker
    result = await resilient_db.execute(select(User).where(User.id == 1))
    # ...
```
