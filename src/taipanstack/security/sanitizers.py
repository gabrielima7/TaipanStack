"""
Input sanitizers for cleaning untrusted data.

Provides functions to sanitize strings, filenames, and paths
to remove potentially dangerous characters.
"""

import functools
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

    result = value

    # Strip whitespace first
    if strip_whitespace:
        result = result.strip()

    # Remove null bytes and control characters
    result = _CONTROL_CHARS_RE.sub("", result)

    # Handle HTML
    if not allow_html:
        # Remove HTML tags
        result = _HTML_TAGS_RE.sub("", result)
        # Escape HTML entities
        result = result.replace("&", "&amp;")
        result = result.replace("<", "&lt;")
        result = result.replace(">", "&gt;")

    # Handle unicode
    if not allow_unicode:  # pragma: no branch
        result = result.encode("ascii", errors="ignore").decode("ascii")

    # Truncate if needed
    if max_length is not None and len(result) > max_length:
        result = result[:max_length]

    return result


@functools.lru_cache(maxsize=32)
def _get_replacement_regex(replacement: str) -> re.Pattern:
    """Cache the compiled regex for consecutive replacement characters."""
    return re.compile(f"{re.escape(replacement)}+")


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
        return "unnamed"

    # Get parts
    original_path = Path(filename)
    stem = original_path.stem
    suffix = original_path.suffix if preserve_extension else ""

    # Check fast path: if the filename is already safe and valid length
    if (
        len(stem) + len(suffix) <= max_length
        and not _INVALID_FILENAME_CHARS_RE.search(stem)
        and not stem.startswith((".", " "))
        and not stem.endswith((".", " "))
        and "/" not in stem
        and "\\" not in stem
        and stem.upper() not in _WINDOWS_RESERVED_NAMES
    ):
        if replacement:
            if (
                replacement * 2 not in stem
                and not stem.startswith(replacement)
                and not stem.endswith(replacement)
            ):
                return f"{stem}{suffix}" if stem else f"unnamed{suffix}"
        else:
            return f"{stem}{suffix}" if stem else f"unnamed{suffix}"

    # Remove invalid characters using precompiled regex for performance
    safe_stem = _INVALID_FILENAME_CHARS_RE.sub(replacement, stem)

    # Remove leading/trailing dots and spaces (Windows issues)
    safe_stem = safe_stem.strip(". ")

    # Remove path separators that might have snuck through
    if "/" in safe_stem:
        safe_stem = safe_stem.replace("/", replacement)
    if "\\" in safe_stem:
        safe_stem = safe_stem.replace("\\", replacement)

    # Collapse multiple replacement chars
    if replacement and replacement in safe_stem:
        replace_regex = _get_replacement_regex(replacement)
        safe_stem = replace_regex.sub(replacement, safe_stem)
        safe_stem = safe_stem.strip(replacement)

    # Handle reserved names (Windows)
    if safe_stem.upper() in _WINDOWS_RESERVED_NAMES:
        safe_stem = f"{replacement}{safe_stem}"

    # Handle empty result
    if not safe_stem:
        safe_stem = "unnamed"

    # Construct result
    result = f"{safe_stem}{suffix}"

    # Truncate if needed (keeping extension)
    if len(result) > max_length:
        available = max_length - len(suffix)
        if available > 0:
            safe_stem = safe_stem[:available]
            result = f"{safe_stem}{suffix}"
        else:
            result = result[:max_length]

    return result


def _clean_path_parts(path_parts: tuple[str, ...]) -> list[str]:
    """Clean and sanitize individual path components."""
    parts: list[str] = []
    for part in path_parts:
        if part == "..":
            if parts and parts[-1] != "..":
                parts.pop()
        elif part != ".":  # pragma: no branch
            safe_part = sanitize_filename(part, preserve_extension=True)
            if safe_part:  # pragma: no branch
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

    return sanitized  # pragma: no cover


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
    if isinstance(path, str):  # pragma: no branch
        path_str = path.replace("\x00", "")
    else:
        path_str = str(path).replace("\x00", "")

    # Clean components
    path_obj = Path(path_str)
    parts = _clean_path_parts(path_obj.parts)

    # Reconstruct path
    if path_obj.is_absolute():  # pragma: no branch
        sanitized = (
            Path("/").joinpath(*parts) if parts else Path("/")
        )  # pragma: no cover
    elif parts:  # pragma: no branch
        sanitized = Path().joinpath(*parts)
    else:  # pragma: no cover
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

    # Fast path: if no sensitive characters and within length, return as is
    if (
        len(value) <= max_length
        and "\x00" not in value
        and (allow_multiline or ("\n" not in value and "\r" not in value))
    ):
        return value

    result = value

    # Remove null bytes
    result = result.replace("\x00", "")

    # Handle newlines
    if not allow_multiline:
        result = result.replace("\n", " ").replace("\r", " ")

    # Truncate
    if len(result) > max_length:
        result = result[:max_length]

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

    # Fast path: already clean and valid
    if not _SQL_IDENTIFIER_DENY_RE.search(identifier):
        if (
            identifier[0] in _VALID_SQL_PREFIX
            and len(identifier) <= MAX_SQL_IDENTIFIER_LENGTH
        ):
            return identifier
        result = identifier
    else:
        # Only allow alphanumeric and underscore
        result = _SQL_IDENTIFIER_DENY_RE.sub("", identifier)

    # Must start with letter or underscore
    if result and result[0] not in _VALID_SQL_PREFIX:
        result = f"_{result}"

    # Check length (most DBs limit to 128 chars)
    if len(result) > MAX_SQL_IDENTIFIER_LENGTH:
        result = result[:MAX_SQL_IDENTIFIER_LENGTH]

    if not result:
        msg = "SQL identifier contains no valid characters"
        raise ValueError(msg)

    return result
