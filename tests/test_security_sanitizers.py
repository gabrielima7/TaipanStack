"""Tests for input sanitizers."""

from pathlib import Path

import pytest

from taipanstack.security.sanitizers import (
    sanitize_env_value,
    sanitize_filename,
    sanitize_path,
    sanitize_sql_identifier,
    sanitize_string,
)


class TestSanitizeString:
    """Tests for sanitize_string function."""

    def test_empty_string(self) -> None:
        """Test empty string returns empty."""
        assert sanitize_string("") == ""

    def test_normal_string_unchanged(self) -> None:
        """Test normal string passes through."""
        assert sanitize_string("Hello World") == "Hello World"

    def test_strips_whitespace(self) -> None:
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
    def test_strips_various_whitespace(self, whitespace: str) -> None:
        """Test various whitespace characters are stripped correctly."""
        # Test leading/trailing whitespace
        assert sanitize_string(f"{whitespace}hello{whitespace}") == "hello"
        # Test string with only whitespace (should become empty)
        assert sanitize_string(whitespace) == ""

    def test_no_strip_whitespace(self) -> None:
        """Test whitespace preserved when disabled."""
        result = sanitize_string("  hello  ", strip_whitespace=False)
        assert result == "  hello  "

    def test_removes_null_bytes(self) -> None:
        """Test null bytes are removed."""
        assert sanitize_string("hel\x00lo") == "hello"

    def test_removes_html_tags(self) -> None:
        """Test HTML tags are removed by default."""
        result = sanitize_string("<script>alert('xss')</script>")
        assert "<script>" not in result
        assert "alert" in result  # Text content preserved

    def test_allows_html_when_enabled(self) -> None:
        """Test HTML tags preserved when allowed."""
        result = sanitize_string("<b>bold</b>", allow_html=True)
        assert "<b>" in result

    def test_removes_control_characters(self) -> None:
        """Test control characters are removed."""
        result = sanitize_string("hello\x01\x02world")
        assert result == "helloworld"

    def test_preserves_newlines(self) -> None:
        """Test newlines are preserved."""
        result = sanitize_string("line1\nline2")
        assert "\n" in result

    def test_removes_unicode_when_disabled(self) -> None:
        """Test unicode removed when not allowed."""
        result = sanitize_string("héllo wörld", allow_unicode=False)
        assert "é" not in result
        assert "ö" not in result

    def test_truncates_to_max_length(self) -> None:
        """Test string is truncated."""
        result = sanitize_string("hello world", max_length=5)
        assert result == "hello"
        assert len(result) == 5

    def test_escapes_html_entities(self) -> None:
        """Test HTML entities are escaped after tag removal."""
        # Note: < and > inside text (not as tags) get escaped after tag stripping
        result = sanitize_string("text&more")
        assert "&amp;" in result


class TestSanitizeFilename:
    """Tests for sanitize_filename function."""

    def test_empty_filename(self) -> None:
        """Test empty filename returns 'unnamed'."""
        assert sanitize_filename("") == "unnamed"

    def test_normal_filename(self) -> None:
        """Test normal filename passes through."""
        assert sanitize_filename("test.txt") == "test.txt"

    def test_removes_path_characters(self) -> None:
        """Test path characters are removed."""
        result = sanitize_filename("../etc/passwd.txt")
        assert "/" not in result
        assert ".." not in result

    def test_removes_invalid_windows_chars(self) -> None:
        """Test Windows invalid chars are removed."""
        result = sanitize_filename("file<>:name.txt")
        assert "<" not in result
        assert ">" not in result
        assert ":" not in result

    def test_preserves_extension(self) -> None:
        """Test extension is preserved by default."""
        result = sanitize_filename("bad<file>name.txt")
        assert result.endswith(".txt")

    def test_no_preserve_extension(self) -> None:
        """Test extension not preserved when disabled."""
        result = sanitize_filename("test.txt", preserve_extension=False)
        assert result == "test"

    def test_handles_reserved_names(self) -> None:
        """Test Windows reserved names are handled."""
        result = sanitize_filename("CON")
        assert result != "CON"
        assert result.upper() != "CON"

    def test_max_length_with_extension(self) -> None:
        """Test max length preserves extension."""
        result = sanitize_filename("verylongfilename.txt", max_length=10)
        assert len(result) <= 10
        assert result.endswith(".txt")

    def test_max_length_with_long_extension(self) -> None:
        """Test max length when extension is longer than max_length."""
        # Extension is ".extension" (10 chars), max_length is 5
        result = sanitize_filename("file.extension", max_length=5)
        assert len(result) == 5
        assert result == "file."

    def test_custom_replacement(self) -> None:
        """Test custom replacement character."""
        result = sanitize_filename("bad:name.txt", replacement="-")
        assert ":" not in result
        assert "-" in result

    def test_collapses_multiple_replacements(self) -> None:
        """Test multiple invalid chars become single replacement."""
        result = sanitize_filename("a:::b.txt")
        assert "___" not in result  # Collapsed to single _


class TestSanitizePath:
    """Tests for sanitize_path function."""

    def test_sanitize_path_absolute_with_base_dir(self, tmp_path: Path) -> None:
        """Test sanitize_path when sanitized is absolute and base_dir is given."""
        # When `sanitized.is_absolute()` is True, `_apply_base_dir_constraint` returns `sanitized`
        # if `base_dir` is not None and resolve is False.
        path = tmp_path / "absolute/path"

        base_dir = tmp_path / "base"
        base_dir.mkdir()

        result = sanitize_path(path, base_dir=base_dir, resolve=False)
        assert result.is_absolute()
        assert result.parts[-2:] == ("absolute", "path")

    def test_sanitize_path_absolute_with_parts(self, tmp_path: Path) -> None:
        """Test sanitize_path when path is absolute and has parts."""
        # Covers path reconstruction when path.is_absolute() is True and parts is truthy
        path = tmp_path / "absolute/path"
        result = sanitize_path(path)
        assert result.is_absolute()
        assert result.parts[-2:] == ("absolute", "path")

    def test_sanitize_path_empty(self) -> None:
        """Test sanitize_path when path is empty (no parts, not absolute)."""
        # This covers the line:
        # else:
        #     sanitized = Path()
        result = sanitize_path("")
        assert not result.is_absolute()
        assert result == Path()

    def test_simple_path(self) -> None:
        """Test simple path passes through."""
        result = sanitize_path("test/file.txt")
        assert "test" in str(result)
        assert "file.txt" in str(result)

    def test_removes_traversal(self) -> None:
        """Test path traversal is removed."""
        result = sanitize_path("../etc/passwd")
        assert ".." not in str(result)

    def test_removes_null_bytes(self) -> None:
        """Test null bytes in path are removed."""
        result = sanitize_path("test\x00file.txt")
        assert "\x00" not in str(result)

    def test_max_depth_enforced(self) -> None:
        """Test max depth is enforced."""
        deep_path = "/".join(["dir"] * 20)
        with pytest.raises(ValueError, match="depth"):
            sanitize_path(deep_path, max_depth=5)

    def test_with_base_dir(self, tmp_path: Path) -> None:
        """Test path with base directory."""
        base = tmp_path / "base"
        base.mkdir()
        # max_depth=None to avoid depth check (CI paths can be very long)
        result = sanitize_path("subdir/file.txt", base_dir=base, max_depth=None)
        # Check result is under base directory using Path comparison
        assert str(base) in str(result)

    def test_removes_parent_traversal(self) -> None:
        """Test path traversal with parent directory is resolved."""
        result = sanitize_path("foo/../bar")
        assert "bar" in str(result)
        assert "foo" not in str(result)

    def test_removes_multiple_parent_traversals(self) -> None:
        """Test path traversal with multiple parent directories."""
        result = sanitize_path("foo/bar/../../baz")
        assert "baz" in str(result)
        assert "foo" not in str(result)
        assert "bar" not in str(result)

    def test_handles_empty_parts(self) -> None:
        """Test path with empty parts after sanitization."""
        # To trigger an absolute path traversal resulting in empty parts cross-platform,
        # we resolve the root path (so it gets C:/ on Windows) and append ..
        abs_root = Path("/").resolve()
        abs_traversal = abs_root / ".."
        result = sanitize_path(abs_traversal)

        # When `sanitize_path` reconstructs an absolute path that's empty, it hardcodes `Path("/")`.
        # On Windows, `Path("/")` evaluates to `\` without a drive letter.
        assert result == Path("/")

        # relative path with just traversal leads to empty path "."
        result = sanitize_path("foo/../")
        assert result == Path()

    def test_handles_invalid_character_parts(self) -> None:
        """Test path with parts that become unnamed due to invalid characters."""
        # `sanitize_filename` of `<>:*?` results in `unnamed`
        result = sanitize_path("foo/<>:*?/bar")
        assert "foo" in result.parts
        assert "unnamed" in result.parts
        assert "bar" in result.parts

    def test_resolve_with_base_dir_success(self, tmp_path: Path) -> None:
        """Test resolving path with base directory."""
        base = tmp_path / "base"
        base.mkdir()
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        result = sanitize_path(
            subdir.name, base_dir=tmp_path, max_depth=None, resolve=True
        )
        assert isinstance(result, Path)

    def test_resolve_with_base_dir_error(
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


class TestSanitizeEnvValue:
    """Tests for sanitize_env_value function."""

    def test_type_error(self) -> None:
        """Test non-string value raises TypeError."""
        with pytest.raises(TypeError, match="value must be str, got int"):
            sanitize_env_value(123)  # type: ignore[arg-type]

    def test_empty_value(self) -> None:
        """Test empty value returns empty."""
        assert sanitize_env_value("") == ""

    def test_normal_value(self) -> None:
        """Test normal value passes through."""
        assert sanitize_env_value("hello") == "hello"

    def test_removes_null_bytes(self) -> None:
        """Test null bytes are removed."""
        assert sanitize_env_value("hel\x00lo") == "hello"

    def test_removes_newlines_by_default(self) -> None:
        """Test newlines are replaced by default."""
        result = sanitize_env_value("line1\nline2")
        assert "\n" not in result

    def test_allows_multiline(self) -> None:
        """Test newlines preserved when allowed."""
        result = sanitize_env_value("line1\nline2", allow_multiline=True)
        assert "\n" in result

    def test_truncates_to_max_length(self) -> None:
        """Test truncation to max length."""
        long_value = "a" * 5000
        result = sanitize_env_value(long_value, max_length=100)
        assert len(result) == 100

    def test_sanitize_env_value_fast_path(self) -> None:
        """Test sanitize_env_value fast path for coverage."""
        # Triggers the fast path return
        assert sanitize_env_value("hello", max_length=10) == "hello"
        assert (
            sanitize_env_value("line1\nline2", allow_multiline=True) == "line1\nline2"
        )

    def test_sanitize_env_value_slow_path(self) -> None:
        """Test sanitize_env_value slow path for coverage."""
        # 1. Triggers "\x00" not in value == False
        assert sanitize_env_value("hel\x00lo", max_length=10) == "hello"
        # 2. Triggers ("\n" not in value and "\r" not in value) == False
        assert (
            sanitize_env_value("line1\nline2", max_length=20, allow_multiline=False)
            == "line1 line2"
        )
        # 3. Triggers len(value) <= max_length == False
        assert sanitize_env_value("a" * 15, max_length=10) == "a" * 10
        # 4. Triggers allow_multiline=True with slow path (due to length)
        assert (
            sanitize_env_value("line1\nline2", max_length=5, allow_multiline=True)
            == "line1"
        )


class TestSanitizeSqlIdentifier:
    """Tests for sanitize_sql_identifier function."""

    def test_type_error(self) -> None:
        """Test non-string identifier raises TypeError."""
        with pytest.raises(TypeError, match="identifier must be str, got float"):
            sanitize_sql_identifier(3.14)  # type: ignore[arg-type]

    def test_empty_identifier_raises(self) -> None:
        """Test empty identifier raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            sanitize_sql_identifier("")

    def test_normal_identifier(self) -> None:
        """Test normal identifier passes through."""
        assert sanitize_sql_identifier("users") == "users"

    def test_removes_special_characters(self) -> None:
        """Test special characters are removed."""
        result = sanitize_sql_identifier("users;DROP TABLE--")
        assert ";" not in result
        assert "-" not in result
        assert "DROP" in result  # Letters preserved

    def test_prefix_if_starts_with_number(self) -> None:
        """Test underscore added if starts with number."""
        result = sanitize_sql_identifier("123column")
        assert result.startswith("_")

    def test_only_numbers(self) -> None:
        """Test identifier with only numbers adds underscore prefix."""
        result = sanitize_sql_identifier("12345")
        assert result == "_12345"

    def test_truncates_long_identifier(self) -> None:
        """Test long identifier is truncated."""
        long_name = "a" * 200
        result = sanitize_sql_identifier(long_name)
        assert len(result) <= 128

    def test_invalid_chars_only_raises(self) -> None:
        """Test identifier with only invalid chars raises."""
        with pytest.raises(ValueError, match="no valid characters"):
            sanitize_sql_identifier(";--")

    def test_allows_underscores(self) -> None:
        """Test underscores are allowed."""
        result = sanitize_sql_identifier("user_name")
        assert result == "user_name"


def test_sanitize_string_value_error():
    import pytest

    with pytest.raises(TypeError):
        sanitize_string(123)


def test_sanitize_filename_value_error():
    import pytest

    with pytest.raises(TypeError):
        sanitize_filename(123)


def test_sanitize_filename_no_replacement():
    # test replacement='' to hit the if replacement: branch fallback
    assert sanitize_filename("foo/bar", replacement="") == "bar"
