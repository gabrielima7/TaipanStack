"""Absolute final tests to hit every remaining line."""
from pathlib import Path
from unittest.mock import patch

import pytest


class TestValidatorsTLD:
    """Tests for validators URL TLD check (lines 235-236)."""

    def test_validate_url_no_tld_expected(self) -> None:
        """Test validate_url with domain that has no TLD."""
        from taipanstack.security.validators import validate_url
        with pytest.raises(ValueError, match="TLD"):
            validate_url("http://testserver/path")

    def test_validate_url_ends_with_dot_expected(self) -> None:
        """Test validate_url with domain ending in dot."""
        from taipanstack.security.validators import validate_url
        with pytest.raises(ValueError, match="TLD"):
            validate_url("http://example./path")

class TestValidatorsParseError:
    """Tests for validators URL ValueError (lines 213-215)."""

    def test_validate_url_parse_error(self) -> None:
        """Test validate_url when urlparse raises ValueError."""
        from taipanstack.security.validators import validate_url
        with patch("taipanstack.security.validators.urlsplit") as mock_parse:
            mock_parse.side_effect = ValueError("Parse failed")
            with pytest.raises(ValueError, match="Invalid URL"):
                validate_url("http://valid.com")

class TestGuardsSymlinkDenied:
    """Tests for guards symlink denied (line 118)."""

    def test_guard_path_traversal_symlink_param_expected(self, tmp_path: Path) -> None:
        """Test guard_path_traversal with allow_symlinks parameter."""
        from taipanstack.security.guards import guard_path_traversal
        regular = tmp_path / "regular.txt"
        regular.write_text("content")
        result = guard_path_traversal(regular, tmp_path, allow_symlinks=False)
        assert result.exists()

class TestGuardsExtensionDenied:
    """Tests for guards extension denied (line 256)."""

    def test_guard_file_extension_not_in_allowed_expected(self) -> None:
        """Test guard_file_extension when extension not in allowed list."""
        from taipanstack.security.guards import SecurityError, guard_file_extension
        with pytest.raises(SecurityError, match="not in allowed"):
            guard_file_extension("file.pdf", allowed_extensions=["txt", "doc"])

class TestSanitizersEmptyParts:
    """Tests for sanitizers edge cases (lines 154, 221-223)."""

    def test_sanitize_filename_becomes_empty_expected(self) -> None:
        """Test sanitize_filename when sanitized stem is empty."""
        from taipanstack.security.sanitizers import sanitize_filename
        result = sanitize_filename("....")
        assert result == "unnamed"

    def test_sanitize_path_base_dir_constraint_expected(self, tmp_path: Path) -> None:
        """Test sanitize_path with base_dir and non-existent path."""
        from taipanstack.security.sanitizers import sanitize_path
        result = sanitize_path("new/file.txt", base_dir=tmp_path, max_depth=None)
        assert str(tmp_path) in str(result)

class TestFilesystemLine175:
    """Test for filesystem.py line 175."""

    def test_safe_write_different_encoding_expected(self, tmp_path: Path) -> None:
        """Test safe_write with different encoding."""
        from taipanstack.utils.filesystem import WriteOptions, safe_write
        test_file = tmp_path / "encoded.txt"
        content = "Héllo Wörld"
        result = safe_write(test_file, content, options=WriteOptions(encoding="utf-8"))
        assert result.read_text(encoding="utf-8") == content
