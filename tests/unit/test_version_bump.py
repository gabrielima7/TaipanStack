import pytest
from pathlib import Path
from scripts.bump_version import calculate_next_version, update_project_files

def test_bump_standard_patch():
    assert calculate_next_version("0.7.0") == "0.7.1"
    assert calculate_next_version("v0.7.0") == "0.7.1"
    assert calculate_next_version("0.6.9") == "0.6.10"

def test_bump_rollover_ten_to_minor():
    assert calculate_next_version("0.6.10") == "0.7.0"
    assert calculate_next_version("v0.6.10") == "0.7.0"
    assert calculate_next_version("1.2.10") == "1.3.0"

def test_invalid_version_raises():
    with pytest.raises(ValueError):
        calculate_next_version("invalid-version")
    with pytest.raises(ValueError):
        calculate_next_version("")

def test_update_project_files(tmp_path: Path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[project]\nversion = "0.6.4"\nname = "test"\n', encoding="utf-8")
    
    init_dir = tmp_path / "src" / "taipanstack"
    init_dir.mkdir(parents=True)
    init_file = init_dir / "__init__.py"
    init_file.write_text('__version__ = "0.6.3"\n', encoding="utf-8")

    update_project_files("0.7.0", root_dir=tmp_path)

    assert 'version = "0.7.0"' in pyproject.read_text(encoding="utf-8")
    assert '__version__ = "0.7.0"' in init_file.read_text(encoding="utf-8")
