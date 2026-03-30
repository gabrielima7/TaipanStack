import re
from pathlib import Path
from typing import Sequence

def sanitize_filename_optimized(
    filename: str,
    *,
    max_length: int = 255,
    replacement: str = "_",
    preserve_extension: bool = True,
) -> str:
    if not isinstance(filename, str):
        raise TypeError(f"filename must be str, got {type(filename).__name__}")

    if not filename:
        return "unnamed"

    # Fast path: already safe?
    # To properly check fast path, we need to know what constitutes safe. Let's just do standard processing for now.
