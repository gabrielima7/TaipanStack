import pytest


def test_utils_subprocess_additional_utils_subprocess_raise_on_error():
    import subprocess

    from taipanstack.utils.subprocess import SafeCommandResult

    res = SafeCommandResult(
        command=["ls"], returncode=1, stdout="", stderr="", duration_seconds=1.0
    )

    with pytest.raises(subprocess.CalledProcessError):
        res.raise_on_error()


def test_utils_subprocess_additional_allowed_keys_custom_expected():
    from taipanstack.utils.subprocess import _get_allowed_keys

    assert _get_allowed_keys(["TEST_VAR"]) == {"TEST_VAR"}


def test_utils_subprocess_additional_filter_environment_empty_expected():
    from taipanstack.utils.subprocess import _filter_environment

    assert _filter_environment(None, []) == {}


def test_utils_subprocess_additional_run_safe_command_check_true_expected():
    import subprocess

    import pytest

    from taipanstack.utils.subprocess import run_safe_command

    with pytest.raises(subprocess.CalledProcessError):
        run_safe_command(["false"], check=True, allowed_commands=["false"])


def test_utils_subprocess_additional_filter_environment_empty_allowed_expected():
    from taipanstack.utils.subprocess import _filter_environment

    assert _filter_environment({"PATH": "/bin"}, []) == {}


def test_utils_subprocess_additional_filter_environment_none_allowed_expected():
    from taipanstack.utils.subprocess import _filter_environment

    assert _filter_environment({"PATH": "/bin", "OTHER": "val"}, None) == {
        "PATH": "/bin"
    }


def test_utils_subprocess_additional_run_safe_command_timeout_expected():
    import pytest

    from taipanstack.utils.subprocess import run_safe_command

    with pytest.raises(ValueError):
        run_safe_command(["echo", "hello"], timeout=-1)


def test_utils_subprocess_additional_execute_command_capture_false_expected():
    from unittest.mock import patch

    from taipanstack.utils.subprocess import _execute_command

    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = None
        mock_run.return_value.stderr = None
        result = _execute_command(["echo", "hello"], None, 1.0, False, {})
        assert result.returncode == 0
        assert result.stdout == ""
        assert result.stderr == ""


def test_utils_subprocess_additional_get_allowed_keys_none_expected():
    from taipanstack.utils.subprocess import _get_allowed_keys

    assert _get_allowed_keys(None) == {"PATH"}


def test_utils_subprocess_additional_extract_timeout_stdout_not_str_expected():
    import subprocess

    from taipanstack.utils.subprocess import _extract_timeout_stdout

    err = subprocess.TimeoutExpired(["sleep", "10"], 1.0)
    err.stdout = b"some bytes"
    assert _extract_timeout_stdout(err) == "some bytes"


def test_utils_subprocess_additional_utils_subprocess_validate_timeout_type_error() -> None:
    """Test _validate_timeout with invalid types."""
    from taipanstack.utils.subprocess import _validate_timeout

    with pytest.raises(TypeError, match="timeout must be a finite non-negative number"):
        _validate_timeout("10")  # type: ignore


def test_utils_subprocess_additional_utils_subprocess_validate_timeout_none_expected() -> None:
    """Test _validate_timeout with None."""
    from taipanstack.utils.subprocess import _validate_timeout

    # Should not raise
    _validate_timeout(None)  # type: ignore
