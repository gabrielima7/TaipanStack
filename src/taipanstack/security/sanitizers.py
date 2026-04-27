"""
Input sanitizers for cleaning untrusted data.

Provides functions to sanitize strings, filenames, and paths
to remove potentially dangerous characters.
"""

import re
from pathlib import Path

# Constants to avoid magic values (PLR2004)
MAX_SQL_IDENTIFIER_LENGTH = 128  # pragma: no mutate
MAX_PATH_LENGTH = 4096  # pragma: no mutate

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


def _handle_html(result: str, allow_html: bool) -> str:
    """Remove HTML tags and escape entities if not allowed."""
    if allow_html:
        return result
    result = _HTML_TAGS_RE.sub("", result)
    result = result.replace("&", "&amp;")
    result = result.replace("<", "&lt;")
    return result.replace(">", "&gt;")


def _handle_unicode(result: str, allow_unicode: bool) -> str:
    """Filter out non-ASCII characters if unicode is not allowed."""
    if allow_unicode:
        return result
    return result.encode("ascii", errors="ignore").decode("ascii")


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

    result = value.strip() if strip_whitespace else value
    result = _CONTROL_CHARS_RE.sub("", result)
    result = _handle_html(result, allow_html)
    result = _handle_unicode(result, allow_unicode)

    if max_length is not None and len(result) > max_length:
        return result[:max_length]
    return result


def _extract_stem_and_suffix(
    filename: str, preserve_extension: bool
) -> tuple[str, str]:
    """Extract stem and suffix from a filename."""
    # Get parts using native string manipulation instead of Path for performance
    # Emulate Path(filename).name
    name = filename
    slash_idx = max(name.rfind("/"), name.rfind("\\"))
    if slash_idx >= 0:
        name = name[slash_idx + 1 :]

    stem = name
    suffix = ""

    idx = name.rfind(".")
    # Pathlib considers pure dotfiles (like ".hidden") or "..." as stem no suffix
    if idx > 0 and not all(c == "." for c in name) and name != "..":
        stem = name[:idx]
        suffix = name[idx:] if preserve_extension else ""
    else:
        stem = name

    return stem, suffix


def _remove_invalid_chars(stem: str, replacement: str) -> str:
    """Remove or replace invalid characters in a filename stem."""
    try:
        if "\\" in replacement:
            # Use lambda to avoid processing regex escape sequences in replacement
            safe_stem = _INVALID_FILENAME_CHARS_RE.sub(lambda _: replacement, stem)
        else:
            safe_stem = _INVALID_FILENAME_CHARS_RE.sub(replacement, stem)
    except re.error:
        safe_stem = _INVALID_FILENAME_CHARS_RE.sub("_", stem)

    # Remove leading/trailing dots and spaces (Windows issues)
    safe_stem = safe_stem.strip(". ")

    # Remove path separators that might have snuck through
    safe_stem = safe_stem.replace("/", replacement)
    safe_stem = safe_stem.replace("\\", replacement)

    return safe_stem


def _collapse_replacements(safe_stem: str, replacement: str) -> str:
    """Collapse multiple consecutive replacement characters."""
    if replacement:
        double_replacement = replacement + replacement
        while double_replacement in safe_stem:
            safe_stem = safe_stem.replace(double_replacement, replacement)
        safe_stem = safe_stem.strip(replacement)
    return safe_stem


def _truncate_filename(safe_stem: str, suffix: str, max_length: int) -> str:
    """Truncate the filename while keeping the extension if possible."""
    result = f"{safe_stem}{suffix}"
    if len(result) > max_length:
        available = max_length - len(suffix)
        if available > 0:
            safe_stem = safe_stem[:available]
            result = f"{safe_stem}{suffix}"
        else:
            result = result[:max_length]
    return result


def _is_filename_safe(filename: str, max_length: int, stem: str) -> bool:
    """Check if a filename is already safe without any modifications."""
    return (
        len(filename) <= max_length
        and filename not in {"..", "."}
        and stem.upper() not in _WINDOWS_RESERVED_NAMES
        and filename.isascii()
        and filename.replace(".", "").replace("-", "").replace("_", "").isalnum()
    )


def _finalize_filename(
    safe_stem: str, replacement: str, suffix: str, max_length: int
) -> str:
    """Finalize the sanitized filename by handling reserved names and empty results."""
    # Handle reserved names (Windows)
    if safe_stem.upper() in _WINDOWS_RESERVED_NAMES:
        safe_stem = f"{replacement}{safe_stem}"

    # Handle empty result
    if not safe_stem:
        safe_stem = "unnamed"

    return _truncate_filename(safe_stem, suffix, max_length)


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

    stem, suffix = _extract_stem_and_suffix(filename, preserve_extension)

    if _is_filename_safe(filename, max_length, stem):
        return f"{stem}{suffix}"

    safe_stem = _remove_invalid_chars(stem, replacement)
    safe_stem = _collapse_replacements(safe_stem, replacement)

    return _finalize_filename(safe_stem, replacement, suffix, max_length)


def _get_stem(part: str) -> str:
    """Get the stem of a path part."""
    idx = part.rfind(".")
    return part[:idx] if idx > 0 and not all(c == "." for c in part) else part


def _is_safe_path_part(part: str, stem: str) -> bool:
    """Check if a path part is safe."""
    return (
        len(part) <= 255  # noqa: PLR2004
        and part.isascii()
        and part.replace(".", "").replace("-", "").replace("_", "").isalnum()
        and stem.upper() not in _WINDOWS_RESERVED_NAMES
    )


def _handle_dot_dot(parts: list[str], anchor: str) -> None:
    """Handle '..' by popping the last part if safe."""
    if parts and parts[-1] != ".." and parts[-1] != anchor:
        parts.pop()


def _handle_normal_part(part: str, parts: list[str]) -> None:
    """Handle a normal part by checking if it's safe or sanitizing it."""
    stem = _get_stem(part)
    if _is_safe_path_part(part, stem):
        parts.append(part)
    else:
        safe_part = sanitize_filename(part, preserve_extension=True)
        if safe_part and safe_part != "..":  # pragma: no branch
            parts.append(safe_part)


def _process_path_part(part: str, parts: list[str], anchor: str) -> None:
    """Process a single path component, updating the parts list inline."""
    if part == "..":
        _handle_dot_dot(parts, anchor)
    elif part != ".":  # pragma: no branch
        _handle_normal_part(part, parts)


def _clean_path_parts(path: Path) -> list[str]:
    """Clean and sanitize individual path components."""
    parts: list[str] = []
    anchor = path.anchor
    for part in path.parts:
        _process_path_part(part, parts, anchor)
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
        if len(path) > MAX_PATH_LENGTH:
            msg = "Path length exceeds maximum allowed"
            raise ValueError(msg)
        if "\x00" in path:  # pragma: no branch
            path = path.replace("\x00", "")
        path = Path(path)
    else:  # pragma: no branch
        if len(str(path)) > MAX_PATH_LENGTH:
            msg = "Path length exceeds maximum allowed"
            raise ValueError(msg)
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


def _sanitize_env_multiline(value: str, max_length: int) -> str:
    """Sanitize an environment value allowing multiline characters."""
    if "\x00" not in value and len(value) <= max_length:
        return value
    return value.replace("\x00", "")


def _sanitize_env_singleline(value: str, max_length: int) -> str:
    """Sanitize an environment value, converting multiline to spaces."""
    if (
        "\x00" not in value
        and "\n" not in value
        and "\r" not in value
        and len(value) <= max_length
    ):
        return value
    return value.replace("\x00", "").replace("\n", " ").replace("\r", " ")


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

    if allow_multiline:
        result = _sanitize_env_multiline(value, max_length)
    else:
        result = _sanitize_env_singleline(value, max_length)

    if len(result) > max_length:
        return result[:max_length]
    return result


def _sanitize_sql_identifier_slow_path(identifier: str) -> str:
    """Apply slow path sanitization for SQL identifiers."""
    result = _SQL_IDENTIFIER_DENY_RE.sub("", identifier)

    # Must start with letter or underscore
    if result and not result[0].isalpha() and result[0] != "_":
        result = f"_{result}"

    # Check length (most DBs limit to 128 chars)
    if len(result) > MAX_SQL_IDENTIFIER_LENGTH:
        result = result[:MAX_SQL_IDENTIFIER_LENGTH]

    if not result:
        msg = "SQL identifier contains no valid characters"
        raise ValueError(msg)

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
    if type(identifier) is str:
        if (
            len(identifier) <= 128  # noqa: PLR2004
            and identifier.isascii()
            and identifier.isidentifier()
        ):
            return identifier

        if not identifier:
            msg = "SQL identifier cannot be empty"
            raise ValueError(msg)

        return _sanitize_sql_identifier_slow_path(identifier)

    raise TypeError(f"identifier must be str, got {type(identifier).__name__}")
