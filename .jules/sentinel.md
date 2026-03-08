## 2023-10-27 - Secure Jitter Implementation
**Vulnerability:** Standard pseudo-random generators (`random.uniform`) used for retry jitter.
**Learning:** Even though retry jitter is intentionally non-cryptographic (for load distribution, not security), using standard `random` flags a B311 warning in security linters like Bandit. The "Sentinel" philosophy mandates a strict security baseline where standard `random` modules are prohibited to maintain a clean bill of health. We learned that to suppress these tool warnings without compromising the strict policy, we should use `secrets.SystemRandom().uniform()` as a drop-in replacement.
**Prevention:** For any randomization task (even non-cryptographic like backoff jitter), use `secrets.SystemRandom` to avoid static analysis security warnings and adhere to strict security policies.

## 2026-03-08 - [Path Traversal bypass due to resolved symlinks]
**Vulnerability:** The `guard_path_traversal` function intended to block symlink-based path traversal attacks (when `allow_symlinks=False`), but checked `resolved.is_symlink()` after calling `path.resolve()`. Since `resolve()` natively follows and removes symlinks, `is_symlink()` always returned `False`, rendering the check entirely ineffective.
**Learning:** In Python path traversal protections, checking `is_symlink()` on a `pathlib.Path` object *after* calling `.resolve()` is a vulnerability pattern, as `resolve()` natively follows and removes symlinks. Validations must occur on the unresolved path components.
**Prevention:** When implementing symlink checks, traverse the un-resolved path components (or use `.readlink()`) relative to the base directory before using `.resolve()` to determine the final location.
