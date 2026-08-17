"""Extended tests for path traversal in filesystem utilities."""

from pathlib import Path

import pytest

from taipanstack.core.result import Err
from taipanstack.security.guards import SecurityError
from taipanstack.utils.filesystem import (
    ensure_dir,
    safe_read,
    safe_write,
)


class TestFilesystemTraversalExtended:
    """Tests for various traversal patterns and edge cases."""

    @pytest.mark.parametrize("pattern", ["%2e%2e", "%252e%252e", "~"])
    def test_filesystem_traversal_extended_ensure_dir_traversal_patterns_expected(
        self, tmp_path: Path, pattern: str
    ):
        """Test that ensure_dir blocks various traversal patterns."""
        with pytest.raises(SecurityError) as exc_info:
            ensure_dir(f"{pattern}/evil_dir")
        assert "path_traversal" in str(exc_info.value).lower()

    def test_filesystem_traversal_extended_ensure_dir_absolute_path_not_blocked_by_default_expected(
        self, tmp_path: Path
    ):
        """Test that ensure_dir allows absolute paths when no base_dir is provided.

        This is required for backward compatibility and internal usage.
        """
        target = tmp_path / "abs_dir"
        result = ensure_dir(str(target.absolute()))
        assert result.exists()
        assert result.is_absolute()

    @pytest.mark.parametrize("pattern", ["%2e%2e", "%252e%252e"])
    def test_filesystem_traversal_extended_safe_read_encoded_traversal_expected(
        self, tmp_path: Path, pattern: str
    ):
        """Test that safe_read blocks encoded traversal patterns."""
        result = safe_read(f"{pattern}/etc/passwd")
        assert isinstance(result, Err)
        assert isinstance(result.err_value, SecurityError)

    def test_filesystem_traversal_extended_safe_write_encoded_traversal_expected(
        self, tmp_path: Path
    ):
        """Test that safe_write blocks encoded traversal patterns."""
        with pytest.raises(SecurityError):
            safe_write("%2e%2e/evil.txt", "content")

    def test_filesystem_traversal_extended_ensure_dir_with_explicit_base_dir_encoded_expected(
        self, tmp_path: Path
    ):
        """Test ensure_dir with base_dir and encoded traversal."""
        with pytest.raises(SecurityError):
            ensure_dir("%2e%2e/evil", base_dir=tmp_path)

    def test_filesystem_traversal_extended_tilde_in_middle_not_blocked_expected(
        self, tmp_path: Path
    ):
        """Test that tilde in the middle of a component (like Windows short paths) is not blocked."""
        # This simulates a Windows short path like RUNNER~1
        path = tmp_path / "RUNNER~1"
        result = ensure_dir(path)
        assert result.exists()
        assert "RUNNER~1" in str(result)
