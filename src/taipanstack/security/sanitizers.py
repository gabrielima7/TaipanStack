"""
Input sanitizers for cleaning untrusted data.

Provides functions to sanitize strings, filenames, and paths
to remove potentially dangerous characters.
"""

import re
from pathlib import Path

# Constants to avoid magic values (PLR2004)
MAX_SQL_IDENTIFIER_LENGTH = 128  # pragma: no mutate

# Pre-compiled regex and sets for Performance Benchmarks
_INVALID_FILENAME_CHARS_RE = re.compile(r'[<>:"/\\|?*\x00-\x1f]')  # pragma: no mutate
_SQL_IDENTIFIER_DENY_RE = re.compile(r"[^a-zA-Z0-9_]")  # pragma: no mutate
_HTML_TAGS_RE = re.compile(r"<[^>]+>")  # pragma: no mutate
# Remove control characters (C0 and C1 sets)
_CONTROL_CHARS_RE = re.compile(
    r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]"
)  # pragma: no mutate
_VALID_SQL_PREFIX = frozenset(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
)  # pragma: no mutate
_WINDOWS_RESERVED_NAMES = frozenset(  # pragma: no mutate
    {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9",
    }
)

_ENV_MULTILINE_TRANSLATE = str.maketrans("\n\r", "  ")


def sanitize_string(
    value: str,
    *,
    max_length: int | None = None,
    allow_html: bool = False,
    allow_unicode: bool = True,
    strip_whitespace: bool = True,
) -> str:
    """Sanitize a string by removing dangerous characters.

    Args:
        value: The string to sanitize.
        max_length: Maximum length to truncate to.
        allow_html: Whether to keep HTML tags (default: False).
        allow_unicode: Whether to keep non-ASCII characters.
        strip_whitespace: Whether to strip leading/trailing whitespace.

    Returns:
        The sanitized string.

    Example:
        ```python
        sanitize_string("<script>alert('xss')</script>Hello")
        # Returns: "scriptalert('xss')/scriptHello"
        ```

    """
    if not isinstance(value, str):
        raise TypeError(f"value must be str, got {type(value).__name__}")

    if not value:
        return ""

    # Strip whitespace first
    result = value.strip() if strip_whitespace else value

    # Remove null bytes and control characters
    result = _CONTROL_CHARS_RE.sub("", result)

    # Handle HTML
    if not allow_html:
        if "<" in result or ">" in result:
            result = _HTML_TAGS_RE.sub("", result)
        if "&" in result or "<" in result or ">" in result:
            result = (
                result.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            )

    # Handle unicode
    if not allow_unicode and not result.isascii():
        result = result.encode("ascii", errors="ignore").decode("ascii")

    # Truncate if needed
    if max_length is not None and len(result) > max_length:
        result = result[:max_length]

    return result


def sanitize_filename(
    filename: str,
    *,
    max_length: int = 255,
    replacement: str = "_",
    preserve_extension: bool = True,
) -> str:
    """Sanitize a filename to be safe for filesystem use.

    Removes or replaces characters that are:
    - Not allowed in filenames on various OSes
    - Potentially dangerous (path separators, etc.)

    Args:
        filename: The filename to sanitize.
        max_length: Maximum length for the filename.
        replacement: Character to replace invalid chars with.
        preserve_extension: Keep original extension.

    Returns:
        The sanitized filename.

    Example:
        ```python
        sanitize_filename("my/../file<>:name.txt")
        # Returns: 'my_file_name.txt'
        ```

    """
    if not isinstance(filename, str):
        raise TypeError(f"filename must be str, got {type(filename).__name__}")

    if not filename:
        filename = "unnamed"

    # Extract stem and suffix natively to avoid pathlib overhead
    slash_idx = max(filename.rfind("/"), filename.rfind("\\"))
    name = filename[slash_idx + 1 :] if slash_idx >= 0 else filename
    idx = name.rfind(".")

    if idx > 0 and name != ".." and not name.startswith("..") and name.strip(".") != "":
        stem = name[:idx]
        suffix = name[idx:] if preserve_extension else ""
    else:
        stem = name
        suffix = ""

    # Remove invalid characters using precompiled regex
    try:
        if "\\" in replacement:
            safe_stem = _INVALID_FILENAME_CHARS_RE.sub(lambda _: replacement, stem)
        else:
            safe_stem = _INVALID_FILENAME_CHARS_RE.sub(replacement, stem)
    except re.error:  # pragma: no cover
        safe_stem = _INVALID_FILENAME_CHARS_RE.sub("_", stem)

    # Clean residual path chars
    safe_stem = (
        safe_stem.strip(". ").replace("/", replacement).replace("\\", replacement)
    )

    # Collapse multiple replacement chars
    if replacement:
        double_replacement = replacement + replacement
        while double_replacement in safe_stem:
            safe_stem = safe_stem.replace(double_replacement, replacement)
        safe_stem = safe_stem.strip(replacement)

    # Handle reserved names (Windows)
    if safe_stem.upper() in _WINDOWS_RESERVED_NAMES:
        safe_stem = f"{replacement}{safe_stem}"

    # Handle empty result
    if not safe_stem:
        safe_stem = "unnamed"

    # Truncate while keeping extension if possible
    result = f"{safe_stem}{suffix}"
    if len(result) > max_length:
        available = max_length - len(suffix)
        if available > 0:
            return f"{safe_stem[:available]}{suffix}"
        return result[:max_length]

    return result


def _clean_path_parts(path: Path) -> list[str]:
    """Clean and sanitize individual path components."""
    parts: list[str] = []
    anchor = path.anchor
    for part in path.parts:
        if part == "..":
            if parts and parts[-1] != ".." and parts[-1] != anchor:
                parts.pop()
        elif part != ".":  # pragma: no branch
            safe_part = sanitize_filename(part, preserve_extension=True)
            if safe_part and safe_part != "..":  # pragma: no branch
                parts.append(safe_part)
    return parts


def _apply_base_dir_constraint(
    sanitized: Path,
    base_dir: Path | str | None,
    resolve: bool,
) -> Path:
    """Apply base directory constraints to a sanitized path."""
    if base_dir is None:
        return sanitized

    base = Path(base_dir).resolve()
    if resolve:
        try:
            return sanitized.resolve()
        except (OSError, RuntimeError) as e:
            msg = f"Cannot resolve path: {e}"
            raise ValueError(msg) from e

    # Make absolute relative to base
    if not sanitized.is_absolute():  # pragma: no branch
        return base / sanitized

    return sanitized


def sanitize_path(
    path: str | Path,
    *,
    base_dir: Path | None = None,
    max_depth: int | None = 10,
    resolve: bool = False,
) -> Path:
    """Sanitize a path to prevent traversal and normalize it.

    Args:
        path: The path to sanitize.
        base_dir: Optional base directory to constrain to.
        max_depth: Maximum directory depth allowed.
        resolve: Whether to resolve the path (requires it to exist).

    Returns:
        The sanitized Path object.

    Raises:
        ValueError: If path is invalid or too deep.

    """
    if isinstance(path, str):
        if "\x00" in path:  # pragma: no branch
            path = path.replace("\x00", "")
        path = Path(path)
    else:  # pragma: no branch
        path = Path(path)

    # Clean components
    parts = _clean_path_parts(path)

    # Reconstruct path
    if path.is_absolute():  # pragma: no branch
        # Use path.anchor to correctly preserve absolute roots on Windows (e.g. C:\)
        anchor = Path(path.anchor)
        sanitized = anchor.joinpath(*parts) if parts else anchor
    elif parts:  # pragma: no branch
        sanitized = Path().joinpath(*parts)
    else:
        sanitized = Path()

    # Check depth
    depth = len(sanitized.parts)
    if max_depth is not None and depth > max_depth:
        msg = f"Path depth {depth} exceeds maximum of {max_depth}"
        raise ValueError(msg)

    # Constrain to base_dir
    return _apply_base_dir_constraint(sanitized, base_dir, resolve)


def sanitize_env_value(
    value: str,
    *,
    max_length: int = 4096,
    allow_multiline: bool = False,
) -> str:
    """Sanitize a value for use as an environment variable.

    Args:
        value: The value to sanitize.
        max_length: Maximum length allowed.
        allow_multiline: Whether to allow newlines.

    Returns:
        The sanitized value.

    Raises:
        TypeError: If value is not a string.

    """
    if not isinstance(value, str):
        raise TypeError(f"value must be str, got {type(value).__name__}")

    if not value:
        return ""

    val_len = len(value)

    if allow_multiline:
        if "\x00" not in value and val_len <= max_length:
            return value
        result = value.replace("\x00", "")
    else:
        if (
            val_len <= max_length
            and "\x00" not in value
            and "\n" not in value
            and "\r" not in value
        ):
            return value
        result = value.translate(_ENV_MULTILINE_TRANSLATE).replace("\x00", "")

    if len(result) > max_length:
        return result[:max_length]
    return result


def sanitize_sql_identifier(identifier: str) -> str:
    """Sanitize a SQL identifier (table/column name).

    Note: This is NOT for SQL values - use parameterized queries for those!

    Args:
        identifier: The identifier to sanitize.

    Returns:
        The sanitized identifier.

    Raises:
        TypeError: If identifier is not a string.
        ValueError: If identifier is empty or too long.

    """
    if not isinstance(identifier, str):
        raise TypeError(f"identifier must be str, got {type(identifier).__name__}")

    if not identifier:
        msg = "SQL identifier cannot be empty"
        raise ValueError(msg)

    length = len(identifier)

    # Fast path: already clean and valid
    if (
        identifier.isidentifier()
        and identifier.isascii()
        and length <= MAX_SQL_IDENTIFIER_LENGTH
    ):
        return identifier

    result = _SQL_IDENTIFIER_DENY_RE.sub("", identifier)

    # Must start with letter or underscore
    if result:
        first_char = result[0]
        if not first_char.isalpha() and first_char != "_":
            result = f"_{result}"

    # Check length (most DBs limit to 128 chars)
    if len(result) > MAX_SQL_IDENTIFIER_LENGTH:
        result = result[:MAX_SQL_IDENTIFIER_LENGTH]

    if not result:
        msg = "SQL identifier contains no valid characters"
        raise ValueError(msg)

    return result
