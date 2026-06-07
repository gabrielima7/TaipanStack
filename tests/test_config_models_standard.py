"""Tests for stack.config.models module."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from taipanstack.config.models import (
    DependencyConfig,
    LoggingConfig,
    SecurityConfig,
    StackConfig,
)


class TestSecurityConfig:
    """Tests for SecurityConfig model."""

    def test_config_models_default_values_standard_expected(self) -> None:
        """Test default security configuration."""
        config = SecurityConfig()

        assert config.level == "strict"
        assert config.enable_bandit is True
        assert config.enable_pip_audit is True
        assert config.enable_semgrep is True
        assert config.enable_detect_secrets is True
        assert config.bandit_severity == "low"

    def test_config_models_paranoid_level_standard_expected(self) -> None:
        """Test paranoid security level."""
        config = SecurityConfig(level="paranoid")
        assert config.level == "paranoid"

    def test_config_models_frozen_config_standard_expected(self) -> None:
        """Test that config is immutable."""
        config = SecurityConfig()
        with pytest.raises(ValidationError):
            config.level = "standard"  # type: ignore[misc]

    def test_config_models_extra_fields_forbidden_standard_expected(self) -> None:
        """Test that extra fields are not allowed."""
        with pytest.raises(ValidationError):
            SecurityConfig(invalid_field="value")  # type: ignore[call-arg]


class TestDependencyConfig:
    """Tests for DependencyConfig model."""

    def test_config_models_default_values_standard_expected(self) -> None:
        """Test default dependency configuration."""
        config = DependencyConfig()

        assert config.install_runtime_deps is False
        assert config.install_dev_deps is True
        assert "ruff" in config.dev_dependencies
        assert "pytest" in config.dev_dependencies

    def test_config_models_custom_dependencies_standard_expected(self) -> None:
        """Test custom dependencies."""
        config = DependencyConfig(
            dev_dependencies=["pytest", "mypy"],
            runtime_dependencies=["fastapi"],
        )

        assert config.dev_dependencies == ["pytest", "mypy"]
        assert config.runtime_dependencies == ["fastapi"]


class TestLoggingConfig:
    """Tests for LoggingConfig model."""

    def test_config_models_default_values_standard_expected(self) -> None:
        """Test default logging configuration."""
        config = LoggingConfig()

        assert config.level == "INFO"
        assert config.format == "detailed"
        assert config.enable_structured is False

    def test_config_models_valid_levels_standard_expected(self) -> None:
        """Test all valid log levels."""
        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            config = LoggingConfig(level=level)  # type: ignore[arg-type]
            assert config.level == level

    def test_config_models_invalid_level_rejected_standard_expected(self) -> None:
        """Test invalid log level is rejected."""
        with pytest.raises(ValidationError):
            LoggingConfig(level="INVALID")  # type: ignore[arg-type]


class TestStackConfig:
    """Tests for StackConfig model."""

    def test_config_models_default_values_standard_expected(self) -> None:
        """Test default stack configuration."""
        config = StackConfig()

        assert config.project_name == "my_project"
        assert config.dry_run is False
        assert config.force is False
        assert config.verbose is False
        assert isinstance(config.security, SecurityConfig)
        assert isinstance(config.dependencies, DependencyConfig)
        assert isinstance(config.logging, LoggingConfig)

    def test_config_models_valid_project_name_standard_expected(self) -> None:
        """Test valid project names."""
        config = StackConfig(project_name="my_awesome_project")
        assert config.project_name == "my_awesome_project"

    def test_config_models_invalid_project_name_rejected_standard_expected(self) -> None:
        """Test invalid project names are rejected."""
        with pytest.raises(ValidationError, match="invalid"):
            StackConfig(project_name="123invalid")

        with pytest.raises(ValidationError, match="invalid"):
            StackConfig(project_name="has spaces")

    def test_config_models_valid_python_version_standard_expected(self) -> None:
        """Test valid Python versions."""
        config = StackConfig(python_version="3.11")
        assert config.python_version == "3.11"

    def test_config_models_invalid_python_version_rejected_standard_expected(self) -> None:
        """Test invalid Python versions are rejected."""
        with pytest.raises(ValidationError):
            StackConfig(python_version="2.7")

        with pytest.raises(ValidationError, match="invalid"):
            StackConfig(python_version="invalid")

    def test_config_models_valid_project_dir_standard_expected(self, tmp_path: Path) -> None:
        """Test valid project directory is resolved."""
        config = StackConfig(project_dir=tmp_path)
        assert config.project_dir == tmp_path.resolve()

    def test_config_models_path_traversal_rejected_standard_expected(self, tmp_path: Path) -> None:
        """Test path traversal in project_dir is rejected."""
        with pytest.raises(ValidationError, match="Path traversal"):
            StackConfig(project_dir=Path("../../../etc"))

    def test_config_models_absolute_path_accepted_standard_expected(self, tmp_path: Path) -> None:
        """Test absolute path is accepted and resolved."""
        abs_path = tmp_path.resolve()
        config = StackConfig(project_dir=abs_path)
        assert config.project_dir == abs_path

    def test_config_models_path_with_dots_not_traversal_accepted_standard_expected(
        self, tmp_path: Path
    ) -> None:
        """Test paths with dots that are not traversal are accepted."""
        dot_path = tmp_path / "my.project.dir"
        config = StackConfig(project_dir=dot_path)
        assert config.project_dir == dot_path.resolve()

    def test_config_models_non_existent_path_accepted_standard_expected(self, tmp_path: Path) -> None:
        """Test non-existent path is accepted (resolve handles it)."""
        non_existent = tmp_path / "new_project_dir"
        config = StackConfig(project_dir=non_existent)
        assert config.project_dir == non_existent.resolve()

    def test_config_models_direct_validate_project_dir_call_standard_expected(self) -> None:
        """Test direct call to validate_project_dir classmethod."""
        test_path = Path("some/path")
        resolved = StackConfig.validate_project_dir(test_path)
        assert resolved == test_path.resolve()

    def test_config_models_validate_project_dir_traversal_direct_call_standard_expected(
        self,
    ) -> None:
        """Test direct call to validate_project_dir with traversal."""
        with pytest.raises(ValueError, match="Path traversal"):
            StackConfig.validate_project_dir(Path("safe/../unsafe"))

    def test_config_models_path_with_double_dots_in_name_rejected_standard_expected(
        self,
    ) -> None:
        """Test that paths with '..' in the name are currently rejected.

        Note: This is current behavior due to simple string check.
        """
        with pytest.raises(ValidationError, match="Path traversal"):
            StackConfig(project_dir=Path("dir_with..dots"))

    def test_config_models_paranoid_requires_all_tools_standard_expected(self) -> None:
        """Test paranoid mode requires all security tools."""
        with pytest.raises(ValidationError, match="requires all security tools"):
            StackConfig(
                security=SecurityConfig(
                    level="paranoid",
                    enable_bandit=False,
                )
            )

    def test_config_models_to_target_version_standard_expected(self) -> None:
        """Test target version conversion."""
        config = StackConfig(python_version="3.12")
        assert config.to_target_version() == "py312"

    def test_config_models_nested_configs_standard_expected(self) -> None:
        """Test nested configuration objects."""
        config = StackConfig(
            security=SecurityConfig(level="paranoid"),
            logging=LoggingConfig(level="DEBUG"),
        )

        assert config.security.level == "paranoid"
        assert config.logging.level == "DEBUG"

    def test_config_models_invalid_python_version_too_old_standard_expected(self) -> None:
        """Test that a Python version older than supported is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            StackConfig(python_version="3.9")

        assert "not supported" in str(exc_info.value)
