import argparse
import subprocess
from unittest.mock import patch

import pytest
import taipanstack_bootstrapper as taipanstack


def test_handle_error(capsys):
    with pytest.raises(SystemExit) as exc:
        taipanstack._handle_error("Test error")
    assert exc.value.code == 1
    captured = capsys.readouterr()
    assert "Error: Test error\n" in captured.err


def test_run_command_file_not_found():
    args = argparse.Namespace(dry_run=False, verbose=False)
    with (
        patch("subprocess.run", side_effect=FileNotFoundError),
        patch("taipanstack_bootstrapper._handle_error") as mock_error,
    ):
        taipanstack._run_command(["notacommand"], args)
        mock_error.assert_called_once()
        assert "not found" in mock_error.call_args[0][0]


def test_run_command_called_process_error():
    args = argparse.Namespace(dry_run=False, verbose=False)
    err = subprocess.CalledProcessError(1, ["cmd"], stderr="some error")
    with (
        patch("subprocess.run", side_effect=err),
        patch("taipanstack_bootstrapper._handle_error") as mock_error,
    ):
        taipanstack._run_command(["cmd"], args)
        mock_error.assert_called_once()
        assert "failed with exit code 1" in mock_error.call_args[0][0]
        assert "some error" in mock_error.call_args[0][0]


def test_safe_write_rename_error(tmp_path):
    args = argparse.Namespace(dry_run=False, verbose=False, force=False)
    file_path = tmp_path / "test.txt"
    file_path.write_text("old")
    with (
        patch("pathlib.Path.rename", side_effect=PermissionError),
        patch("taipanstack_bootstrapper._handle_error") as mock_error,
    ):
        taipanstack._safe_write(file_path, "new", args)
        mock_error.assert_called_once()
        assert "Could not create backup" in mock_error.call_args[0][0]


def test_safe_write_write_error(tmp_path):
    args = argparse.Namespace(dry_run=False, verbose=False, force=False)
    file_path = tmp_path / "test.txt"
    with (
        patch("pathlib.Path.write_text", side_effect=PermissionError),
        patch("taipanstack_bootstrapper._handle_error") as mock_error,
    ):
        taipanstack._safe_write(file_path, "new", args)
        mock_error.assert_called_once()
        assert "Could not write to file" in mock_error.call_args[0][0]


def test_generate_pyproject_config_dry_run_with_config(tmp_path, monkeypatch):
    args = argparse.Namespace(dry_run=True, verbose=True, force=False)
    monkeypatch.chdir(tmp_path)
    with patch("taipanstack_bootstrapper._log") as mock_log:
        taipanstack._generate_pyproject_config(args)
        mock_log.assert_any_call(
            "Would add tool configurations to pyproject.toml", args, is_verbose=True
        )


def test_generate_pyproject_config_already_exists(tmp_path, monkeypatch):
    args = argparse.Namespace(dry_run=False, verbose=False, force=False)
    monkeypatch.chdir(tmp_path)
    toml = tmp_path / "pyproject.toml"
    toml.write_text("[tool.ruff]\n[tool.mypy]\n[tool.pytest.ini_options]\n")
    with patch("taipanstack_bootstrapper._log") as mock_log:
        taipanstack._generate_pyproject_config(args)
        mock_log.assert_any_call(
            "✅ Configurations for Ruff, Mypy, and Pytest already exist in pyproject.toml.",
            args,
        )


def test_generate_dependabot_config_error(tmp_path, monkeypatch):
    args = argparse.Namespace(dry_run=False, verbose=False, force=False)
    monkeypatch.chdir(tmp_path)
    with (
        patch("pathlib.Path.mkdir", side_effect=PermissionError),
        patch("taipanstack_bootstrapper._handle_error") as mock_error,
        patch("taipanstack_bootstrapper._safe_write"),
    ):
        taipanstack._generate_dependabot_config(args)
        mock_error.assert_called_once()
        assert "Could not create .github directory" in mock_error.call_args[0][0]


def test_check_git_initialized_already(tmp_path, monkeypatch):
    args = argparse.Namespace(dry_run=False, verbose=False, force=False)
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".git").mkdir()
    with patch("taipanstack_bootstrapper._log") as mock_log:
        taipanstack._check_git_initialized(args)
        mock_log.assert_any_call("✅ Git repository already initialized.", args)


def test_check_git_initialized_no_git(tmp_path, monkeypatch):
    args = argparse.Namespace(dry_run=False, verbose=False, force=False)
    monkeypatch.chdir(tmp_path)
    with (
        patch("shutil.which", return_value=None),
        patch("taipanstack_bootstrapper._log") as mock_log,
    ):
        taipanstack._check_git_initialized(args)
        mock_log.assert_any_call(
            "⚠️  Git not found in PATH. Skipping Git initialization.", args
        )


def test_check_connectivity_success():
    args = argparse.Namespace(dry_run=False, verbose=False, force=False)
    with patch("socket.create_connection"):
        taipanstack._check_connectivity(args)


def test_check_connectivity_failure():
    args = argparse.Namespace(dry_run=False, verbose=False, force=False)
    with (
        patch("socket.create_connection", side_effect=TimeoutError),
        patch("taipanstack_bootstrapper._handle_error") as mock_error,
    ):
        taipanstack._check_connectivity(args)
        mock_error.assert_called_once()
        assert "Could not connect to the internet" in mock_error.call_args[0][0]


def test_create_project_structure_toml_error(tmp_path, monkeypatch):
    args = argparse.Namespace(dry_run=False, verbose=False, force=False)
    monkeypatch.chdir(tmp_path)
    toml = tmp_path / "pyproject.toml"
    toml.write_text("")
    with (
        patch("pathlib.Path.read_text", side_effect=OSError),
        patch("pathlib.Path.mkdir"),
    ):
        taipanstack._create_project_structure(args)


def test_create_project_structure_mkdir_error(tmp_path, monkeypatch):
    args = argparse.Namespace(dry_run=False, verbose=False, force=False)
    monkeypatch.chdir(tmp_path)
    with (
        patch("pathlib.Path.mkdir", side_effect=PermissionError),
        patch("taipanstack_bootstrapper._log") as mock_log,
    ):
        taipanstack._create_project_structure(args)
        assert any("Could not create" in call[0][0] for call in mock_log.call_args_list)


def test_create_project_structure_init_write_error(tmp_path, monkeypatch):
    args = argparse.Namespace(dry_run=False, verbose=False, force=False)
    monkeypatch.chdir(tmp_path)
    with (
        patch("pathlib.Path.write_text", side_effect=PermissionError),
        patch("taipanstack_bootstrapper._log") as mock_log,
    ):
        taipanstack._create_project_structure(args)
        assert any(
            "Could not create src/my_project/__init__.py" in call[0][0]
            for call in mock_log.call_args_list
        )


def test_create_project_structure_main_write_error(tmp_path, monkeypatch):
    args = argparse.Namespace(dry_run=False, verbose=False, force=False)
    monkeypatch.chdir(tmp_path)
    with (
        patch("pathlib.Path.write_text", side_effect=PermissionError),
        patch("taipanstack_bootstrapper._log") as mock_log,
    ):
        taipanstack._create_project_structure(args)
        _ = mock_log


def test_validate_setup_failures(tmp_path, monkeypatch):
    args = argparse.Namespace(dry_run=False, verbose=False, force=False)
    monkeypatch.chdir(tmp_path)
    with (
        patch("shutil.which", return_value="poetry"),
        patch(
            "taipanstack_bootstrapper._run_command",
            return_value=subprocess.CompletedProcess([], 1),
        ),
        patch("taipanstack_bootstrapper._log") as mock_log,
    ):
        taipanstack._validate_setup(args)
        assert any(
            "Issues found during validation" in call[0][0]
            for call in mock_log.call_args_list
        )


def test_check_poetry_installation_not_found(monkeypatch):
    args = argparse.Namespace(dry_run=False, verbose=False, force=False)
    with (
        patch("shutil.which", side_effect=lambda _x: None),
        patch("taipanstack_bootstrapper._handle_error") as mock_error,
    ):
        taipanstack._check_poetry_installation(args)
        mock_error.assert_called_once()
        assert "Poetry not found" in mock_error.call_args[0][0]


def test_check_poetry_installation_not_found_has_pipx(monkeypatch):
    args = argparse.Namespace(dry_run=False, verbose=False, force=False)
    with (
        patch("shutil.which", side_effect=lambda x: x == "pipx"),
        patch("taipanstack_bootstrapper._handle_error") as mock_error,
    ):
        taipanstack._check_poetry_installation(args)
        mock_error.assert_called_once()
        assert "pipx install poetry" in mock_error.call_args[0][0]


def test_initialize_poetry_project_exists(tmp_path, monkeypatch):
    args = argparse.Namespace(dry_run=False, verbose=False, force=False)
    monkeypatch.chdir(tmp_path)
    (tmp_path / "pyproject.toml").write_text("")
    with patch("taipanstack_bootstrapper._log") as mock_log:
        taipanstack._initialize_poetry_project(args)
        mock_log.assert_any_call("✅ Poetry project already initialized.", args)


def test_add_dependencies_uvloop(monkeypatch):
    args = argparse.Namespace(
        dry_run=False, verbose=False, force=False, install_runtime_deps=True
    )
    with (
        patch("taipanstack_bootstrapper._is_windows", return_value=False),
        patch("taipanstack_bootstrapper._run_command") as mock_run,
    ):
        taipanstack._add_dependencies(args)
        assert any("uvloop" in call[0][0] for call in mock_run.call_args_list)


def test_run_command_verbose():
    args = argparse.Namespace(dry_run=False, verbose=True, force=False)
    with (
        patch("subprocess.run", return_value=subprocess.CompletedProcess([], 0)),
        patch("taipanstack_bootstrapper._log") as mock_log,
    ):
        taipanstack._run_command(["cmd"], args)
        mock_log.assert_any_call("Executing command: `cmd`", args, is_verbose=True)


def test_cli():
    with patch("sys.argv", ["taipanstack_bootstrapper.py", "--dry-run", "--verbose"]):
        args = taipanstack._setup_cli()
        assert args.dry_run is True
        assert args.verbose is True


def test_run_command_called_process_error_no_stderr():
    args = argparse.Namespace(dry_run=False, verbose=False)
    err = subprocess.CalledProcessError(1, ["cmd"], stderr=None)
    with (
        patch("subprocess.run", side_effect=err),
        patch("taipanstack_bootstrapper._handle_error") as mock_error,
    ):
        taipanstack._run_command(["cmd"], args)
        mock_error.assert_called_once()
        assert "Error:" not in mock_error.call_args[0][0]


def test_run_command_called_process_error_capture_output():
    args = argparse.Namespace(dry_run=False, verbose=False)
    err = subprocess.CalledProcessError(1, ["cmd"], stderr="some error")
    with (
        patch("subprocess.run", side_effect=err),
        patch("taipanstack_bootstrapper._handle_error") as mock_error,
    ):
        taipanstack._run_command(["cmd"], args, capture_output=True)
        mock_error.assert_called_once()
        assert "some error" not in mock_error.call_args[0][0]


def test_generate_pyproject_config_dry_run_no_config(tmp_path, monkeypatch):
    args = argparse.Namespace(dry_run=True, verbose=True, force=False)
    monkeypatch.chdir(tmp_path)
    toml = tmp_path / "pyproject.toml"
    toml.write_text("[tool.ruff]\n[tool.mypy]\n[tool.pytest.ini_options]\n")
    with patch("taipanstack_bootstrapper._log") as mock_log:
        taipanstack._generate_pyproject_config(args)
        mock_log.assert_any_call(
            "✅ Configurations for Ruff, Mypy, and Pytest already exist in pyproject.toml.",
            args,
        )


def test_create_project_structure_toml_index_error_true(tmp_path, monkeypatch):
    args = argparse.Namespace(dry_run=False, verbose=False, force=False)
    monkeypatch.chdir(tmp_path)
    (tmp_path / "pyproject.toml").write_text("name = ")
    taipanstack._create_project_structure(args)


def test_validate_setup_poetry_fails3(tmp_path, monkeypatch):
    args = argparse.Namespace(dry_run=False, verbose=False, force=False)
    monkeypatch.chdir(tmp_path)
    (tmp_path / "pyproject.toml").write_text("")
    (tmp_path / ".pre-commit-config.yaml").write_text("")
    (tmp_path / "SECURITY.md").write_text("")
    (tmp_path / ".github").mkdir()
    (tmp_path / ".github" / "dependabot.yml").write_text("")
    with (
        patch("shutil.which", return_value="poetry"),
        patch("subprocess.run") as mock_run,
    ):
        mock_run.return_value = subprocess.CompletedProcess(
            ["poetry", "run", "pre-commit", "--version"], 1, "out", "err"
        )
        with patch("taipanstack_bootstrapper._log") as mock_log:
            taipanstack._validate_setup(args)
            assert any(
                "Pre-commit is not installed correctly" in call[0][0]
                for call in mock_log.call_args_list
            )


def test_create_project_structure_read_oserror_true(tmp_path, monkeypatch):
    args = argparse.Namespace(dry_run=False, verbose=False, force=False)
    monkeypatch.chdir(tmp_path)
    (tmp_path / "pyproject.toml").mkdir()
    taipanstack._create_project_structure(args)


def test_validate_setup_poetry_fails_system_exit(tmp_path, monkeypatch):
    args = argparse.Namespace(dry_run=False, verbose=False, force=False)
    monkeypatch.chdir(tmp_path)
    (tmp_path / "pyproject.toml").write_text("")
    (tmp_path / ".pre-commit-config.yaml").write_text("")
    (tmp_path / "SECURITY.md").write_text("")
    (tmp_path / ".github").mkdir()
    (tmp_path / ".github" / "dependabot.yml").write_text("")

    with patch("shutil.which", return_value="poetry"):
        with patch(
            "subprocess.run", side_effect=subprocess.CalledProcessError(1, ["cmd"])
        ):
            with patch("taipanstack_bootstrapper._log") as mock_log:
                taipanstack._validate_setup(args)
                assert any(
                    "Pre-commit is not installed correctly" in call[0][0]
                    for call in mock_log.call_args_list
                )


def test_validate_setup_poetry_not_found(tmp_path, monkeypatch):
    args = argparse.Namespace(dry_run=False, verbose=False, force=False)
    monkeypatch.chdir(tmp_path)
    (tmp_path / "pyproject.toml").write_text("")
    (tmp_path / ".pre-commit-config.yaml").write_text("")
    (tmp_path / "SECURITY.md").write_text("")
    (tmp_path / ".github").mkdir()
    (tmp_path / ".github" / "dependabot.yml").write_text("")

    with patch("shutil.which", return_value=None):
        with patch("taipanstack_bootstrapper._log") as mock_log:
            taipanstack._validate_setup(args)
            assert any(
                "Validation completed successfully!" in call[0][0]
                for call in mock_log.call_args_list
            )


def test_add_dependencies_no_uvloop_windows2(monkeypatch):
    args = argparse.Namespace(
        dry_run=False, verbose=False, force=False, install_runtime_deps=True
    )
    with (
        patch("taipanstack_bootstrapper._is_windows", return_value=True),
        patch("taipanstack_bootstrapper._run_command") as mock_run,
    ):
        taipanstack._add_dependencies(args)
        _ = mock_run


def test_add_dependencies_install_runtime_false_coverage(monkeypatch):
    args = argparse.Namespace(
        dry_run=False, verbose=False, force=False, install_runtime_deps=False
    )
    with patch("taipanstack_bootstrapper._run_command") as mock_run:
        taipanstack._add_dependencies(args)
        _ = mock_run


def test_generate_pyproject_config_write_error2(tmp_path, monkeypatch):
    args = argparse.Namespace(dry_run=False, verbose=False, force=False)
    monkeypatch.chdir(tmp_path)
    # create the file
    (tmp_path / "pyproject.toml").write_text("")

    # We want it to raise OSError when trying to open for *writing*, not reading.
    # The code reads the file first. We must only raise OSError on write mode, or patch the right place.
    # We can patch open but only raise error if mode is 'a'.

    import pathlib

    original_open = pathlib.Path.open

    def mock_open(self, *args, **kwargs):
        if (args and args[0] == "a") or kwargs.get("mode") == "a":
            raise OSError("test write error")
        return original_open(self, *args, **kwargs)

    with patch.object(pathlib.Path, "open", mock_open):
        with patch("taipanstack_bootstrapper._handle_error") as mock_error:
            taipanstack._generate_pyproject_config(args)
            mock_error.assert_called_once()


def test_create_project_structure_mock_pyproject_toml_path_index_error2(
    tmp_path, monkeypatch
):
    args = argparse.Namespace(dry_run=False, verbose=False, force=False)
    monkeypatch.chdir(tmp_path)

    from unittest.mock import MagicMock
    mock_path = MagicMock()
    mock_path.exists.return_value = True
    # simulate the contents "name =" that causes IndexError when parsing
    mock_path.read_text.return_value = "name ="

    with patch("taipanstack_bootstrapper.PYPROJECT_TOML_PATH", mock_path):
        taipanstack._create_project_structure(args)
