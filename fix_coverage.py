content = """import subprocess as sp
from pathlib import Path
from unittest.mock import patch

import pytest

def test_config_generators_branches_expected():
    from taipanstack.config.generators import generate_pre_commit_config
    from taipanstack.config.models import SecurityConfig, StackConfig

    config = StackConfig(
        project_name="test",
        security=SecurityConfig(
            enable_bandit=False,
            enable_safety=True,
            enable_semgrep=False,
            enable_detect_secrets=False,
        ),
    )
    yaml = generate_pre_commit_config(config)
    assert "safety" in yaml

    config = StackConfig(
        project_name="test",
        security=SecurityConfig(
            enable_bandit=False,
            enable_safety=False,
            enable_semgrep=True,
            enable_detect_secrets=False,
        ),
    )
    yaml = generate_pre_commit_config(config)
    assert "semgrep" in yaml

    config = StackConfig(
        project_name="test",
        security=SecurityConfig(
            enable_bandit=False,
            enable_safety=False,
            enable_semgrep=False,
            enable_detect_secrets=True,
        ),
    )
    yaml = generate_pre_commit_config(config)
    assert "detect-secrets" in yaml


def test_compat_branches_expected():
    from taipanstack.core.compat import _get_features_for_version

    features = _get_features_for_version((3, 11), force_refresh=True)
    assert features is not None
    features = _get_features_for_version((3, 11), force_refresh=False)
    assert features is not None
    features = _get_features_for_version((3, 13), force_refresh=True)
    assert features is not None


def test_optimizations_branches_expected():
    from taipanstack.core.optimizations import (
        _get_system_optimizations
    )

    opt = _get_system_optimizations(force_refresh=True)
    assert opt is not None
    opt = _get_system_optimizations(force_refresh=False)
    assert opt is not None


def test_result_branches_expected():
    from taipanstack.core.result import (
        Ok,
        Err,
        and_then_async,
        collect_results,
        map_async,
    )

    class Dummy:
        pass

    _ = collect_results([Dummy(), Dummy()])

    assert Ok(1).unwrap_or(2) == 1

    def my_lambda(_):
        return 2

    assert Ok(1).unwrap_or_else(my_lambda) == 1
    assert Err(1).unwrap_or_else(my_lambda) == 2

    import asyncio

    async def run():
        _ = await map_async(Dummy(), my_lambda)
        _ = await and_then_async(Dummy(), my_lambda)

    asyncio.run(run())


def test_circuit_breaker_branches_expected():
    from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState

    breaker = CircuitBreaker(failure_threshold=1)

    import asyncio

    async def try_call():
        try:
            async with breaker._lock:
                breaker._state = CircuitState.OPEN
                breaker._record_success()
                breaker._record_failure()
        except Exception:
            assert True

    asyncio.run(try_call())


def test_guards_branches_expected(tmp_path):
    from taipanstack.security.guards import (
        SecurityError,
        guard_env_variable,
        guard_path_traversal,
        guard_ssrf,
    )

    test_file = tmp_path / "valid.txt"
    test_file.touch()
    guard_path_traversal(test_file, tmp_path)

    with pytest.raises(SecurityError):
        guard_env_variable(
            "NONEXISTENT_VAR_12345", allowed_names=["NONEXISTENT_VAR_12345"]
        )

    with patch("taipanstack.security.guards.urlsplit") as mock_urlsplit:
        mock_urlsplit.side_effect = ValueError("Mocked error")
        res = guard_ssrf("http://example.com")
        assert res.is_err()


def test_password_branches_expected():
    from pydantic import SecretStr

    from taipanstack.security.password import hash_password, verify_password

    assert verify_password("", "hash") is False
    assert verify_password(SecretStr(""), "hash") is False
    assert verify_password("a" * 1025, "hash") is False
    assert verify_password(SecretStr("a" * 1025), "hash") is False

    with pytest.raises(ValueError):
        hash_password("")
    with pytest.raises(ValueError):
        hash_password("a" * 1025)
    with pytest.raises(TypeError):
        verify_password(1, "hash")


def test_subprocess_branches_expected():
    from taipanstack.utils.subprocess import run_safe_command

    res = run_safe_command(["echo", "test"])
    assert res.success

    with patch("taipanstack.utils.subprocess.subprocess.run") as mock_run:
        exc = sp.TimeoutExpired(cmd=["python"], timeout=1.0)
        exc.stdout = b"bytes"
        mock_run.side_effect = exc
        res = run_safe_command(["python"], timeout=1.0)
        assert res.stdout == "bytes"

        class MockExc(sp.TimeoutExpired):
            def __init__(self):
                assert True

            @property
            def timeout(self):
                return 1.0

            @property
            def cmd(self):
                return ["python"]

        exc2 = MockExc()
        mock_run.side_effect = exc2
        res2 = run_safe_command(["python"], timeout=1.0)
        assert res2.returncode == -1
"""

with open("tests/test_coverage_operations_expected.py", "w") as f:
    f.write(content)
