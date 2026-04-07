import re
from pathlib import Path
from taipanstack.security.sanitizers import _clean_path_parts, sanitize_filename, _WINDOWS_RESERVED_NAMES
import time

def _clean_path_parts_old(path: Path) -> list[str]:
    """Clean and sanitize individual path components."""
    parts: list[str] = []
    anchor = path.anchor
    for part in path.parts:
        if part == "..":
            if parts and parts[-1] != ".." and parts[-1] != anchor:
                parts.pop()
        elif part != ".":  # pragma: no branch
            # fast-path bypass for perfectly safe segments (skip split/logic)
            # Find the stem to check against reserved names
            idx = part.rfind(".")
            stem = part[:idx] if idx > 0 and not all(c == "." for c in part) else part
            if (
                len(part) <= 255  # noqa: PLR2004
                and part.isascii()
                and part.replace(".", "").replace("-", "").replace("_", "").isalnum()
                and stem.upper() not in _WINDOWS_RESERVED_NAMES
            ):
                parts.append(part)
            else:
                safe_part = sanitize_filename(part, preserve_extension=True)
                if safe_part and safe_part != "..":  # pragma: no branch
                    parts.append(safe_part)
    return parts

_SAFE_PART_RE = re.compile(r"^[a-zA-Z0-9._-]+$")

def _clean_path_parts_new(path: Path) -> list[str]:
    """Clean and sanitize individual path components."""
    parts: list[str] = []
    anchor = path.anchor
    for part in path.parts:
        if part == "..":
            if parts and parts[-1] != ".." and parts[-1] != anchor:
                parts.pop()
        elif part != ".":  # pragma: no branch
            # fast-path bypass for perfectly safe segments (skip split/logic)
            # Using regex for faster isalnum + allowed chars check
            if (
                len(part) <= 255
                and _SAFE_PART_RE.match(part)
            ):
                # Find the stem to check against reserved names
                idx = part.rfind(".")
                stem = part[:idx] if idx > 0 and not all(c == "." for c in part) else part
                if stem.upper() not in _WINDOWS_RESERVED_NAMES:
                    parts.append(part)
                    continue

            safe_part = sanitize_filename(part, preserve_extension=True)
            if safe_part and safe_part != "..":  # pragma: no branch
                parts.append(safe_part)
    return parts

path_str = "a/b/c/d/e/f/g/h/file.txt"
path = Path(path_str)

start = time.time()
for _ in range(100000):
    _clean_path_parts_old(path)
print("old:", time.time() - start)

start = time.time()
for _ in range(100000):
    _clean_path_parts_new(path)
print("new:", time.time() - start)
