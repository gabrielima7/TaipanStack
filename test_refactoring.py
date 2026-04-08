import subprocess
import os

with open("src/taipanstack/security/sanitizers.py", "r") as f:
    content = f.read()

# Refactor _process_path_part
new_process_path = """def _process_parent_dir(parts: list[str], anchor: str) -> None:
    \"\"\"Process a parent directory reference '..' .\"\"\"
    if not parts:
        return
    if parts[-1] == "..":
        return
    if parts[-1] == anchor:
        return
    parts.pop()

def _process_path_part(part: str, parts: list[str], anchor: str) -> None:
    \"\"\"Process a single path component, updating the parts list inline.\"\"\"
    if part == "..":
        _process_parent_dir(parts, anchor)
        return
    if part == ".":
        return

    stem = _get_stem(part)
    if _is_safe_path_part(part, stem):
        parts.append(part)
        return

    safe_part = sanitize_filename(part, preserve_extension=True)
    if safe_part and safe_part != "..":
        parts.append(safe_part)"""

import re
content = re.sub(r'def _process_path_part\(part: str, parts: list\[str\], anchor: str\) -> None:(?:.|\n)*?(?=def _clean_path_parts)', new_process_path + '\n\n\n', content)

# Refactor sanitize_filename
new_sanitize_filename = """def _is_safe_filename_fast_path(
    filename: str, stem: str, max_length: int
) -> bool:
    \"\"\"Check if a filename meets fast-path criteria.\"\"\"
    return (
        len(filename) <= max_length
        and filename not in {"..", "."}
        and stem.upper() not in _WINDOWS_RESERVED_NAMES
        and filename.isascii()
        and filename.replace(".", "").replace("-", "").replace("_", "").isalnum()
    )

def sanitize_filename(
    filename: str,
    *,
    max_length: int = 255,
    replacement: str = "_",
    preserve_extension: bool = True,
) -> str:
    \"\"\"Sanitize a filename to be safe for filesystem use.

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

    \"\"\"
    if not isinstance(filename, str):
        raise TypeError(f"filename must be str, got {type(filename).__name__}")

    if not filename:
        filename = "unnamed"

    stem, suffix = _extract_stem_and_suffix(filename, preserve_extension)

    # Fast-path for already safe, typical filenames
    if _is_safe_filename_fast_path(filename, stem, max_length):
        return f"{stem}{suffix}"

    # Remove invalid characters using precompiled regex for performance
    safe_stem = _remove_invalid_chars(stem, replacement)

    # Collapse multiple replacement chars
    safe_stem = _collapse_replacements(safe_stem, replacement)

    # Handle reserved names (Windows)
    if safe_stem.upper() in _WINDOWS_RESERVED_NAMES:
        safe_stem = f"{replacement}{safe_stem}"

    # Handle empty result
    if not safe_stem:
        safe_stem = "unnamed"

    return _truncate_filename(safe_stem, suffix, max_length)"""

content = re.sub(r'def sanitize_filename\(.*?(?=def _get_stem)', new_sanitize_filename + '\n\n\n', content, flags=re.DOTALL)

with open("src/taipanstack/security/sanitizers.py", "w") as f:
    f.write(content)
