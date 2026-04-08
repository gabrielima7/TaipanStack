import subprocess
import os

with open("src/taipanstack/security/sanitizers.py", "r") as f:
    content = f.read()

# Refactor sanitize_string
new_sanitize_string = """def _strip_html(value: str) -> str:
    \"\"\"Remove HTML tags and escape HTML entities.\"\"\"
    result = _HTML_TAGS_RE.sub("", value)
    result = result.replace("&", "&amp;")
    result = result.replace("<", "&lt;")
    result = result.replace(">", "&gt;")
    return result

def sanitize_string(
    value: str,
    *,
    max_length: int | None = None,
    allow_html: bool = False,
    allow_unicode: bool = True,
    strip_whitespace: bool = True,
) -> str:
    \"\"\"Sanitize a string by removing dangerous characters.

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

    \"\"\"
    if not isinstance(value, str):
        raise TypeError(f"value must be str, got {type(value).__name__}")

    if not value:
        return ""

    result = value

    if strip_whitespace:
        result = result.strip()

    result = _CONTROL_CHARS_RE.sub("", result)

    if not allow_html:
        result = _strip_html(result)

    if not allow_unicode:
        result = result.encode("ascii", errors="ignore").decode("ascii")

    if max_length is not None and len(result) > max_length:
        result = result[:max_length]

    return result"""

import re
content = re.sub(r'def sanitize_string\(.*?(?=def _extract_stem_and_suffix)', new_sanitize_string + '\n\n\n', content, flags=re.DOTALL)

with open("src/taipanstack/security/sanitizers.py", "w") as f:
    f.write(content)
