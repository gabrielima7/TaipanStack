# 🛡️ Sentinel: [High] Fix path traversal guard crashes and null byte injection

## 🚨 Severity
High

## 💡 Vulnerability
The `guard_path_traversal` function in `src/taipanstack/security/guards.py` was vulnerable to unhandled exceptions when processing malicious or invalid input types. Specifically:
1. When passed paths or base directories containing embedded null bytes (`\x00`), `pathlib.Path.resolve()` crashed with a deep internal `ValueError: lstat: embedded null character in path`, bypassing the graceful `SecurityError` rejection.
2. The function did not correctly type-check `base_dir`, causing `TypeError: argument should be a str or an os.PathLike object where __fspath__ returns a str, not 'bytes'` when non-string types were provided.

## 🎯 Impact
By exploiting these edge cases, an attacker could bypass intended security guardrails by crashing the application on an unhandled exception instead of being gracefully blocked via the standard `SecurityError` flow.

## 🔧 Fix
- Patched `guard_path_traversal` to explicitly validate the type of `base_dir` and proactively detect embedded null bytes in both the `path` and `base_dir` parameters.
- If null bytes are detected, it now safely raises a `SecurityError` explicitly citing "Path contains null bytes" before any `pathlib` operations occur.
- Added a new property-based fuzz test using `hypothesis` to continuously bombard the target with diverse types and string mutations to guarantee no unhandled exceptions persist.

## ✅ Verification
The complete test suite successfully passes with the new fuzzing payload and the code survives massive, malformed input values.
