"""Tests for configuration generators."""

from taipanstack.config.generators import (
    generate_pyproject_config,
    generate_security_policy,
)
from taipanstack.config.models import StackConfig


class TestGeneratePyprojectConfig:
    """Tests for generate_pyproject_config function."""

    def test_generates_ruff_config_expected(self) -> None:
        """Test that Ruff configuration is generated."""
        config = StackConfig(project_name="test-project")
        result = generate_pyproject_config(config)
        assert "[tool.ruff]" in result
        assert "line-length" in result

    def test_generates_mypy_config_expected(self) -> None:
        """Test that Mypy configuration is generated."""
        config = StackConfig(project_name="test-project")
        result = generate_pyproject_config(config)
        assert "[tool.mypy]" in result
        assert "python_version" in result

    def test_generates_pytest_config_expected(self) -> None:
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

    def test_includes_reporting_instructions_expected(self) -> None:
        """Test that reporting instructions are included."""
        result = generate_security_policy()
        assert "report" in result.lower() or "vulnerabilit" in result.lower()

    def test_includes_supported_versions_expected(self) -> None:
        """Test that supported versions section exists."""
        result = generate_security_policy()
        assert "version" in result.lower()
