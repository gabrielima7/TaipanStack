from taipanstack.security.sanitizers import sanitize_filename
import re

_INVALID_FILENAME_CHARS_RE = re.compile(r'[<>:"/\\|?*\x00-\x1f]')

def sanitize_filename_opt(
    filename: str,
    *,
    max_length: int = 255,
    replacement: str = "_",
    preserve_extension: bool = True,
) -> str:
    if type(filename) is not str:
        raise TypeError(f"filename must be str, got {type(filename).__name__}")

    if not filename:
        return "unnamed"

    slash_idx = max(filename.rfind("/"), filename.rfind("\\"))
    if slash_idx >= 0:
        name = filename[slash_idx + 1 :]
    else:
        name = filename

    idx = name.rfind(".")
    if idx > 0 and not all(c == "." for c in name) and name != "..":
        stem = name[:idx]
        suffix = name[idx:] if preserve_extension else ""
    else:
        stem = name
        suffix = ""

    if "\\" in replacement:
        safe_stem = _INVALID_FILENAME_CHARS_RE.sub(lambda _: replacement, stem)
    else:
        safe_stem = _INVALID_FILENAME_CHARS_RE.sub(replacement, stem)

    safe_stem = safe_stem.strip(". ")
    safe_stem = safe_stem.replace("/", replacement).replace("\\", replacement)

    if replacement:
        double_replacement = replacement + replacement
        while double_replacement in safe_stem:
            safe_stem = safe_stem.replace(double_replacement, replacement)
        safe_stem = safe_stem.strip(replacement)

    upper_stem = safe_stem.upper()
    if upper_stem in {"CON", "PRN", "AUX", "NUL"} or (upper_stem.startswith(("COM", "LPT")) and len(upper_stem) == 4 and upper_stem[3].isdigit()):
        safe_stem = f"{replacement}{safe_stem}"

    if not safe_stem:
        safe_stem = "unnamed"

    result = f"{safe_stem}{suffix}"

    if len(result) > max_length:
        available = max_length - len(suffix)
        if available > 0:
            safe_stem = safe_stem[:available]
            result = f"{safe_stem}{suffix}"
        else:
            result = result[:max_length]

    return result

import timeit
print(timeit.timeit(lambda: sanitize_filename("a/b/c/d/e/f/g/h/file.txt"), number=10000))
print(timeit.timeit(lambda: sanitize_filename_opt("a/b/c/d/e/f/g/h/file.txt"), number=10000))
