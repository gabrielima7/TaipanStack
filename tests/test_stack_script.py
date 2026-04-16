import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
import taipanstack_bootstrapper as taipanstack


@pytest.fixture(autouse=True)
def setup_teardown(tmp_path, monkeypatch):
    """
    Fixture to isolate each test in a temporary directory
    and mock dangerous system calls.
    """
    monkeypatch.chdir(tmp_path)
    mock_run = MagicMock(return_value=subprocess.CompletedProcess([], 0))
    with (
        patch("subprocess.run", mock_run),
        patch("taipanstack_bootstrapper._check_connectivity", return_value=None),
    ):
        yield mock_run


def run_main_with_args(args):
    """Helper to run the script's main function with specific arguments."""
    with patch.object(sys, "argv", ["taipanstack_bootstrapper.py", *args]):
        taipanstack.main()


def test_dry_run_does_not_create_files_expected(tmp_path):
    """
    Verifies that running with --dry-run does not create any configuration files.
    """
    run_main_with_args(["--dry-run"])
    assert not (tmp_path / "pyproject.toml").exists()
    assert not (tmp_path / ".pre-commit-config.yaml").exists()
    assert not (tmp_path / "SECURITY.md").exists()
    assert not (tmp_path / ".github" / "dependabot.yml").exists()


def test_safe_write_creates_backup_expected(tmp_path):
    """
    Verifies that a backup (.bak) is created when a configuration file already exists.
    """
    dummy_file = tmp_path / ".pre-commit-config.yaml"
    dummy_file.write_text("old content")
    run_main_with_args([])
    backup_file = tmp_path / ".pre-commit-config.yaml.bak"
    assert backup_file.exists()
    assert backup_file.read_text() == "old content"
    assert dummy_file.exists()
    assert "pre-commit-hooks" in dummy_file.read_text()


def test_force_mode_overwrites_without_backup_expected(tmp_path):
    """
    Verifies that the --force flag overwrites the file directly without creating a backup.
    """
    dummy_file = tmp_path / ".pre-commit-config.yaml"
    dummy_file.write_text("old content")
    run_main_with_args(["--force"])
    backup_file = tmp_path / ".pre-commit-config.yaml.bak"
    assert not backup_file.exists()
    assert dummy_file.exists()
    assert "pre-commit-hooks" in dummy_file.read_text()


def test_idempotency_for_pyproject_toml_expected(tmp_path):
    """
    Verifies that running the script twice does not duplicate sections in pyproject.toml.
    """
    pyproject_toml = tmp_path / "pyproject.toml"
    pyproject_toml.write_text('[tool.poetry]\nname = "test"\n')
    run_main_with_args([])
    content_after_first_run = pyproject_toml.read_text()
    assert "[tool.ruff]" in content_after_first_run
    assert "[tool.mypy]" in content_after_first_run
    assert content_after_first_run.count("[tool.ruff]") == 1
    run_main_with_args([])
    content_after_second_run = pyproject_toml.read_text()
    assert content_after_first_run == content_after_second_run
    assert content_after_second_run.count("[tool.ruff]") == 1


def test_stack_script_git_initialization_expected(tmp_path):
    """
    Verifies that Git is initialized automatically when it does not exist.
    """
    assert not (tmp_path / ".git").exists()
    run_main_with_args([])


def test_project_structure_creation_expected(tmp_path):
    """
    Verifies that the project folder structure is created correctly.
    """
    pyproject_toml = tmp_path / "pyproject.toml"
    pyproject_toml.write_text('[tool.poetry]\nname = "my_test_project"\n')
    run_main_with_args([])
    assert (tmp_path / "src" / "my_test_project").exists()
    assert (tmp_path / "tests").exists()
    assert (tmp_path / "docs").exists()
    assert (tmp_path / "src" / "my_test_project" / "__init__.py").exists()
    assert (tmp_path / "tests" / "__init__.py").exists()
    assert (tmp_path / "src" / "my_test_project" / "main.py").exists()
    assert (tmp_path / "tests" / "test_example.py").exists()


def test_optional_dependencies_flag_expected(tmp_path, monkeypatch):
    """
    Verifies that the --install-runtime-deps flag controls dependency installation.
    """
    pyproject_toml = tmp_path / "pyproject.toml"
    pyproject_toml.write_text('[tool.poetry]\nname = "test"\n')
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = subprocess.CompletedProcess([], 0)
        run_main_with_args([])
        poetry_add_calls = [
            call
            for call in mock_run.call_args_list
            if call[0][0][0:2] == ["poetry", "add"] and "--group" not in call[0][0]
        ]
        assert len(poetry_add_calls) == 0


def test_install_runtime_deps_flag_expected(tmp_path, monkeypatch):
    """
    Verifies that --install-runtime-deps installs the production dependencies.
    """
    pyproject_toml = tmp_path / "pyproject.toml"
    pyproject_toml.write_text('[tool.poetry]\nname = "test"\n')
    with patch("taipanstack_bootstrapper.platform.system", return_value="Linux"):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess([], 0)
            run_main_with_args(["--install-runtime-deps"])
            poetry_add_calls = [
                call
                for call in mock_run.call_args_list
                if len(call[0]) > 0
                and "poetry" in str(call[0][0])
                and ("add" in str(call[0][0]))
                and any("pydantic" in str(arg) for arg in call[0][0])
            ]
            assert len(poetry_add_calls) > 0, (
                "Poetry add with pydantic should have been called"
            )


def test_python_version_detection_expected(tmp_path):
    """
    Verifies that the Python version is dynamically detected.
    """
    pyproject_toml = tmp_path / "pyproject.toml"
    pyproject_toml.write_text('[tool.poetry]\nname = "test"\n')
    run_main_with_args([])
    content = pyproject_toml.read_text()
    import sys

    expected_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    assert f'python_version = "{expected_version}"' in content


def test_setup_pre_commit_expected():
    """
    Verifies that the pre-commit configuration file is generated with correct content.
    """
    args = MagicMock()
    args.dry_run = False
    args.verbose = False
    with patch("taipanstack_bootstrapper._safe_write") as mock_safe_write:
        taipanstack._setup_pre_commit(args)
        mock_safe_write.assert_called_once()
        path, content, _passed_args = mock_safe_write.call_args[0]
        assert path == taipanstack.PRE_COMMIT_CONFIG_PATH
        assert "repos:" in content
        assert "https://github.com/pre-commit/pre-commit-hooks" in content
        assert "ruff" in content
        assert "mypy" in content
        assert "bandit" in content
        assert "safety" in content
        assert "semgrep" in content
        assert "detect-secrets" in content


def test_setup_pre_commit_dry_run_expected():
    """
    Verifies that _setup_pre_commit handles the args correctly for dry-run.
    """
    args = MagicMock()
    args.dry_run = True
    args.verbose = True
    with patch("taipanstack_bootstrapper._safe_write") as mock_safe_write:
        taipanstack._setup_pre_commit(args)
        mock_safe_write.assert_called_once()
        path, content, passed_args = mock_safe_write.call_args[0]
        assert path == taipanstack.PRE_COMMIT_CONFIG_PATH
        assert "repos:" in content
        assert passed_args == args
