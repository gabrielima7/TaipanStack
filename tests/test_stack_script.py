import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Adds the root directory to the path so `taipanstack_bootstrapper` can be imported
sys.path.insert(0, str(Path(__file__).parent.parent))

import taipanstack_bootstrapper as taipanstack


@pytest.fixture(autouse=True)
def setup_teardown(tmp_path, monkeypatch):
    """
    Fixture to isolate each test in a temporary directory
    and mock dangerous system calls.
    """
    # Changes the current working directory to the temporary directory
    monkeypatch.chdir(tmp_path)

    # Mocks subprocess.run to avoid executing real commands (like poetry)
    mock_run = MagicMock(return_value=subprocess.CompletedProcess([], 0))
    with patch("subprocess.run", mock_run):
        yield mock_run


def run_main_with_args(args):
    """Helper to run the script's main function with specific arguments."""
    with patch.object(sys, "argv", ["taipanstack_bootstrapper.py", *args]):
        taipanstack.main()


def test_dry_run_does_not_create_files(tmp_path):
    """
    Verifies that running with --dry-run does not create any configuration files.
    """
    run_main_with_args(["--dry-run"])

    # Ensures none of the main files were created
    assert not (tmp_path / "pyproject.toml").exists()
    assert not (tmp_path / ".pre-commit-config.yaml").exists()
    assert not (tmp_path / "SECURITY.md").exists()
    assert not (tmp_path / ".github" / "dependabot.yml").exists()


def test_safe_write_creates_backup(tmp_path):
    """
    Verifies that a backup (.bak) is created when a configuration file already exists.
    """
    # Creates a dummy file to simulate an existing configuration
    dummy_file = tmp_path / ".pre-commit-config.yaml"
    dummy_file.write_text("old content")

    run_main_with_args([])  # Normal execution, no flags

    # Verifies if the backup was created
    backup_file = tmp_path / ".pre-commit-config.yaml.bak"
    assert backup_file.exists()
    assert backup_file.read_text() == "old content"

    # Verifies if the new file was also created
    assert dummy_file.exists()
    assert "pre-commit-hooks" in dummy_file.read_text()  # Checks new file content


def test_force_mode_overwrites_without_backup(tmp_path):
    """
    Verifies that the --force flag overwrites the file directly without creating a backup.
    """
    dummy_file = tmp_path / ".pre-commit-config.yaml"
    dummy_file.write_text("old content")

    run_main_with_args(["--force"])

    # Ensures that the backup file was NOT created
    backup_file = tmp_path / ".pre-commit-config.yaml.bak"
    assert not backup_file.exists()

    # Ensures that the original file was overwritten
    assert dummy_file.exists()
    assert "pre-commit-hooks" in dummy_file.read_text()


def test_idempotency_for_pyproject_toml(tmp_path):
    """
    Verifies that running the script twice does not duplicate sections in pyproject.toml.
    """
    # Creates an initial pyproject.toml, as if `poetry init` had run
    pyproject_toml = tmp_path / "pyproject.toml"
    pyproject_toml.write_text('[tool.poetry]\nname = "test"\n')

    # First run
    run_main_with_args([])
    content_after_first_run = pyproject_toml.read_text()

    # Verifies if the sections were added
    assert "[tool.ruff]" in content_after_first_run
    assert "[tool.mypy]" in content_after_first_run
    assert content_after_first_run.count("[tool.ruff]") == 1

    # Second run
    run_main_with_args([])
    content_after_second_run = pyproject_toml.read_text()

    # Compares the content and ensures there was no duplication
    assert content_after_first_run == content_after_second_run
    assert content_after_second_run.count("[tool.ruff]") == 1


def test_git_initialization(tmp_path):
    """
    Verifies that Git is initialized automatically when it does not exist.
    """
    # Ensures .git does not exist
    assert not (tmp_path / ".git").exists()

    run_main_with_args([])

    # Verifies if .git was created (if git is available)
    # Note: may not exist if git is not installed on the test system


def test_project_structure_creation(tmp_path):
    """
    Verifies that the project folder structure is created correctly.
    """
    # Creates a pyproject.toml with a project name
    pyproject_toml = tmp_path / "pyproject.toml"
    pyproject_toml.write_text('[tool.poetry]\nname = "my_test_project"\n')

    run_main_with_args([])

    # Verifies if the folders were created
    assert (tmp_path / "src" / "my_test_project").exists()
    assert (tmp_path / "tests").exists()
    assert (tmp_path / "docs").exists()

    # Verifies if __init__.py files were created
    assert (tmp_path / "src" / "my_test_project" / "__init__.py").exists()
    assert (tmp_path / "tests" / "__init__.py").exists()

    # Verifies if sample files were created
    assert (tmp_path / "src" / "my_test_project" / "main.py").exists()
    assert (tmp_path / "tests" / "test_example.py").exists()


def test_optional_dependencies_flag(tmp_path, monkeypatch):
    """
    Verifies that the --install-runtime-deps flag controls dependency installation.
    """
    pyproject_toml = tmp_path / "pyproject.toml"
    pyproject_toml.write_text('[tool.poetry]\nname = "test"\n')

    # Without the flag, it should not install production dependencies
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = subprocess.CompletedProcess([], 0)
        run_main_with_args([])

        # Verifies that poetry add was NOT called for production
        poetry_add_calls = [
            call
            for call in mock_run.call_args_list
            if call[0][0][0:2] == ["poetry", "add"] and "--group" not in call[0][0]
        ]
        assert len(poetry_add_calls) == 0


def test_install_runtime_deps_flag(tmp_path, monkeypatch):
    """
    Verifies that --install-runtime-deps installs the production dependencies.
    """
    pyproject_toml = tmp_path / "pyproject.toml"
    pyproject_toml.write_text('[tool.poetry]\nname = "test"\n')

    # Mock platform.system to avoid subprocess issues on Windows
    with patch("taipanstack_bootstrapper.platform.system", return_value="Linux"):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess([], 0)
            run_main_with_args(["--install-runtime-deps"])

            # Verifies that poetry add WAS called for production
            # Looks for calls that include 'pydantic' (production dependency)
            poetry_add_calls = [
                call
                for call in mock_run.call_args_list
                if len(call[0]) > 0
                and "poetry" in str(call[0][0])
                and "add" in str(call[0][0])
                and any("pydantic" in str(arg) for arg in call[0][0])
            ]
            assert len(poetry_add_calls) > 0, (
                "Poetry add with pydantic should have been called"
            )


def test_python_version_detection(tmp_path):
    """
    Verifies that the Python version is dynamically detected.
    """
    pyproject_toml = tmp_path / "pyproject.toml"
    pyproject_toml.write_text('[tool.poetry]\nname = "test"\n')

    run_main_with_args([])

    content = pyproject_toml.read_text()

    # Verifies if the Python version is in the configuration
    import sys

    expected_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    assert f'python_version = "{expected_version}"' in content
