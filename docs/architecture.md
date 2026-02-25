# TaipanStack Architecture

TaipanStack is built on the philosophy of maximum safety by default, combined with blazing fast asynchronous programming. The internal architecture favors a strict layered dependency map which is enforced statically.

## Layered Design

The architecture enforces unidirectional data flow and strict dependency boundaries.
1. **Application Layer (`app/`)**: Where the business logic resides. This layer is allowed to import from `taipanstack/`, but `taipanstack/` may NEVER import from `app/`.
2. **Utilities & Adapters (`utils/`, `config/`)**: Contains pure Python utilities, file handlers, logging pipelines, and configuration management wrappers.
3. **Core Layer (`core/`)**: Holds the `Result` pattern bindings, performance optimizations (like `uvloop`, `orjson`), and primitive aliases that form the base of the framework mapping.
4. **Security Layer (`security/`)**: Sits orthogonally to the framework and provides decorators and validators (`@safe_xyz`) intended to wrap edge boundaries.

## Concurrency Model

When used with production dependencies (`--install-runtime-deps`), TaipanStack opts-in to `uvloop` for asyncio execution. This provides a 2-4x speedup over the standard `asyncio` loop. `TaipanStack` detects this implicitly and bootstraps the loop on `main()` invocation.

## Error Handling Philosophy

Exceptions represent unrecoverable panics in runtime. For standard failures—such as network loss, missing rows, validation errors—TaipanStack uses the **Result** monad.

- Never use `raise ValueError(...)` to return to a caller.
- Methods should strongly type their possible failures via `Err[MyCustomError]`.
- Pattern matching (`match` / `case`) leverages Python 3.10+ to unpack results safely.

This ensures you cannot deploy a bug where you "forgot" to catch a standard exception—Mypy handles it statically!

## Security Strategy

The core framework exposes `taipanstack.security` heavily inspired by security best practices.
1. **No Silent Failures**: Malformed configuration immediately faults with a clear exception during startup.
2. **Boundary Validation**: Data coming from API/users is validated immediately using `pydantic`.
3. **AST Scanning**: Every build verifies the project with both `bandit` and `semgrep`. Over time, we embed custom `semgrep` definitions to detect and ban bad practices in TaipanStack explicitly.
