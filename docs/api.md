# API Documentation

This document covers the core modules and functions provided by TaipanStack.

## Core Types

### `Result`, `Ok`, `Err`
Inspired by Rust and other functional languages, TaipanStack heavily relies on the `Result` pattern to prevent silent exceptions.

- **`Result[T, E]`**: A type alias representing either `Ok(T)` or `Err(E)`.
- **`Ok(T)`**: Represents a successful operation, containing the value `T`.
- **`Err(E)`**: Represents a failed operation, containing the error `E`.

**Usage:**
```python
from taipanstack.core.result import Result, Ok, Err

def find_user(user_id: str) -> Result[User, UserError]:
    user = db.query(user_id)
    if user:
        return Ok(user)
    return Err(UserNotFoundError(f"User {user_id} not found"))
```

### `@safe` Decorator
The `@safe` decorator wraps any standard function that may raise an exception into a function that returns a `Result`.
```python
@safe(ZeroDivisionError)
def divide(a: int, b: int) -> float:
    return a / b

# Returns Err(ZeroDivisionError) if b is 0.
```

## Security Utils

### Guards
Guards prevent malicious operations by raising `SecurityError` immediately.

- `guard_path_traversal(user_path: str, base_dir: str) -> Path`: Prevents directory traversal attacks (`../`).
- `guard_command_injection(command: list[str], allowed_commands: list[str]) -> list[str]`: Ensures standard OS command execution is restricted to safe sub-commands.

### Validators & Sanitizers
Prevent XSS, SQL injection, and invalid data formats.
- `sanitize_html(input_str: str) -> str`: Removes `<script>` tags and risky HTTP payloads.
- `validate_email(email_str: str) -> bool`: Safe email matching against strict regex profiles.

## Application Utilities

### `circuit_breaker`
To protect external services from snowballing failures, wrap unstable network dependencies in `@circuit_breaker(failure_threshold=5, timeout=30)`.

### `retry`
Applies an exponential backoff retry mechanism to any async or sync operation.
```python
@retry(max_attempts=3, base_delay=1.0, on=(TimeoutError,))
def make_request(): ...
```

### `metrics`
Contains basic decorators `@timed` and `@counted` to emit system instrumentation.
