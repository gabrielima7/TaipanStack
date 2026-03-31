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

    def test_read_existing_file(self, tmp_path: Path) -> None:
        """Test reading an existing file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello, World!", encoding="utf-8")

        result = safe_read(test_file)
        match result:
            case Ok(content):
                assert content == "Hello, World!"
            case Err():
                pytest.fail("Expected Ok but got Err")

    def test_read_with_base_dir(self, tmp_path: Path) -> None:
        """Test reading with base directory constraint."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content", encoding="utf-8")

        result = safe_read(test_file, base_dir=tmp_path)
        match result:
            case Ok(content):
                assert content == "content"
            case Err():
                pytest.fail("Expected Ok but got Err")

    def test_read_nonexistent_file(self, tmp_path: Path) -> None:
        """Test reading non-existent file returns Err."""
        result = safe_read(tmp_path / "nonexistent.txt")
        match result:
            case Err(FileNotFoundErr(path=p)):
                assert "nonexistent.txt" in str(p)
            case _:
                pytest.fail("Expected Err(FileNotFoundErr)")

    def test_read_directory_fails(self, tmp_path: Path) -> None:
        """Test reading a directory returns Err."""
        result = safe_read(tmp_path)
        match result:
            case Err(NotAFileErr(path=p)):
                assert p == tmp_path
            case _:
                pytest.fail("Expected Err(NotAFileErr)")

    def test_read_file_too_large(self, tmp_path: Path) -> None:
        """Test reading file exceeding max_size returns Err."""
        test_file = tmp_path / "large.txt"
        test_file.write_text("A" * 1000, encoding="utf-8")

        result = safe_read(test_file, max_size_bytes=100)
        match result:
            case Err(FileTooLargeErr(size=s, max_size=m)):
                assert s >= 1000
                assert m == 100
            case _:
                pytest.fail("Expected Err(FileTooLargeErr)")

    def test_read_with_custom_encoding(self, tmp_path: Path) -> None:
        """Test reading with custom encoding."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("ÄÖÅÜ", encoding="utf-8")

        result = safe_read(test_file, encoding="utf-8")
        match result:
            case Ok(content):
                assert content == "ÄÖÅÜ"
            case Err():
                pytest.fail("Expected Ok")

    def test_path_traversal_blocked(self, tmp_path: Path) -> None:
        """Test that path traversal is blocked."""
        result = safe_read(tmp_path / ".." / "etc" / "passwd", base_dir=tmp_path)
        match result:
            case Err(SecurityError()):
                pass  # Expected
            case _:
                pytest.fail("Expected Err(SecurityError)")

    def test_path_traversal_without_base_dir_blocked(self) -> None:
        """Test that path traversal is blocked when no base_dir is provided."""
        result = safe_read("../etc/passwd")
        match result:
            case Err(SecurityError()):
                pass  # Expected
            case _:
                pytest.fail("Expected Err(SecurityError)")


class TestSafeWrite:
    """Tests for safe_write function."""

    def test_write_new_file(self, tmp_path: Path) -> None:
        """Test writing a new file."""
        test_file = tmp_path / "new.txt"
        result = safe_write(test_file, "content")

        assert result.exists()
        assert result.read_text() == "content"

    def test_write_empty_content(self, tmp_path: Path) -> None:
        """Test writing an empty string."""
        test_file = tmp_path / "empty.txt"
        result = safe_write(test_file, "")

        assert result.exists()
        assert result.read_text() == ""

    def test_write_creates_parent_dirs(self, tmp_path: Path) -> None:
        """Test that parent directories are created."""
        test_file = tmp_path / "subdir" / "nested" / "file.txt"
        safe_write(test_file, "nested content")

        assert test_file.exists()

    def test_write_creates_backup(self, tmp_path: Path) -> None:
        """Test that backup is created for existing file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("original")

        safe_write(test_file, "updated", options=WriteOptions(backup=True))

        assert test_file.read_text() == "updated"
        assert (tmp_path / "test.txt.bak").exists()
        assert (tmp_path / "test.txt.bak").read_text() == "original"

    def test_write_no_backup(self, tmp_path: Path) -> None:
        """Test writing without backup."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("original")

        safe_write(test_file, "updated", options=WriteOptions(backup=False))

        assert test_file.read_text() == "updated"
        assert not (tmp_path / "test.txt.bak").exists()

    def test_atomic_write(self, tmp_path: Path) -> None:
        """Test atomic write mode."""
        test_file = tmp_path / "atomic.txt"
        safe_write(test_file, "atomic content", options=WriteOptions(atomic=True))

        assert test_file.read_text() == "atomic content"

    def test_non_atomic_write(self, tmp_path: Path) -> None:
        """Test non-atomic write mode."""
        test_file = tmp_path / "direct.txt"
        safe_write(test_file, "direct content", options=WriteOptions(atomic=False))

        assert test_file.read_text() == "direct content"

    def test_path_traversal_blocked(self, tmp_path: Path) -> None:
        """Test that path traversal is blocked."""
        with pytest.raises(SecurityError):
            safe_write(
                tmp_path / ".." / "etc" / "evil.txt",
                "malicious",
                options=WriteOptions(base_dir=tmp_path),
            )

    def test_path_traversal_without_base_dir_blocked(self) -> None:
        """Test that path traversal is blocked when no base_dir is provided."""
        with pytest.raises(SecurityError):
            safe_write("../etc/evil.txt", "malicious")


class TestEnsureDir:
    """Tests for ensure_dir function."""

    def test_create_new_directory(self, tmp_path: Path) -> None:
        """Test creating a new directory."""
        new_dir = tmp_path / "new_dir"
        result = ensure_dir(new_dir)

        assert result.exists()
        assert result.is_dir()

    def test_existing_directory_ok(self, tmp_path: Path) -> None:
        """Test that existing directory is OK."""
        result = ensure_dir(tmp_path)
        assert result.exists()

    def test_create_nested_directories(self, tmp_path: Path) -> None:
        """Test creating nested directories."""
        nested = tmp_path / "a" / "b" / "c"
        result = ensure_dir(nested)

        assert result.exists()
        assert result.is_dir()

    def test_path_traversal_blocked(self, tmp_path: Path) -> None:
        """Test that path traversal is blocked."""
        with pytest.raises(SecurityError):
            ensure_dir(tmp_path / ".." / "etc" / "evil_dir", base_dir=tmp_path)

    def test_path_traversal_without_base_dir_blocked(self) -> None:
        """Test that path traversal is blocked when no base_dir is provided."""
        with pytest.raises(SecurityError):
            ensure_dir("../etc/evil_dir")


class TestSafeCopy:
    """Tests for safe_copy function."""


class TestSafeDelete:
    """Tests for safe_delete function."""


class TestGetFileHash:
    """Tests for get_file_hash function."""


class TestFindFiles:
    """Tests for find_files function."""
