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
    find_files,
    get_file_hash,
    safe_copy,
    safe_delete,
    safe_read,
    safe_write,
)


class TestSafeRead:
    """Tests for safe_read function."""

    def test_read_no_max_size(self, tmp_path: Path) -> None:
        """Test reading a file with max_size_bytes=None."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("hello")

        result = safe_read(test_file, max_size_bytes=None)
        assert result.ok_value == "hello"

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
            case Err(FileNotFoundErr(path=p) as e):
                assert "nonexistent.txt" in str(p)
                assert e.message == f"File not found: {p}"
            case _:
                pytest.fail("Expected Err(FileNotFoundErr)")

    def test_read_directory_fails(self, tmp_path: Path) -> None:
        """Test reading a directory returns Err."""
        result = safe_read(tmp_path)
        match result:
            case Err(NotAFileErr(path=p) as e):
                assert p == tmp_path
                assert e.message == f"Not a file: {p}"
            case _:
                pytest.fail("Expected Err(NotAFileErr)")

    def test_read_file_too_large(self, tmp_path: Path) -> None:
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

    def test_write_existing_file_with_base_dir(self, tmp_path: Path) -> None:
        """Test writing an existing file with base_dir."""
        test_file = tmp_path / "existing.txt"
        test_file.write_text("old")

        result = safe_write(test_file, "new", options=WriteOptions(base_dir=tmp_path))

        assert result.exists()
        assert result.read_text() == "new"

    def test_write_no_create_parents(self, tmp_path: Path) -> None:
        """Test writing a file with create_parents=False."""
        test_file = tmp_path / "direct.txt"
        result = safe_write(
            test_file, "content", options=WriteOptions(create_parents=False)
        )

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

    def test_safe_write_cleanup_propagates_oserror(self, tmp_path: Path) -> None:
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

    def test_safe_write_cleanup_succeeds(self, tmp_path: Path) -> None:
        """Test that cleanup during write unlinks the temp file."""
        test_file = tmp_path / "cleanup.txt"

        from unittest.mock import patch

        # Trigger an exception to enter the `except Exception:` cleanup block
        with patch("pathlib.Path.rename", side_effect=ValueError("Rename failed")):
            with pytest.raises(ValueError, match="Rename failed"):
                safe_write(test_file, "content", options=WriteOptions(atomic=True))

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

    def test_write_invalid_filename_blocked(self, tmp_path: Path) -> None:
        """Test that writing to an invalid filename raises an error instead of silently mutating."""
        test_file = tmp_path / "report:2023.txt"
        with pytest.raises(
            SecurityError, match="Unsafe or invalid characters in filename"
        ):
            safe_write(test_file, "content")


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

    def test_file_exists_error_when_path_is_file(self, tmp_path: Path) -> None:
        """Test that FileExistsError is raised if intermediate path is a file."""
        conflict_file = tmp_path / "conflict"
        conflict_file.write_text("content")

        with pytest.raises(FileExistsError, match="Path exists but is not a directory"):
            ensure_dir(conflict_file / "nested_dir")

        with pytest.raises(FileExistsError, match="Path exists but is not a directory"):
            ensure_dir(conflict_file)

    def test_root_directory_already_exists(self) -> None:
        """Test ensuring the root directory to cover the root parent check."""
        import sys

        # Determine the root directory based on the platform
        root = Path("C:\\") if sys.platform == "win32" else Path("/")

        # Ensure dir on the root should not loop indefinitely and should return the root
        result = ensure_dir(root)
        assert result == root

    def test_missing_intermediate_directory_created(self, tmp_path: Path) -> None:
        """Test creating a directory with a missing intermediate parent."""
        target = tmp_path / "missing" / "leaf"
        result = ensure_dir(target)

        assert result.exists()
        assert result.is_dir()
        assert (tmp_path / "missing").is_dir()

    def test_root_parent_loop_break(self, monkeypatch: pytest.MonkeyPatch) -> None:
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
            pass

        monkeypatch.setattr(Path, "mkdir", mock_mkdir)

        ensure_dir(root)


class TestSafeCopy:
    """Tests for safe_copy function."""

    def test_copy_file_with_base_dir(self, tmp_path: Path) -> None:
        """Test copying files with base_dir."""
        src = tmp_path / "src.txt"
        src.write_text("hello")

        dst_new = tmp_path / "dst_new.txt"
        safe_copy(src, dst_new, base_dir=tmp_path)
        assert dst_new.read_text() == "hello"

        dst_existing = tmp_path / "dst_exist.txt"
        dst_existing.write_text("old")
        safe_copy(src, dst_existing, base_dir=tmp_path, overwrite=True)
        assert dst_existing.read_text() == "hello"

    def test_copy_file(self, tmp_path: Path) -> None:
        """Test copying a file."""
        src = tmp_path / "source.txt"
        src.write_text("content")
        dst = tmp_path / "dest.txt"

        result = safe_copy(src, dst)

        assert result.exists()
        assert result.read_text() == "content"

    def test_copy_nonexistent_source(self, tmp_path: Path) -> None:
        """Test copying non-existent source raises error."""
        with pytest.raises(FileNotFoundError):
            safe_copy(tmp_path / "nonexistent.txt", tmp_path / "dest.txt")

    def test_copy_overwrite_denied(self, tmp_path: Path) -> None:
        """Test overwriting denied by default."""
        src = tmp_path / "source.txt"
        src.write_text("source")
        dst = tmp_path / "dest.txt"
        dst.write_text("existing")

        with pytest.raises(FileExistsError):
            safe_copy(src, dst, overwrite=False)

    def test_copy_overwrite_allowed(self, tmp_path: Path) -> None:
        """Test overwriting when allowed."""
        src = tmp_path / "source.txt"
        src.write_text("new content")
        dst = tmp_path / "dest.txt"
        dst.write_text("old content")

        safe_copy(src, dst, overwrite=True)

        assert dst.read_text() == "new content"

    def test_copy_creates_parent_dirs(self, tmp_path: Path) -> None:
        """Test that parent directories are created."""
        src = tmp_path / "source.txt"
        src.write_text("content")
        dst = tmp_path / "subdir" / "dest.txt"

        safe_copy(src, dst)

        assert dst.exists()


class TestSafeDelete:
    """Tests for safe_delete function."""

    def test_delete_file(self, tmp_path: Path) -> None:
        """Test deleting a file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        deleted = safe_delete(test_file)

        assert deleted is True
        assert not test_file.exists()

    def test_delete_nonexistent_missing_ok(self, tmp_path: Path) -> None:
        """Test deleting non-existent file with missing_ok=True."""
        deleted = safe_delete(tmp_path / "nonexistent.txt", missing_ok=True)
        assert deleted is False

    def test_delete_nonexistent_missing_not_ok(self, tmp_path: Path) -> None:
        """Test deleting non-existent file with missing_ok=False."""
        with pytest.raises(FileNotFoundError):
            safe_delete(tmp_path / "nonexistent.txt", missing_ok=False)

    def test_delete_directory_non_recursive(self, tmp_path: Path) -> None:
        """Test deleting empty directory."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        deleted = safe_delete(empty_dir, recursive=False)

        assert deleted is True
        assert not empty_dir.exists()

    def test_delete_directory_recursive(self, tmp_path: Path) -> None:
        """Test deleting directory recursively."""
        dir_path = tmp_path / "dir"
        dir_path.mkdir()
        (dir_path / "file.txt").write_text("content")

        deleted = safe_delete(dir_path, recursive=True)

        assert deleted is True
        assert not dir_path.exists()

    def test_path_traversal_blocked(self, tmp_path: Path) -> None:
        """Test that path traversal is blocked."""
        with pytest.raises(SecurityError):
            safe_delete(tmp_path / ".." / "etc" / "passwd", base_dir=tmp_path)

    def test_path_traversal_without_base_dir_blocked(self) -> None:
        """Test that path traversal is blocked when no base_dir is provided."""
        with pytest.raises(SecurityError):
            safe_delete("../etc/passwd")


class TestGetFileHash:
    """Tests for get_file_hash function."""

    def test_sha256_hash(self, tmp_path: Path) -> None:
        """Test SHA256 hash computation."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("hello")

        file_hash = get_file_hash(test_file)

        # Known SHA256 hash of "hello"
        expected = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        assert file_hash == expected

    def test_md5_hash_blocked(self, tmp_path: Path) -> None:
        """Test MD5 hash is blocked."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("hello")

        with pytest.raises(SecurityError, match="weak"):
            get_file_hash(test_file, algorithm="md5")

    def test_sha1_hash_blocked(self, tmp_path: Path) -> None:
        """Test SHA-1 hash is blocked."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("hello")

        with pytest.raises(SecurityError, match="weak"):
            get_file_hash(test_file, algorithm="sha1")

    def test_same_content_same_hash(self, tmp_path: Path) -> None:
        """Test that same content produces same hash."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file1.write_text("identical content")
        file2.write_text("identical content")

        assert get_file_hash(file1) == get_file_hash(file2)

    def test_path_traversal_blocked(self, tmp_path: Path) -> None:
        """Test that path traversal is blocked."""
        with pytest.raises(SecurityError):
            get_file_hash(
                tmp_path / ".." / "etc" / "passwd",
                base_dir=tmp_path,
            )


class TestFindFiles:
    """Tests for find_files function."""

    def test_find_all_files(self, tmp_path: Path) -> None:
        """Test finding all files."""
        (tmp_path / "file1.txt").write_text("1")
        (tmp_path / "file2.txt").write_text("2")

        files = list(find_files(tmp_path))

        assert len(files) == 2

    def test_find_by_pattern(self, tmp_path: Path) -> None:
        """Test finding files by pattern."""
        (tmp_path / "test.py").write_text("python")
        (tmp_path / "test.txt").write_text("text")

        files = list(find_files(tmp_path, pattern="*.py"))

        assert len(files) == 1
        assert files[0].suffix == ".py"

    def test_find_recursive(self, tmp_path: Path) -> None:
        """Test recursive file search."""
        (tmp_path / "root.txt").write_text("root")
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "nested.txt").write_text("nested")

        files = list(find_files(tmp_path, recursive=True))

        assert len(files) == 2

    def test_find_non_recursive(self, tmp_path: Path) -> None:
        """Test non-recursive file search."""
        (tmp_path / "root.txt").write_text("root")
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "nested.txt").write_text("nested")

        files = list(find_files(tmp_path, pattern="*.txt", recursive=False))

        assert len(files) == 1
        assert files[0].name == "root.txt"

    def test_find_excludes_hidden_by_default(self, tmp_path: Path) -> None:
        """Test that hidden files are excluded by default."""
        (tmp_path / "visible.txt").write_text("visible")
        (tmp_path / ".hidden.txt").write_text("hidden")

        files = list(find_files(tmp_path, include_hidden=False))

        assert len(files) == 1
        assert files[0].name == "visible.txt"

    def test_find_includes_hidden(self, tmp_path: Path) -> None:
        """Test including hidden files."""
        (tmp_path / "visible.txt").write_text("visible")
        (tmp_path / ".hidden.txt").write_text("hidden")

        files = list(find_files(tmp_path, include_hidden=True))

        assert len(files) == 2

    def test_find_in_nonexistent_dir(self, tmp_path: Path) -> None:
        """Test finding in non-existent directory returns empty list."""
        files = list(find_files(tmp_path / "nonexistent"))
        assert files == []
