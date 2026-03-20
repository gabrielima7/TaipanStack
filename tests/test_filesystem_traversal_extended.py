"""Extended tests for path traversal in filesystem utilities."""

from pathlib import Path

import pytest

from taipanstack.core.result import Err
from taipanstack.security.guards import SecurityError
from taipanstack.utils.filesystem import (
    ensure_dir,
    find_files,
    get_file_hash,
    safe_copy,
    safe_delete,
    safe_read,
    safe_write,
)


class TestFilesystemTraversalExtended:
    """Tests for various traversal patterns and edge cases."""

    @pytest.mark.parametrize("pattern", ["%2e%2e", "%252e%252e", "~"])
    def test_ensure_dir_traversal_patterns(self, tmp_path: Path, pattern: str):
        """Test that ensure_dir blocks various traversal patterns."""
        with pytest.raises(SecurityError) as exc_info:
            ensure_dir(f"{pattern}/evil_dir")
        assert "path_traversal" in str(exc_info.value).lower()

    def test_ensure_dir_absolute_path_not_blocked_by_default(self, tmp_path: Path):
        """Test that ensure_dir allows absolute paths when no base_dir is provided.

        This is required for backward compatibility and internal usage.
        """
        target = tmp_path / "abs_dir"
        result = ensure_dir(str(target.absolute()))
        assert result.exists()
        assert result.is_absolute()

    @pytest.mark.parametrize("pattern", ["%2e%2e", "%252e%252e"])
    def test_safe_read_encoded_traversal(self, tmp_path: Path, pattern: str):
        """Test that safe_read blocks encoded traversal patterns."""
        result = safe_read(f"{pattern}/etc/passwd")
        assert isinstance(result, Err)
        assert isinstance(result.err_value, SecurityError)

    def test_safe_write_encoded_traversal(self, tmp_path: Path):
        """Test that safe_write blocks encoded traversal patterns."""
        with pytest.raises(SecurityError):
            safe_write("%2e%2e/evil.txt", "content")

    def test_safe_delete_encoded_traversal(self, tmp_path: Path):
        """Test that safe_delete blocks encoded traversal patterns."""
        with pytest.raises(SecurityError):
            safe_delete("%2e%2e/evil.txt")

    def test_get_file_hash_encoded_traversal(self, tmp_path: Path):
        """Test that get_file_hash blocks encoded traversal patterns."""
        with pytest.raises(SecurityError):
            get_file_hash("%2e%2e/etc/passwd")

    def test_find_files_encoded_traversal(self, tmp_path: Path):
        """Test that find_files blocks encoded traversal patterns."""
        with pytest.raises(SecurityError):
            find_files("%2e%2e/etc")

    def test_safe_copy_encoded_traversal(self, tmp_path: Path):
        """Test that safe_copy blocks encoded traversal patterns."""
        # Source traversal
        with pytest.raises(SecurityError):
            safe_copy("%2e%2e/etc/passwd", "local.txt")

        # Destination traversal
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        with pytest.raises(SecurityError):
            safe_copy(test_file, "%2e%2e/evil.txt")

    def test_ensure_dir_with_explicit_base_dir_encoded(self, tmp_path: Path):
        """Test ensure_dir with base_dir and encoded traversal."""
        with pytest.raises(SecurityError):
            ensure_dir("%2e%2e/evil", base_dir=tmp_path)

    def test_tilde_in_middle_not_blocked(self, tmp_path: Path):
        """Test that tilde in the middle of a component (like Windows short paths) is not blocked."""
        # This simulates a Windows short path like RUNNER~1
        path = tmp_path / "RUNNER~1"
        result = ensure_dir(path)
        assert result.exists()
        assert "RUNNER~1" in str(result)
