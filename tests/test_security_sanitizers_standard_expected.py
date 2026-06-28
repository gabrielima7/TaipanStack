"""Tests for input sanitizers."""

from pathlib import Path

import pytest

from taipanstack.security.sanitizers import (
    sanitize_filename,
    sanitize_path,
    sanitize_string,
)


class TestSanitizeString:
    """Tests for sanitize_string function."""

    def test_security_sanitizers_empty_string_standard_expected(self) -> None:
        """Test empty string returns empty."""
        assert sanitize_string("") == ""

    def test_security_sanitizers_normal_string_unchanged_standard_expected(
        self,
    ) -> None:
        """Test normal string passes through."""
        assert sanitize_string("Hello World") == "Hello World"

    def test_security_sanitizers_strips_whitespace_standard_expected(self) -> None:
        """Test whitespace is stripped by default."""
        assert sanitize_string("  hello  ") == "hello"

    @pytest.mark.parametrize(
        "whitespace",
        [
            " ",  # Space
            "\t",  # Tab
            "\n",  # Newline
            "\r",  # Carriage return
            "\v",  # Vertical tab
            "\f",  # Form feed
            "\xa0",  # Non-breaking space
            " \t\n\r ",  # Mixed whitespace
        ],
    )
    def test_security_sanitizers_strips_various_whitespace_standard_expected(
        self, whitespace: str
    ) -> None:
        """Test various whitespace characters are stripped correctly."""
        # Test leading/trailing whitespace
        assert sanitize_string(f"{whitespace}hello{whitespace}") == "hello"
        # Test string with only whitespace (should become empty)
        assert sanitize_string(whitespace) == ""

    def test_security_sanitizers_no_strip_whitespace_standard_expected(self) -> None:
        """Test whitespace preserved when disabled."""
        result = sanitize_string("  hello  ", strip_whitespace=False)
        assert result == "  hello  "

    def test_security_sanitizers_removes_null_bytes_standard_expected(self) -> None:
        """Test null bytes are removed."""
        assert sanitize_string("hel\x00lo") == "hello"

    def test_security_sanitizers_removes_html_tags_standard_expected(self) -> None:
        """Test HTML tags are removed by default."""
        result = sanitize_string("<script>alert('xss')</script>")
        assert "<script>" not in result
        assert "alert" in result  # Text content preserved

    def test_security_sanitizers_allows_html_when_enabled_standard_expected(
        self,
    ) -> None:
        """Test HTML tags preserved when allowed."""
        result = sanitize_string("<b>bold</b>", allow_html=True)
        assert "<b>" in result

    def test_security_sanitizers_removes_control_characters_standard_expected(
        self,
    ) -> None:
        """Test control characters are removed."""
        result = sanitize_string("hello\x01\x02world")
        assert result == "helloworld"

    def test_security_sanitizers_preserves_newlines_standard_expected(self) -> None:
        """Test newlines are preserved."""
        result = sanitize_string("line1\nline2")
        assert "\n" in result

    def test_security_sanitizers_removes_unicode_when_disabled_standard_expected(
        self,
    ) -> None:
        """Test unicode removed when not allowed."""
        result = sanitize_string("héllo wörld", allow_unicode=False)
        assert "é" not in result
        assert "ö" not in result

    def test_security_sanitizers_truncates_to_max_length_standard_expected(
        self,
    ) -> None:
        """Test string is truncated."""
        result = sanitize_string("hello world", max_length=5)
        assert result == "hello"
        assert len(result) == 5

    def test_security_sanitizers_escapes_html_entities_standard_expected(self) -> None:
        """Test HTML entities are escaped after tag removal."""
        # Note: < and > inside text (not as tags) get escaped after tag stripping
        result = sanitize_string("text&more")
        assert "&amp;" in result


class TestSanitizeFilename:
    """Tests for sanitize_filename function."""

    def test_security_sanitizers_empty_filename_standard_expected(self) -> None:
        """Test empty filename returns 'unnamed'."""
        assert sanitize_filename("") == "unnamed"

    def test_security_sanitizers_normal_filename_standard_expected(self) -> None:
        """Test normal filename passes through."""
        assert sanitize_filename("test.txt") == "test.txt"

    def test_security_sanitizers_removes_path_characters_standard_expected(
        self,
    ) -> None:
        """Test path characters are removed."""
        result = sanitize_filename("../etc/passwd.txt")
        assert "/" not in result
        assert ".." not in result

    def test_security_sanitizers_removes_invalid_windows_chars_standard_expected(
        self,
    ) -> None:
        """Test Windows invalid chars are removed."""
        result = sanitize_filename("file<>:name.txt")
        assert "<" not in result
        assert ">" not in result
        assert ":" not in result

    def test_security_sanitizers_preserves_extension_standard_expected(self) -> None:
        """Test extension is preserved by default."""
        result = sanitize_filename("bad<file>name.txt")
        assert result.endswith(".txt")

    def test_security_sanitizers_no_preserve_extension_standard_expected(self) -> None:
        """Test extension not preserved when disabled."""
        result = sanitize_filename("test.txt", preserve_extension=False)
        assert result == "test"

    def test_security_sanitizers_handles_reserved_names_standard_expected(self) -> None:
        """Test Windows reserved names are handled."""
        result = sanitize_filename("CON")
        assert result != "CON"
        assert result.upper() != "CON"

    def test_security_sanitizers_handles_dot_names_standard_expected(self) -> None:
        """Test fast-path avoids passing dotfiles directly without stripping."""
        result = sanitize_filename(".")
        assert result == "unnamed"
        result2 = sanitize_filename("..")
        assert result2 == "unnamed"

    def test_security_sanitizers_max_length_with_extension_standard_expected(
        self,
    ) -> None:
        """Test max length preserves extension."""
        result = sanitize_filename("verylongfilename.txt", max_length=10)
        assert len(result) <= 10
        assert result.endswith(".txt")

    def test_security_sanitizers_max_length_with_long_extension_standard_expected(
        self,
    ) -> None:
        """Test max length when extension is longer than max_length."""
        # Extension is ".extension" (10 chars), max_length is 5
        result = sanitize_filename("file.extension", max_length=5)
        assert len(result) == 5
        assert result == "file."

    def test_security_sanitizers_custom_replacement_standard_expected(self) -> None:
        """Test custom replacement character."""
        result = sanitize_filename("bad:name.txt", replacement="-")
        assert ":" not in result
        assert "-" in result

    def test_security_sanitizers_collapses_multiple_replacements_standard_expected(
        self,
    ) -> None:
        """Test multiple invalid chars become single replacement."""
        result = sanitize_filename("a:::b.txt")
        assert "___" not in result  # Collapsed to single _


class TestSanitizePath:
    """Tests for sanitize_path function."""

    def test_security_sanitizers_sanitize_path_absolute_with_base_dir_standard_expected(
        self, tmp_path: Path
    ) -> None:
        """Test sanitize_path when sanitized is absolute and base_dir is given."""
        # When `sanitized.is_absolute()` is True, `_apply_base_dir_constraint` returns `sanitized`
        # if `base_dir` is not None and resolve is False.
        path = tmp_path / "absolute/path"

        base_dir = tmp_path / "base"
        base_dir.mkdir()

        result = sanitize_path(path, base_dir=base_dir, max_depth=None, resolve=False)
        assert result.is_absolute()
        assert result.parts[-2:] == ("absolute", "path")

    def test_security_sanitizers_sanitize_path_absolute_with_parts_standard_expected(
        self, tmp_path: Path
    ) -> None:
        """Test sanitize_path when path is absolute and has parts."""
        # Covers path reconstruction when path.is_absolute() is True and parts is truthy
        path = tmp_path / "absolute/path"
        result = sanitize_path(path, max_depth=None)
        assert result.is_absolute()
        assert result.parts[-2:] == ("absolute", "path")

    def test_security_sanitizers_sanitize_path_empty_standard_expected(self) -> None:
        """Test sanitize_path when path is empty (no parts, not absolute)."""
        # Covers the else branch where parts are empty and path is not absolute
        result = sanitize_path("")
        assert not result.is_absolute()
        assert result == Path()

    def test_security_sanitizers_simple_path_standard_expected(self) -> None:
        """Test simple path passes through."""
        result = sanitize_path("test/file.txt")
        assert "test" in str(result)
        assert "file.txt" in str(result)

    def test_security_sanitizers_removes_traversal_standard_expected(self) -> None:
        """Test path traversal is removed."""
        result = sanitize_path("../etc/passwd")
        assert ".." not in str(result)

    def test_security_sanitizers_removes_null_bytes_standard_expected(self) -> None:
        """Test null bytes in path are removed."""
        result = sanitize_path("test\x00file.txt")
        assert "\x00" not in str(result)

    def test_security_sanitizers_max_depth_enforced_standard_expected(self) -> None:
        """Test max depth is enforced."""
        deep_path = "/".join(["dir"] * 20)
        with pytest.raises(ValueError, match="depth"):
            sanitize_path(deep_path, max_depth=5)

    def test_security_sanitizers_with_base_dir_standard_expected(
        self, tmp_path: Path
    ) -> None:
        """Test path with base directory."""
        base = tmp_path / "base"
        base.mkdir()
        # max_depth=None to avoid depth check (CI paths can be very long)
        result = sanitize_path("subdir/file.txt", base_dir=base, max_depth=None)
        # Check result is under base directory using Path comparison
        assert str(base) in str(result)

    def test_security_sanitizers_removes_parent_traversal_standard_expected(
        self,
    ) -> None:
        """Test path traversal with parent directory is resolved."""
        result = sanitize_path("foo/../bar")
        assert "bar" in str(result)
        assert "foo" not in str(result)

    def test_security_sanitizers_removes_multiple_parent_traversals_standard_expected(
        self,
    ) -> None:
        """Test path traversal with multiple parent directories."""
        result = sanitize_path("foo/bar/../../baz")
        assert "baz" in str(result)
        assert "foo" not in str(result)
        assert "bar" not in str(result)

    def test_security_sanitizers_handles_empty_parts_standard_expected(self) -> None:
        """Test path with empty parts after sanitization."""
        # To trigger an absolute path traversal resulting in empty parts cross-platform,
        # we resolve the root path (so it gets C:/ on Windows) and append ..
        abs_root = Path("/").resolve()
        abs_traversal = abs_root / ".."
        result = sanitize_path(abs_traversal)

        # `sanitize_path` reconstructs an absolute path that's empty by preserving the anchor.
        # On Windows, `abs_root.anchor` evaluates to e.g. `C:\`.
        assert result == Path(abs_root.anchor)

        # relative path with just traversal leads to empty path "."
        result = sanitize_path("foo/../")
        assert result == Path()

    def test_security_sanitizers_handles_invalid_character_parts_standard_expected(
        self,
    ) -> None:
        """Test path with parts that become unnamed due to invalid characters."""
        # `sanitize_filename` of `<>:*?` results in `unnamed`
        result = sanitize_path("foo/<>:*?/bar")
        assert "foo" in result.parts
        assert "unnamed" in result.parts
        assert "bar" in result.parts

    def test_security_sanitizers_resolve_with_base_dir_success_standard_expected(
        self, tmp_path: Path
    ) -> None:
        """Test resolving path with base directory."""
        base = tmp_path / "base"
        base.mkdir()
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        result = sanitize_path(
            subdir.name, base_dir=tmp_path, max_depth=None, resolve=True
        )
        assert isinstance(result, Path)

    def test_security_sanitizers_resolve_with_base_dir_error_standard_expected(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test resolving path with base directory raises ValueError on error."""
        base = tmp_path / "base"
        base.mkdir()

        original_resolve = Path.resolve

        def mock_resolve(self, *args, **kwargs):
            if "subdir" in str(self):
                raise OSError("Mocked error")
            return original_resolve(self, *args, **kwargs)

        monkeypatch.setattr("pathlib.Path.resolve", mock_resolve)
        with pytest.raises(ValueError, match="Cannot resolve path"):
            sanitize_path("subdir", base_dir=base, max_depth=None, resolve=True)


def test_security_sanitizers_sanitize_string_value_error_standard_expected():
    import pytest

    with pytest.raises(TypeError):
        sanitize_string(123)

    with pytest.raises(TypeError):
        sanitize_string("test", max_length="5")

    with pytest.raises(TypeError):
        sanitize_string("test", max_length=True)

    with pytest.raises(TypeError):
        sanitize_string("test", max_length=False)


def test_security_sanitizers_sanitize_filename_value_error_standard_expected():
    import pytest

    with pytest.raises(TypeError):
        sanitize_filename(123)


def test_security_sanitizers_sanitize_filename_no_replacement_standard_expected():
    # test replacement='' to hit the if replacement: branch fallback
    assert sanitize_filename("foo/bar", replacement="") == "bar"


def test_security_sanitizers_sanitizers_re_error_coverage_standard_expected() -> None:
    """Test sanitizers filename validation fallback on re.error."""
    import re

    import taipanstack.security.sanitizers as sanitizers_mod

    original_re = sanitizers_mod._INVALID_FILENAME_CHARS_RE

    class MockRe:
        def __init__(self):
            self.calls = 0

        def sub(self, _repl, string, count: int = 0) -> str:
            if self.calls == 0:
                self.calls += 1
                raise re.error("mock error")
            return original_re.sub("_", string)

    sanitizers_mod._INVALID_FILENAME_CHARS_RE = MockRe()  # type: ignore

    try:
        result = sanitize_filename("test<>txt", replacement=chr(92))
        assert result == "test__txt"
    finally:
        sanitizers_mod._INVALID_FILENAME_CHARS_RE = original_re


def test_security_sanitizers_sanitizers_re_error_coverage_no_slash_standard_expected() -> (
    None
):
    """Test sanitizers filename validation fallback on re.error with normal replacement."""
    import re

    import taipanstack.security.sanitizers as sanitizers_mod

    original_re = sanitizers_mod._INVALID_FILENAME_CHARS_RE

    class MockRe:
        def __init__(self):
            self.calls = 0

        def sub(self, _repl, string, count: int = 0) -> str:
            if self.calls == 0:
                self.calls += 1
                raise re.error("mock error")
            return original_re.sub("_", string)

    sanitizers_mod._INVALID_FILENAME_CHARS_RE = MockRe()  # type: ignore

    try:
        result = sanitize_filename("test<>txt", replacement="!")
        assert result == "test__txt"
    finally:
        sanitizers_mod._INVALID_FILENAME_CHARS_RE = original_re


class TestSanitizerFallthrough:
    """Test fallthrough cases for sanitizers."""

    def test_security_sanitizers_sanitize_path_fallthroughs_standard_expected(
        self,
    ) -> None:
        """Test the implicit fallthrough cases in path sanitization."""
        from pathlib import Path

        from taipanstack.security.sanitizers import sanitize_path

        # Test fallthrough for `if safe_part and safe_part != "..":`
        # By passing a part that becomes empty after sanitization, or is ".."
        # A path like "/some/path/../file" has ".."
        # `_process_path_part` falls through `elif part != ".":` when part is "."
        path = sanitize_path(Path("/some/path/./file"))
        assert str(path).endswith("file")

        # Fallthrough when safe_part is empty
        # sanitize_filename returns "" if the filename is invalid or stripped entirely
        path2 = sanitize_path(Path("/some/path/  /file"))
        assert str(path2).endswith("file")
