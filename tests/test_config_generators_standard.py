"""Tests for configuration generators."""

from taipanstack.config.generators import (
    generate_pre_commit_config,
    generate_pyproject_config,
    generate_security_policy,
)
from taipanstack.config.models import SecurityConfig, StackConfig


class TestGeneratePyprojectConfig:
    """Tests for generate_pyproject_config function."""

    def test_config_generators_generates_ruff_config_expected(self) -> None:
        """Test that Ruff configuration is generated."""
        config = StackConfig(project_name="test-project")
        result = generate_pyproject_config(config)

        assert "[tool.ruff]" in result
        assert "line-length" in result

    def test_config_generators_generates_mypy_config_expected(self) -> None:
        """Test that Mypy configuration is generated."""
        config = StackConfig(project_name="test-project")
        result = generate_pyproject_config(config)

        assert "[tool.mypy]" in result
        assert "python_version" in result

    def test_config_generators_generates_pytest_config_expected(self) -> None:
        """Test that Pytest configuration is generated."""
        config = StackConfig(project_name="test-project")
        result = generate_pyproject_config(config)

        assert "[tool.pytest" in result


class TestGenerateSecurityPolicy:
    """Tests for generate_security_policy function."""

    def test_config_generators_generates_markdown_expected(self) -> None:
        """Test that Markdown is generated."""
        result = generate_security_policy()

        assert "# Security Policy" in result

    def test_config_generators_includes_reporting_instructions_expected(self) -> None:
        """Test that reporting instructions are included."""
        result = generate_security_policy()

        assert "report" in result.lower() or "vulnerabilit" in result.lower()

    def test_config_generators_includes_supported_versions_expected(self) -> None:
        """Test that supported versions section exists."""
        result = generate_security_policy()

        assert "version" in result.lower()


class TestGeneratePreCommitConfig:
    """Tests for generate_pre_commit_config."""

    def test_config_generators_pre_commit_all_security_hooks(self) -> None:
        """Test with all security hooks enabled."""
        config = StackConfig(
            project_name="test-project",
            security=SecurityConfig(
                level="strict",
                enable_bandit=True,
                bandit_severity="high",
                enable_pip_audit=True,
                enable_semgrep=True,
                enable_detect_secrets=True,
            ),
        )
        result = generate_pre_commit_config(config)
        assert "repo: https://github.com/PyCQA/bandit" in result
        assert "-lH" in result
        assert "repo: https://github.com/pypa/pip-audit" in result
        assert "repo: https://github.com/semgrep/pre-commit" in result
        assert "repo: https://github.com/Yelp/detect-secrets" in result
        assert "repo: https://github.com/trailofbits/pip-audit" not in result

    def test_config_generators_pre_commit_paranoid_expected(self) -> None:
        """Test paranoid mode adds extra hooks."""
        config = StackConfig(
            project_name="test-project",
            security=SecurityConfig(
                level="paranoid",
            ),
        )
        result = generate_pre_commit_config(config)
        assert "repo: https://github.com/trailofbits/pip-audit" in result
        assert "repo: https://github.com/jendrikseipp/vulture" in result
        assert "repo: https://github.com/guilatrova/tryceratops" in result

    def test_config_generators_pre_commit_no_security_hooks(self) -> None:
        """Test with no security hooks enabled."""
        config = StackConfig(
            project_name="test-project",
            security=SecurityConfig(
                level="standard",
                enable_bandit=False,
                enable_pip_audit=False,
                enable_semgrep=False,
                enable_detect_secrets=False,
            ),
        )
        result = generate_pre_commit_config(config)
        assert "repo: https://github.com/PyCQA/bandit" not in result
        assert "repo: https://github.com/pypa/pip-audit" not in result
        assert "repo: https://github.com/semgrep/pre-commit" not in result
        assert "repo: https://github.com/Yelp/detect-secrets" not in result
