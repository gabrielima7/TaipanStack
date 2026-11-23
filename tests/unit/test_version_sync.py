import re
import tomllib
from pathlib import Path

def get_init_version() -> str:
    init_path = Path("src/taipanstack/__init__.py")
    match = re.search(r'(?m)^__version__\s*=\s*["\']([^"\']+)["\']', init_path.read_text(encoding="utf-8"))
    assert match is not None
    return match.group(1)

def test_version_consistency():
    pyproject_path = Path("pyproject.toml")
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)
    toml_version = data["project"]["version"]
    init_version = get_init_version()
    assert toml_version == init_version
    assert re.match(r"^\d+\.\d+\.\d+$", toml_version) is not None
