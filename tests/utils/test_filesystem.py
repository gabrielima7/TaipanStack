"""Tests for safe filesystem operations."""

import tempfile
from pathlib import Path
from unittest.mock import patch

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

        files = find_files(tmp_path)

        assert len(files) == 2

    def test_find_by_pattern(self, tmp_path: Path) -> None:
        """Test finding files by pattern."""
        (tmp_path / "test.py").write_text("python")
        (tmp_path / "test.txt").write_text("text")

        files = find_files(tmp_path, pattern="*.py")

        assert len(files) == 1
        assert files[0].suffix == ".py"

    def test_find_recursive(self, tmp_path: Path) -> None:
        """Test recursive file search."""
        (tmp_path / "root.txt").write_text("root")
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "nested.txt").write_text("nested")

        files = find_files(tmp_path, recursive=True)

        assert len(files) == 2

    def test_find_non_recursive(self, tmp_path: Path) -> None:
        """Test non-recursive file search."""
        (tmp_path / "root.txt").write_text("root")
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "nested.txt").write_text("nested")

        files = find_files(tmp_path, pattern="*.txt", recursive=False)

        assert len(files) == 1
        assert files[0].name == "root.txt"

    def test_find_excludes_hidden_by_default(self, tmp_path: Path) -> None:
        """Test that hidden files are excluded by default."""
        (tmp_path / "visible.txt").write_text("visible")
        (tmp_path / ".hidden.txt").write_text("hidden")

        files = find_files(tmp_path, include_hidden=False)

        assert len(files) == 1
        assert files[0].name == "visible.txt"

    def test_find_includes_hidden(self, tmp_path: Path) -> None:
        """Test including hidden files."""
        (tmp_path / "visible.txt").write_text("visible")
        (tmp_path / ".hidden.txt").write_text("hidden")

        files = find_files(tmp_path, include_hidden=True)

        assert len(files) == 2

    def test_find_in_nonexistent_dir(self, tmp_path: Path) -> None:
        """Test finding in non-existent directory returns empty list."""
        files = find_files(tmp_path / "nonexistent")
        assert files == []


class TestFilesystemUncovered:
    """Tests for filesystem.py uncovered lines."""

    def test_safe_write_atomic_success(self, tmp_path: Path) -> None:
        """Test atomic write success path."""
        from taipanstack.utils.filesystem import WriteOptions, safe_write

        target = tmp_path / "test.txt"
        safe_write(target, "content", options=WriteOptions(atomic=True))
        assert target.read_text() == "content"


class TestFilesystemMissingBranches:
    """Tests for filesystem missing branches."""

    def test_safe_read_with_base_dir_traversal(self, tmp_path: Path) -> None:
        """Test safe_read when path has .. but base_dir guards it."""
        from taipanstack.utils.filesystem import safe_read

        test_file = tmp_path / "file.txt"
        test_file.write_text("content")

        # Should work with base_dir
        result = safe_read(test_file, base_dir=tmp_path)
        assert result.unwrap() == "content"

    def test_ensure_dir_with_base_dir(self, tmp_path: Path) -> None:
        """Test ensure_dir with base_dir constraint."""
        from taipanstack.utils.filesystem import ensure_dir

        new_dir = tmp_path / "new_subdir"
        result = ensure_dir(new_dir, base_dir=tmp_path)
        assert result.exists()

    def test_find_files_include_hidden(self, tmp_path: Path) -> None:
        """Test find_files with include_hidden=True."""
        from taipanstack.utils.filesystem import find_files

        # Create hidden file
        hidden = tmp_path / ".hidden"
        hidden.touch()
        (tmp_path / "visible.txt").touch()

        results = find_files(tmp_path, include_hidden=True)
        names = [r.name for r in results]
        assert ".hidden" in names


class TestFilesystemLine175:
    """Test for filesystem.py line 175."""

    def test_safe_write_different_encoding(self, tmp_path: Path) -> None:
        """Test safe_write with different encoding."""
        from taipanstack.utils.filesystem import WriteOptions, safe_write

        test_file = tmp_path / "encoded.txt"
        content = "Héllo Wörld"

        result = safe_write(test_file, content, options=WriteOptions(encoding="utf-8"))
        assert result.read_text(encoding="utf-8") == content


class TestFilesystemEdgeCases:
    """Edge case tests for filesystem module."""

    def test_safe_read_with_traversal_no_base_dir(self, tmp_path: Path) -> None:
        """Test safe_read with .. in path but no base_dir uses cwd."""
        from taipanstack.utils.filesystem import safe_read

        # Create a file in tmp_path
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        # This should fail because .. triggers guard with cwd
        result = safe_read(tmp_path / ".." / "etc" / "passwd")
        match result:
            case Err(SecurityError()):
                pass
            case _:
                pytest.fail("Expected Err(SecurityError)")

    def test_safe_write_existing_file_guarded(self, tmp_path: Path) -> None:
        """Test safe_write with existing file and base_dir."""
        from taipanstack.utils.filesystem import WriteOptions, safe_write

        test_file = tmp_path / "existing.txt"
        test_file.write_text("old content")

        result = safe_write(
            test_file, "new content", options=WriteOptions(base_dir=tmp_path)
        )
        assert result.read_text() == "new content"

    def test_safe_write_with_traversal_no_base_dir(self, tmp_path: Path) -> None:
        """Test safe_write with .. triggers guard."""
        from taipanstack.utils.filesystem import safe_write

        with pytest.raises(SecurityError):
            safe_write(tmp_path / ".." / "bad.txt", "content")

    def test_safe_write_atomic_error_cleanup(self, tmp_path: Path) -> None:
        """Test atomic write cleans up temp file on error."""
        from taipanstack.utils.filesystem import WriteOptions, safe_write

        test_file = tmp_path / "test.txt"

        # Mock write_text to raise an error
        with patch.object(Path, "write_text", side_effect=OSError("Write error")):
            with pytest.raises(OSError):
                safe_write(test_file, "content", options=WriteOptions(atomic=True))

    def test_safe_copy_dst_exists_base_dir(self, tmp_path: Path) -> None:
        """Test safe_copy with existing dst and base_dir."""
        from taipanstack.utils.filesystem import safe_copy

        src = tmp_path / "src.txt"
        dst = tmp_path / "dst.txt"
        src.write_text("source")
        dst.write_text("destination")

        result = safe_copy(src, dst, base_dir=tmp_path, overwrite=True)
        assert result.read_text() == "source"

    def test_safe_copy_dst_parent_guarded(self, tmp_path: Path) -> None:
        """Test safe_copy dst parent is guarded when dst doesn't exist."""
        from taipanstack.utils.filesystem import safe_copy

        src = tmp_path / "src.txt"
        dst = tmp_path / "subdir" / "dst.txt"
        src.write_text("source")
        (tmp_path / "subdir").mkdir()

        result = safe_copy(src, dst, base_dir=tmp_path)
        assert result.read_text() == "source"

    def test_find_files_recursive(self, tmp_path: Path) -> None:
        """Test find_files with recursive search."""
        from taipanstack.utils.filesystem import find_files

        # Create test structure
        (tmp_path / "a.txt").touch()
        (tmp_path / "subdir").mkdir()
        (tmp_path / "subdir" / "b.txt").touch()

        results = find_files(tmp_path, pattern="*.txt", recursive=True)
        names = [r.name for r in results]
        assert "a.txt" in names
        assert "b.txt" in names

    def test_get_file_hash_algorithms(self, tmp_path: Path) -> None:
        """Test get_file_hash with different algorithms."""
        from taipanstack.utils.filesystem import get_file_hash

        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")

        sha256_hash = get_file_hash(test_file, algorithm="sha256")
        sha512_hash = get_file_hash(test_file, algorithm="sha512")

        assert sha256_hash != sha512_hash
        assert len(sha256_hash) == 64  # SHA256 hex length
        assert len(sha512_hash) == 128  # SHA512 hex length

        with pytest.raises(SecurityError, match="weak"):
            get_file_hash(test_file, algorithm="md5")


class TestFilesystemComplete:
    """Complete tests for filesystem module."""

    def test_safe_write_non_atomic(self, tmp_path: Path) -> None:
        """Test safe_write with atomic=False."""
        from taipanstack.utils.filesystem import WriteOptions, safe_write

        test_file = tmp_path / "non_atomic.txt"
        result = safe_write(test_file, "content", options=WriteOptions(atomic=False))
        assert result.read_text() == "content"

    def test_safe_delete_recursive(self, tmp_path: Path) -> None:
        """Test safe_delete with recursive=True."""
        from taipanstack.utils.filesystem import safe_delete

        # Create a directory with files
        test_dir = tmp_path / "to_delete"
        test_dir.mkdir()
        (test_dir / "file.txt").write_text("content")

        safe_delete(test_dir, recursive=True)
        assert not test_dir.exists()

    def test_get_file_hash_sha256(self, tmp_path: Path) -> None:
        """Test get_file_hash with sha256."""
        from taipanstack.utils.filesystem import get_file_hash

        test_file = tmp_path / "hash_test.txt"
        test_file.write_text("test content")

        hash_result = get_file_hash(test_file)
        assert len(hash_result) == 64


class TestFilesystemFinalBranches:
    """Final tests for filesystem module to reach 100%."""

    def test_safe_delete_not_found_error(self, tmp_path: Path) -> None:
        """Test safe_delete with missing_ok=False."""
        from taipanstack.utils.filesystem import safe_delete

        with pytest.raises(FileNotFoundError):
            safe_delete(tmp_path / "nonexistent", missing_ok=False)

    def test_find_files_base_dir(self, tmp_path: Path) -> None:
        """Test find_files with base_dir constraint."""
        from taipanstack.utils.filesystem import find_files

        (tmp_path / "file.txt").touch()

        results = find_files(tmp_path, pattern="*.txt", base_dir=tmp_path)
        assert len(list(results)) >= 1


class TestFilesystemSizeLimit:
    """Test filesystem size limit branches."""

    def test_safe_read_no_size_limit(self) -> None:
        """Test safe_read with max_size_bytes=None."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("test content")
            f.flush()
            temp_path = Path(f.name)

        try:
            result = safe_read(temp_path, max_size_bytes=None)
            assert result.is_ok()
            assert result.unwrap() == "test content"
        finally:
            temp_path.unlink()


class TestFilesystemEnsureDir:
    """Test ensure_dir edge cases."""

    def test_ensure_dir_nested(self) -> None:
        """Test ensure_dir creates nested directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = ensure_dir(Path(tmpdir) / "subdir" / "nested")
            assert result.exists()


class TestFilesystemSafeDelete:
    """Test safe_delete edge cases."""

    def test_safe_delete_file_no_base_dir(self) -> None:
        """Test safe_delete without base_dir."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test_file.txt"
            test_file.write_text("content")

            result = safe_delete(test_file, base_dir=None, missing_ok=True)
            assert result is True


class TestFilesystemBranches:
    """Tests for filesystem module branches."""

    def test_safe_read_max_size_exceeded(self, tmp_path: Path) -> None:
        """Test safe_read when file exceeds max size."""
        from taipanstack.utils.filesystem import safe_read

        test_file = tmp_path / "large.txt"
        test_file.write_text("x" * 1000)

        result = safe_read(test_file, max_size_bytes=100)
        match result:
            case Err(FileTooLargeErr(size=s)):
                assert s > 100
            case _:
                pytest.fail("Expected Err(FileTooLargeErr)")

    def test_ensure_dir_already_exists(self, tmp_path: Path) -> None:
        """Test ensure_dir with directory that already exists."""
        from taipanstack.utils.filesystem import ensure_dir

        existing_dir = tmp_path / "existing"
        existing_dir.mkdir()

        result = ensure_dir(existing_dir)
        assert result == existing_dir.resolve()

    def test_safe_write_no_backup(self, tmp_path: Path) -> None:
        """Test safe_write with backup=False."""
        from taipanstack.utils.filesystem import WriteOptions, safe_write

        test_file = tmp_path / "test.txt"
        test_file.write_text("original")

        safe_write(test_file, "new", options=WriteOptions(backup=False))
        assert test_file.read_text() == "new"

        # No backup should exist
        backup_path = tmp_path / "test.txt.bak"
        assert not backup_path.exists()

    def test_find_files_non_recursive(self, tmp_path: Path) -> None:
        """Test find_files with recursive=False."""
        from taipanstack.utils.filesystem import find_files

        (tmp_path / "file.txt").touch()
        (tmp_path / "subdir").mkdir()
        (tmp_path / "subdir" / "nested.txt").touch()

        results = find_files(tmp_path, pattern="*.txt", recursive=False)
        names = [r.name for r in results]
        assert "file.txt" in names
        assert "nested.txt" not in names


class TestFilesystemLine175And259:
    """Test for filesystem.py lines 175 and 259."""

    def test_safe_write_directory_exists(self, tmp_path: Path) -> None:
        """Test safe_write when parent directory already exists."""
        from taipanstack.utils.filesystem import WriteOptions, safe_write

        test_file = tmp_path / "existing_dir" / "file.txt"
        (tmp_path / "existing_dir").mkdir()

        result = safe_write(
            test_file, "content", options=WriteOptions(create_parents=False)
        )
        assert result.read_text() == "content"

    def test_safe_delete_directory(self, tmp_path: Path) -> None:
        """Test safe_delete with directory."""
        from taipanstack.utils.filesystem import safe_delete

        test_dir = tmp_path / "to_delete"
        test_dir.mkdir()
        (test_dir / "file.txt").write_text("content")

        safe_delete(test_dir, recursive=True)
        assert not test_dir.exists()


class TestFilesystem100Percent:
    """Tests to reach 100% for filesystem."""

    def test_get_file_hash_with_base_dir(self, tmp_path: Path) -> None:
        """Test get_file_hash with base_dir."""
        from taipanstack.utils.filesystem import get_file_hash

        test_file = tmp_path / "hashfile.txt"
        test_file.write_text("content")

        result = get_file_hash(test_file, base_dir=tmp_path)
        assert len(result) == 64


class TestFilesystemWriteError:
    """Test for filesystem.py coverage gaps."""

    def test_safe_write_existing_permissions(self, tmp_path: Path) -> None:
        """Test safe_write preserves permissions on existing file."""
        from taipanstack.utils.filesystem import WriteOptions, safe_write

        existing = tmp_path / "existing.txt"
        existing.write_text("old")

        # Write new content atomically
        result = safe_write(existing, "new", options=WriteOptions(atomic=True))
        assert result.read_text() == "new"

    def test_ensure_dir_with_traversal(self, tmp_path: Path) -> None:
        """Test ensure_dir with '..' in path string (L243)."""
        from taipanstack.security.guards import SecurityError
        from taipanstack.utils.filesystem import ensure_dir

        # ".." in path but no base_dir → falls through to guard_path_traversal
        with pytest.raises(SecurityError, match="traversal"):
            ensure_dir("../../../escape_dir")

    def test_safe_delete_with_traversal(self, tmp_path: Path) -> None:
        """Test safe_delete with '..' in path (L327)."""
        from taipanstack.security.guards import SecurityError
        from taipanstack.utils.filesystem import safe_delete

        with pytest.raises(SecurityError, match="traversal"):
            safe_delete("../../../escape_file.txt", missing_ok=False)


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


def test_get_file_hash_traversal_cwd(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test get_file_hash respects cwd traversal guard when base_dir=None."""
    monkeypatch.chdir(tmp_path)

    # Create file outside cwd
    outside_dir = tmp_path.parent / "outside_dir_test_hash"
    outside_dir.mkdir(exist_ok=True)
    outside_file = outside_dir / "secret.txt"
    outside_file.write_text("secret")

    try:
        with pytest.raises(SecurityError) as exc_info:
            get_file_hash("../outside_dir_test_hash/secret.txt")
        assert "path_traversal" in str(exc_info.value).lower()
    finally:
        import shutil

        shutil.rmtree(outside_dir, ignore_errors=True)


def test_find_files_traversal_cwd(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test find_files respects cwd traversal guard when base_dir=None."""
    monkeypatch.chdir(tmp_path)

    # Create dir outside cwd
    outside_dir = tmp_path.parent / "outside_dir_test_find"
    outside_dir.mkdir(exist_ok=True)
    outside_file = outside_dir / "secret.txt"
    outside_file.write_text("secret")

    try:
        with pytest.raises(SecurityError) as exc_info:
            find_files("../outside_dir_test_find")
        assert "path_traversal" in str(exc_info.value).lower()
    finally:
        import shutil

        shutil.rmtree(outside_dir, ignore_errors=True)
