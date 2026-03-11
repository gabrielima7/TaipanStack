from pathlib import Path

import pytest

from taipanstack.security.guards import SecurityError
from taipanstack.utils.filesystem import find_files, get_file_hash


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
