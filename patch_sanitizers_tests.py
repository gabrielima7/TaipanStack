from pathlib import Path

path = Path("tests/test_security_sanitizers_operations.py")
content = path.read_text()

# We need to test the condition where safe_part is completely empty but not ".."
# "a/b/invalid/c" doesn't hit the `else` branch of `_is_safe_path_part` unless "invalid" isn't safe.
# Let's use something definitely unsafe like "a/b/<!>/c".
# The `sanitize_filename` is called inside `_clean_path_parts`.
new_test = """
    def test_security_sanitizers_path_safe_part_empty(self) -> None:
        from taipanstack.security.sanitizers import sanitize_path
        from unittest.mock import patch

        # We need a case where sanitize_filename(part) returns "" for an unsafe part.
        # "a/b/<!>/c" is unsafe.
        with patch("taipanstack.security.sanitizers.sanitize_filename", return_value=""):
            path = sanitize_path("a/b/<!>/c")
            assert str(path) == "a/b/c"
"""
import re
content = re.sub(r'    def test_security_sanitizers_path_safe_part_empty.*?assert str\(path\) == "a/b/c"', new_test.strip("\n"), content, flags=re.DOTALL)
path.write_text(content)
