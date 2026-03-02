import timeit
import sys
from pathlib import Path
sys.path.insert(0, str(Path("src").resolve()))

import taipanstack.security.guards as guards
SecurityError = guards.SecurityError

original_func = r"""
def original_guard_path_traversal(
    path: Path | str,
    base_dir: Path | str | None = None,
    *,
    allow_symlinks: bool = False,
) -> Path:
    if not isinstance(path, (str, Path)):
        raise TypeError(f"path must be str or Path, got {type(path).__name__}")
    path = Path(path) if isinstance(path, str) else path
    base_dir = Path(base_dir).resolve() if base_dir else Path.cwd().resolve()

    # Check for explicit traversal patterns before resolution
    path_str = str(path)
    traversal_patterns = [
        "..",
        "~",
        r"\.\.",
        "%2e%2e",  # URL encoded ..
        "%252e%252e",  # Double URL encoded
    ]

    for pattern in traversal_patterns:
        if pattern.lower() in path_str.lower():
            raise SecurityError(
                f"Path traversal pattern detected: {pattern}",
                guard_name="path_traversal",
                value=path_str[:50],  # Truncate for safety
            )

    try:
        resolved = path.resolve() if path.is_absolute() else (base_dir / path).resolve()
    except (OSError, ValueError) as e:
        raise SecurityError(
            f"Invalid path: {e}",
            guard_name="path_traversal",
        ) from e

    try:
        resolved.relative_to(base_dir)
    except ValueError as e:
        raise SecurityError(
            f"Path escapes base directory: {resolved} is not under {base_dir}",
            guard_name="path_traversal",
            value=str(resolved)[:100],
        ) from e

    is_existing_symlink = (
        not allow_symlinks and resolved.exists() and resolved.is_symlink()
    )
    if is_existing_symlink:
        raise SecurityError(
            "Symlinks are not allowed",
            guard_name="path_traversal",
            value=str(resolved),
        )

    return resolved
"""

# Define original func in globals
exec(original_func, globals())

setup_original = """
from __main__ import original_guard_path_traversal
from pathlib import Path
base = Path('/tmp')
"""

setup_new = """
from taipanstack.security.guards import guard_path_traversal as new_guard_path_traversal
from pathlib import Path
base = Path('/tmp')
"""

test_code_original = "original_guard_path_traversal('safe_file.txt', base)"
test_code_new = "new_guard_path_traversal('safe_file.txt', base)"

iterations = 300000

print("Benchmarking original...")
import timeit
time_original = timeit.timeit(stmt=test_code_original, setup=setup_original, number=iterations)

print("Benchmarking new...")
time_new = timeit.timeit(stmt=test_code_new, setup=setup_new, number=iterations)

print(f"\nOriginal time: {time_original:.4f} seconds")
print(f"New time:      {time_new:.4f} seconds")

if time_original > time_new:
    improvement = (time_original - time_new) / time_original * 100
    print(f"Improvement:   {improvement:.2f}% faster")
else:
    degradation = (time_new - time_original) / time_original * 100
    print(f"Degradation:   {degradation:.2f}% slower")
