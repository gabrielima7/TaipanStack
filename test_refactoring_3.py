import os

with open("src/taipanstack/security/sanitizers.py", "r") as f:
    content = f.read()

# Replace sanitize_path explicitly
new_sanitize_path = """def _reconstruct_path(path: Path, parts: list[str]) -> Path:
    \"\"\"Reconstruct a sanitized path from its parts.\"\"\"
    if path.is_absolute():
        anchor = Path(path.anchor)
        return anchor.joinpath(*parts) if parts else anchor

    if parts:
        return Path().joinpath(*parts)

    return Path()

def sanitize_path(
    path: str | Path,
    *,
    base_dir: Path | None = None,
    max_depth: int | None = 10,
    resolve: bool = False,
) -> Path:
    \"\"\"Sanitize a path to prevent traversal and normalize it.

    Args:
        path: The path to sanitize.
        base_dir: Optional base directory to constrain to.
        max_depth: Maximum directory depth allowed.
        resolve: Whether to resolve the path (requires it to exist).

    Returns:
        The sanitized Path object.

    Raises:
        ValueError: If path is invalid or too deep.

    \"\"\"
    if isinstance(path, str):
        if "\\x00" in path:  # pragma: no branch
            path = path.replace("\\x00", "")
        path = Path(path)
    else:  # pragma: no branch
        path = Path(path)

    # Clean components
    parts = _clean_path_parts(path)

    # Reconstruct path
    sanitized = _reconstruct_path(path, parts)

    # Check depth
    depth = len(sanitized.parts)
    if max_depth is not None and depth > max_depth:
        msg = f"Path depth {depth} exceeds maximum of {max_depth}"
        raise ValueError(msg)

    # Constrain to base_dir
    return _apply_base_dir_constraint(sanitized, base_dir, resolve)"""

content_split = content.split("def sanitize_path(")
before_sanitize_path = content_split[0]
after_sanitize_path = "def _sanitize_env_multiline" + content_split[1].split("def _sanitize_env_multiline")[1]

with open("src/taipanstack/security/sanitizers.py", "w") as f:
    f.write(before_sanitize_path + new_sanitize_path + "\n\n\n" + after_sanitize_path)
