import pytest


def test_utils_subprocess_additional_utils_subprocess_raise_on_error():
    import subprocess

    from taipanstack.utils.subprocess import SafeCommandResult

    res = SafeCommandResult(
        command=["ls"], returncode=1, stdout="", stderr="", duration_seconds=1.0
    )

    with pytest.raises(subprocess.CalledProcessError):
        res.raise_on_error()
