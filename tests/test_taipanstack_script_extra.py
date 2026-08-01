import argparse
import subprocess
from unittest.mock import patch

import pytest
import taipanstack_bootstrapper as taipanstack


def test_taipanstack_script_extra_handle_error(capsys):
    with pytest.raises(SystemExit) as exc:
        taipanstack._handle_error("Test error")
    assert exc.value.code == 1
    captured = capsys.readouterr()
    assert "Error: Test error\n" in captured.err


def test_taipanstack_script_extra_run_command_file_not_found_expected():
    args = argparse.Namespace(dry_run=False, verbose=False)
    with (
        patch("subprocess.run", side_effect=FileNotFoundError),
        patch("taipanstack_bootstrapper._handle_error") as mock_error,
    ):
        taipanstack._run_command(["notacommand"], args)
        mock_error.assert_called_once()
        assert "not found" in mock_error.call_args[0][0]


def test_taipanstack_script_extra_run_command_called_process_error():
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


def test_taipanstack_script_extra_safe_write_rename_error(tmp_path):
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


def test_taipanstack_script_extra_safe_write_write_error(tmp_path):
    args = argparse.Namespace(dry_run=False, verbose=False, force=False)
    file_path = tmp_path / "test.txt"
    with (
        patch("pathlib.Path.write_text", side_effect=PermissionError),
        patch("taipanstack_bootstrapper._handle_error") as mock_error,
    ):
        taipanstack._safe_write(file_path, "new", args)
        mock_error.assert_called_once()
        assert "Could not write to file" in mock_error.call_args[0][0]


def test_taipanstack_script_extra_generate_pyproject_config_dry_run_with_config_expected(
    tmp_path, monkeypatch
):
    args = argparse.Namespace(dry_run=True, verbose=True, force=False)
    monkeypatch.chdir(tmp_path)
    with patch("taipanstack_bootstrapper._log") as mock_log:
        taipanstack._generate_pyproject_config(args)
        mock_log.assert_any_call(
            "Would add tool configurations to pyproject.toml", args, is_verbose=True
        )
