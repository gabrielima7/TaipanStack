"""Tests for safe filesystem operations."""

from pathlib import Path

import pytest

from taipanstack.core.result import Err, Ok
from taipanstack.security.guards import SecurityError
from taipanstack.utils.filesystem import (
    FileNotFoundErr,
    FileTooLargeErr,
    NotAFileErr,
    WriteOptions,
    ensure_dir,
    safe_read,
    safe_write,
)


class TestSafeRead:
    """Tests for safe_read function."""

    def test_utils_filesystem_read_no_max_size_expected(self, tmp_path: Path) -> None:
        """Test reading a file with max_size_bytes=None."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("hello")

        result = safe_read(test_file, max_size_bytes=None)
        assert result.ok_value == "hello"

    def test_utils_filesystem_read_existing_file_expected(self, tmp_path: Path) -> None:
        """Test reading an existing file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello, World!", encoding="utf-8")

        result = safe_read(test_file)
        match result:
            case Ok(content):
                assert content == "Hello, World!"
            case Err():
                pytest.fail("Expected Ok but got Err")

    def test_utils_filesystem_read_with_base_dir_expected(self, tmp_path: Path) -> None:
        """Test reading with base directory constraint."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content", encoding="utf-8")

        result = safe_read(test_file, base_dir=tmp_path)
        match result:
            case Ok(content):
                assert content == "content"
            case Err():
                pytest.fail("Expected Ok but got Err")

    def test_utils_filesystem_read_nonexistent_file_expected(
        self, tmp_path: Path
    ) -> None:
        """Test reading non-existent file returns Err."""
        result = safe_read(tmp_path / "nonexistent.txt")
        match result:
            case Err(FileNotFoundErr(path=p) as e):
                assert "nonexistent.txt" in str(p)
                assert e.message == f"File not found: {p}"
            case _:
                pytest.fail("Expected Err(FileNotFoundErr)")

    def test_utils_filesystem_read_directory_fails(self, tmp_path: Path) -> None:
        """Test reading a directory returns Err."""
        result = safe_read(tmp_path)
        match result:
            case Err(NotAFileErr(path=p) as e):
                assert p == tmp_path
                assert e.message == f"Not a file: {p}"
            case _:
                pytest.fail("Expected Err(NotAFileErr)")

    def test_utils_filesystem_read_file_too_large_expected(
        self, tmp_path: Path
    ) -> None:
        """Test reading file exceeding max_size returns Err."""
        test_file = tmp_path / "large.txt"
        test_file.write_text("A" * 1000, encoding="utf-8")

        result = safe_read(test_file, max_size_bytes=100)
        match result:
            case Err(FileTooLargeErr(size=s, max_size=m) as e):
                assert s >= 1000
                assert m == 100
                assert e.message == f"File too large: {s} bytes (max: {m})"
            case _:
                pytest.fail("Expected Err(FileTooLargeErr)")

    def test_utils_filesystem_read_with_custom_encoding_expected(
        self, tmp_path: Path
    ) -> None:
        """Test reading with custom encoding."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("ÄÖÅÜ", encoding="utf-8")

        result = safe_read(test_file, encoding="utf-8")
        match result:
            case Ok(content):
                assert content == "ÄÖÅÜ"
            case Err():
                pytest.fail("Expected Ok")

    def test_utils_filesystem_path_traversal_blocked(self, tmp_path: Path) -> None:
        """Test that path traversal is blocked."""
        result = safe_read(tmp_path / ".." / "etc" / "passwd", base_dir=tmp_path)
        match result:
            case Err(SecurityError()):
                assert True
            case _:
                pytest.fail("Expected Err(SecurityError)")

    def test_utils_filesystem_path_traversal_without_base_dir_blocked(
        self,
    ) -> None:
        """Test that path traversal is blocked when no base_dir is provided."""
        result = safe_read("../etc/passwd")
        match result:
            case Err(SecurityError()):
                assert True
            case _:
                pytest.fail("Expected Err(SecurityError)")


class TestSafeWrite:
    """Tests for safe_write function."""

    def test_utils_filesystem_write_new_file_expected(self, tmp_path: Path) -> None:
        """Test writing a new file."""
        test_file = tmp_path / "new.txt"
        result = safe_write(test_file, "content")

        assert result.exists()
        assert result.read_text() == "content"

    def test_utils_filesystem_write_existing_file_with_base_dir_expected(
        self, tmp_path: Path
    ) -> None:
        """Test writing an existing file with base_dir."""
        test_file = tmp_path / "existing.txt"
        test_file.write_text("old")

        result = safe_write(test_file, "new", options=WriteOptions(base_dir=tmp_path))

        assert result.exists()
        assert result.read_text() == "new"

    def test_utils_filesystem_write_no_create_parents_expected(
        self, tmp_path: Path
    ) -> None:
        """Test writing a file with create_parents=False."""
        test_file = tmp_path / "direct.txt"
        result = safe_write(
            test_file, "content", options=WriteOptions(create_parents=False)
        )

        assert result.exists()
        assert result.read_text() == "content"

    def test_utils_filesystem_write_empty_content_expected(
        self, tmp_path: Path
    ) -> None:
        """Test writing an empty string."""
        test_file = tmp_path / "empty.txt"
        result = safe_write(test_file, "")

        assert result.exists()
        assert result.read_text() == ""

    def test_utils_filesystem_write_creates_parent_dirs_expected(
        self, tmp_path: Path
    ) -> None:
        """Test that parent directories are created."""
        test_file = tmp_path / "subdir" / "nested" / "file.txt"
        safe_write(test_file, "nested content")

        assert test_file.exists()

    def test_utils_filesystem_write_creates_backup_expected(
        self, tmp_path: Path
    ) -> None:
        """Test that backup is created for existing file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("original")

        safe_write(test_file, "updated", options=WriteOptions(backup=True))

        assert test_file.read_text() == "updated"
        assert (tmp_path / "test.txt.bak").exists()
        assert (tmp_path / "test.txt.bak").read_text() == "original"

    def test_utils_filesystem_write_no_backup_expected(self, tmp_path: Path) -> None:
        """Test writing without backup."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("original")

        safe_write(test_file, "updated", options=WriteOptions(backup=False))

        assert test_file.read_text() == "updated"
        assert not (tmp_path / "test.txt.bak").exists()

    def test_utils_filesystem_atomic_write_expected(self, tmp_path: Path) -> None:
        """Test atomic write mode."""
        test_file = tmp_path / "atomic.txt"
        safe_write(test_file, "atomic content", options=WriteOptions(atomic=True))

        assert test_file.read_text() == "atomic content"

    def test_utils_filesystem_non_atomic_write_expected(self, tmp_path: Path) -> None:
        """Test non-atomic write mode."""
        test_file = tmp_path / "direct.txt"
        safe_write(test_file, "direct content", options=WriteOptions(atomic=False))

        assert test_file.read_text() == "direct content"

    def test_utils_filesystem_safe_write_cleanup_propagates_oserror(
        self, tmp_path: Path
    ) -> None:
        """Test that cleanup during write propagates critical OSErrors like PermissionError."""
        test_file = tmp_path / "protected.txt"

        from unittest.mock import patch

        # Trigger an exception to enter the `except Exception:` cleanup block
        with patch("pathlib.Path.rename", side_effect=ValueError("Rename failed")):
            # When the cleanup attempts to unlink the temp file, raise PermissionError
            with patch(
                "pathlib.Path.unlink", side_effect=PermissionError("Permission denied")
            ):
                with pytest.raises(PermissionError, match="Permission denied"):
                    safe_write(test_file, "content", options=WriteOptions(atomic=True))

    def test_utils_filesystem_safe_write_cleanup_succeeds_expected(
        self, tmp_path: Path
    ) -> None:
        """Test that cleanup during write unlinks the temp file."""
        test_file = tmp_path / "cleanup.txt"

        from unittest.mock import patch

        # Trigger an exception to enter the `except Exception:` cleanup block
        with patch("pathlib.Path.rename", side_effect=ValueError("Rename failed")):
            with pytest.raises(ValueError, match="Rename failed"):
                safe_write(test_file, "content", options=WriteOptions(atomic=True))

    def test_utils_filesystem_path_traversal_blocked(self, tmp_path: Path) -> None:
        """Test that path traversal is blocked."""
        with pytest.raises(SecurityError):
            safe_write(
                tmp_path / ".." / "etc" / "evil.txt",
                "malicious",
                options=WriteOptions(base_dir=tmp_path),
            )

    def test_utils_filesystem_path_traversal_without_base_dir_blocked(
        self,
    ) -> None:
        """Test that path traversal is blocked when no base_dir is provided."""
        with pytest.raises(SecurityError):
            safe_write("../etc/evil.txt", "malicious")

    def test_utils_filesystem_write_invalid_filename_blocked(
        self, tmp_path: Path
    ) -> None:
        """Test that writing to an invalid filename raises an error instead of silently mutating."""
        test_file = tmp_path / "report:2023.txt"
        with pytest.raises(
            SecurityError, match="Unsafe or invalid characters in filename"
        ):
            safe_write(test_file, "content")


class TestEnsureDir:
    """Tests for ensure_dir function."""

    def test_utils_filesystem_create_new_directory_expected(
        self, tmp_path: Path
    ) -> None:
        """Test creating a new directory."""
        new_dir = tmp_path / "new_dir"
        result = ensure_dir(new_dir)

        assert result.exists()
        assert result.is_dir()

    def test_utils_filesystem_existing_directory_ok(self, tmp_path: Path) -> None:
        """Test that existing directory is OK."""
        result = ensure_dir(tmp_path)
        assert result.exists()

    def test_utils_filesystem_create_nested_directories_expected(
        self, tmp_path: Path
    ) -> None:
        """Test creating nested directories."""
        nested = tmp_path / "a" / "b" / "c"
        result = ensure_dir(nested)

        assert result.exists()
        assert result.is_dir()

    def test_utils_filesystem_path_traversal_blocked(self, tmp_path: Path) -> None:
        """Test that path traversal is blocked."""
        with pytest.raises(SecurityError):
            ensure_dir(tmp_path / ".." / "etc" / "evil_dir", base_dir=tmp_path)

    def test_utils_filesystem_path_traversal_without_base_dir_blocked(
        self,
    ) -> None:
        """Test that path traversal is blocked when no base_dir is provided."""
        with pytest.raises(SecurityError):
            ensure_dir("../etc/evil_dir")

    def test_utils_filesystem_file_exists_error_when_path_is_file_expected(
        self, tmp_path: Path
    ) -> None:
        """Test that FileExistsError is raised if intermediate path is a file."""
        conflict_file = tmp_path / "conflict"
        conflict_file.write_text("content")

        with pytest.raises(FileExistsError, match="Path exists but is not a directory"):
            ensure_dir(conflict_file / "nested_dir")

        with pytest.raises(FileExistsError, match="Path exists but is not a directory"):
            ensure_dir(conflict_file)

    def test_utils_filesystem_root_directory_already_exists_expected(self) -> None:
        """Test ensuring the root directory to cover the root parent check."""
        import sys

        # Determine the root directory based on the platform
        root = Path("C:\\") if sys.platform == "win32" else Path("/")

        # Ensure dir on the root should not loop indefinitely and should return the root
        result = ensure_dir(root)
        assert result == root

    def test_utils_filesystem_missing_intermediate_directory_created(
        self, tmp_path: Path
    ) -> None:
        """Test creating a directory with a missing intermediate parent."""
        target = tmp_path / "missing" / "leaf"
        result = ensure_dir(target)

        assert result.exists()
        assert result.is_dir()
        assert (tmp_path / "missing").is_dir()

    def test_utils_filesystem_root_parent_loop_break_expected(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test the break condition when looping up to root."""
        import sys

        root = Path("C:\\") if sys.platform == "win32" else Path("/")

        # We need to simulate that the root is NOT a dir to enter the loop,
        # but it doesn't exist either so we don't hit the FileExistsError.
        original_is_dir = Path.is_dir
        original_exists = Path.exists

        def mock_is_dir(self: Path) -> bool:
            if self == root:
                return False
            return original_is_dir(self)

        def mock_exists(self: Path) -> bool:
            if self == root:
                return False
            return original_exists(self)

        monkeypatch.setattr(Path, "is_dir", mock_is_dir)
        monkeypatch.setattr(Path, "exists", mock_exists)

        # Mock mkdir to avoid PermissionError trying to mkdir on root
        def mock_mkdir(*args, **kwargs) -> None:
            return None

        monkeypatch.setattr(Path, "mkdir", mock_mkdir)

        ensure_dir(root)
