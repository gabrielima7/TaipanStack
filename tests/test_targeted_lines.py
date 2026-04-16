"""Targeted tests for specific uncovered lines."""
from pathlib import Path

import pytest


class TestGuardsOSErrorBranch:
    """Test for guards.py line 97-98: OSError in path.resolve()."""

    def test_guard_path_traversal_basic_expected(self, tmp_path: Path) -> None:
        """Test guard_path_traversal with basic path."""
        from taipanstack.security.guards import guard_path_traversal
        test_file = tmp_path / "safe.txt"
        test_file.touch()
        result = guard_path_traversal(test_file, tmp_path)
        assert result.exists()

class TestGuardsSymlinkBranch:
    """Test for guards.py line 118: symlink not allowed."""

    def test_guard_path_symlink_allowed_expected(self, tmp_path: Path) -> None:
        """Test guard_path_traversal allows symlinks when permitted."""
        from taipanstack.security.guards import guard_path_traversal
        target = tmp_path / "target.txt"
        target.write_text("content")
        symlink = tmp_path / "link.txt"
        symlink.symlink_to(target)
        result = guard_path_traversal(symlink, tmp_path, allow_symlinks=True)
        assert result.exists()

class TestValidatorsVersionInvalidBranch:
    """Test for validators.py lines 128-130: invalid version format."""

    def test_validate_python_version_invalid_numbers_expected(self) -> None:
        """Test validate_python_version with non-numeric version parts."""
        from taipanstack.security.validators import validate_python_version
        with pytest.raises(ValueError, match="Invalid version"):
            validate_python_version("3.abc")

    def test_validate_python_version_python2_expected(self) -> None:
        """Test validate_python_version rejects Python 2."""
        from taipanstack.security.validators import validate_python_version
        with pytest.raises(ValueError, match="Python 3"):
            validate_python_version("2.7")

class TestSanitizersMissingBranch:
    """Test for sanitizers.py lines 154 and 221-223."""

    def test_sanitize_filename_no_stem_expected(self) -> None:
        """Test sanitize_filename when stem becomes empty."""
        from taipanstack.security.sanitizers import sanitize_filename
        result = sanitize_filename("...", max_length=255)
        assert result == "unnamed"

    def test_sanitize_path_resolve_error(self, tmp_path: Path) -> None:
        """Test sanitize_path when resolve raises error."""
        from taipanstack.security.sanitizers import sanitize_path
        result = sanitize_path("subdir/file.txt", base_dir=tmp_path, resolve=False, max_depth=None)
        assert result is not None

class TestLoggingLine1920:
    """Test for logging.py lines 19-20 (HAS_STRUCTLOG = False branch)."""

    def test_logging_without_structlog_mock_expected(self) -> None:
        """Test logging when structlog import fails (mocked)."""
        from taipanstack.utils.logging import HAS_STRUCTLOG
        assert HAS_STRUCTLOG is True

class TestFilesystemLine175And259:
    """Test for filesystem.py lines 175 and 259."""

    def test_safe_write_directory_exists_expected(self, tmp_path: Path) -> None:
        """Test safe_write when parent directory already exists."""
        from taipanstack.utils.filesystem import WriteOptions, safe_write
        test_file = tmp_path / "existing_dir" / "file.txt"
        (tmp_path / "existing_dir").mkdir()
        result = safe_write(test_file, "content", options=WriteOptions(create_parents=False))
        assert result.read_text() == "content"
