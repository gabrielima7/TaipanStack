import re
from pathlib import Path
import os
def sanitize_filename(
    filename: str,
    *,
    max_length: int = 255,
    replacement: str = "_",
    preserve_extension: bool = True,
) -> str:
    if not isinstance(filename, str):
        raise TypeError(f"filename must be str, got {type(filename).__name__}")

    if not filename:
        filename = "unnamed"

    # Get parts
    stripped = filename.rstrip("/\\")
    if not stripped:
        # On POSIX, a backslash is a valid filename character, so Path("\\").name == "\\"
        # On Windows, Path("\\").name == ""
        if os.name != "nt" and "\\" in filename and "/" not in filename:
            name = filename
        else:
            name = ""
    elif os.name == "nt":
        name = stripped.replace("\\", "/").split("/")[-1]
    else:
        name = stripped.split("/")[-1]

    i = name.rfind(".")
    if name in ("..", ".") or i <= 0 or i == len(name) - 1:
        stem, suffix = name, ""
    else:
        stem, suffix = name[:i], name[i:]

    if not preserve_extension:
        suffix = ""

    # Remove invalid characters using precompiled regex for performance
    _INVALID_FILENAME_CHARS_RE = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
    try:
        # Use lambda to avoid processing regex escape sequences in replacement string
        safe_stem = _INVALID_FILENAME_CHARS_RE.sub(lambda _: replacement, stem)
    except re.error:  # pragma: no cover
        safe_stem = _INVALID_FILENAME_CHARS_RE.sub("_", stem)

    # Remove leading/trailing dots and spaces (Windows issues)
    safe_stem = safe_stem.strip(". ")

    # Remove path separators that might have snuck through
    safe_stem = safe_stem.replace("/", replacement)
    safe_stem = safe_stem.replace("\\", replacement)

    # Collapse multiple replacement chars
    if replacement:
        double_replacement = replacement * 2
        while double_replacement in safe_stem:
            safe_stem = safe_stem.replace(double_replacement, replacement)
        safe_stem = safe_stem.strip(replacement)

    # Handle empty result
    if not safe_stem:
        safe_stem = "unnamed"

    return safe_stem

def orig_sanitize(
    filename: str,
    *,
    max_length: int = 255,
    replacement: str = "_",
    preserve_extension: bool = True,
) -> str:
    if not isinstance(filename, str):
        raise TypeError(f"filename must be str, got {type(filename).__name__}")

    if not filename:
        filename = "unnamed"

    original_path = Path(filename)
    stem = original_path.stem

    _INVALID_FILENAME_CHARS_RE = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
    safe_stem = _INVALID_FILENAME_CHARS_RE.sub(lambda _: replacement, stem)

    safe_stem = safe_stem.strip(". ")
    safe_stem = safe_stem.replace("/", replacement)
    safe_stem = safe_stem.replace("\\", replacement)

    if replacement:
        double_replacement = replacement * 2
        while double_replacement in safe_stem:
            safe_stem = safe_stem.replace(double_replacement, replacement)
        safe_stem = safe_stem.strip(replacement)

    if not safe_stem:
        safe_stem = "unnamed"
    return safe_stem

os.name = "posix"
print("POSIX orig:", repr(orig_sanitize("\\")))
print("POSIX new:", repr(sanitize_filename("\\")))

os.name = "nt"
print("NT orig:", repr(orig_sanitize("\\")))
print("NT new:", repr(sanitize_filename("\\")))
