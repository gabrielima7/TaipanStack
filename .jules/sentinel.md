## 2026-03-09 - Path Traversal bypass via Symlinks checking with `.resolve()`
**Vulnerability:** The path traversal guard logic `is_symlink()` check always evaluates to `False` because `path.resolve()` resolves the entire path natively, following symlinks and stripping them away. This means that a symlink pointing to an unauthorized directory could effectively bypass the `allow_symlinks=False` check.
**Learning:** `path.resolve()` on a `pathlib.Path` follows symlinks intrinsically, therefore applying `.is_symlink()` directly to the `resolved` path guarantees a `False` result, making the security mechanism fail silently.
**Prevention:** Iteratively loop through all parts of the *unresolved* path components upwards using `.parent` up until the base directory to properly call `.is_symlink()` and check for user-supplied symlinks correctly before attempting to resolve the file.
## 2026-03-11 - Missing Path Traversal Guard in File Utilities
**Vulnerability:** The `find_files` and `get_file_hash` utility functions in `taipanstack.utils.filesystem` did not apply a default path traversal check (`guard_path_traversal(..., Path.cwd())`) when `base_dir=None` was supplied. This oversight allowed them to process files outside of the current working directory, unlike all other functions in the module (`safe_read`, `safe_write`, `ensure_dir`, `safe_delete`) which did include the strict fallback.
**Learning:** Similar functions across an API module can drift in their security constraints. A missing fallback traversal block can create a gap where read-only actions (like hashing or globbing) can bypass protections that write actions strictly enforce.
**Prevention:** Ensure a unified, central path-validation mechanism or decorator that strictly defines fallbacks (e.g. `cwd`), rather than reimplementing the exact same `if base_dir ... elif ".." in str(path): ...` logic repetitively in every file utility function.

## 2026-03-12 - Sensitive Data Exposure via BaseModel
**Vulnerability:** Models representing users (`UserCreate` and `User`) inherited from Pydantic's `BaseModel` instead of `SecureBaseModel`. This allowed sensitive fields like `password` and `password_hash` to be included in plaintext when dumping the model to a dictionary or JSON, leading to potential credential leakage in logs or API responses.
**Learning:** Standard Pydantic models do not provide automated redaction for sensitive keys. Even when using `SecretStr`, calling `.model_dump()` or `.model_dump_json()` on a `BaseModel` can still expose sensitive values depending on the configuration and usage.
**Prevention:** Always use `SecureBaseModel` for any data models that handle Pydantic's `SecretStr` or contain fields with sensitive names (like `password`, `token`, `secret`, `api_key`). `SecureBaseModel` provides an extra layer of defense-in-depth by automatically masking these fields during serialization.

## 2026-03-13 - Use of Weak Hash Algorithms in Filesystem Utilities
**Vulnerability:** The `get_file_hash` function allowed any algorithm supported by `hashlib.new()`, including cryptographically weak ones like MD5 and SHA-1.
**Learning:** Defaulting to arbitrary user-supplied strings for cryptographic primitives without validation can lead to the use of insecure or deprecated algorithms.
**Prevention:** Implement a dedicated security guard (whitelist) for cryptographic algorithms and apply it consistently across all utilities that perform hashing or encryption.

## 2026-03-18 - Regex Validation Bypass via Trailing Newlines
**Vulnerability:** Regex patterns in `src/taipanstack/security/validators.py` (e.g., for project names, emails, semver, Python versions) used the `$` anchor for string termination.
**Learning:** In Python's `re` module, the `$` anchor matches either the end of the string OR just before a trailing newline (`\n`). This allows an attacker to bypass strict string validation by appending a newline character to an otherwise invalid payload.
**Prevention:** Always use the `\Z` anchor instead of `$` when enforcing absolute string termination in security-critical regex patterns to prevent newline-based bypasses.
