"""Tests for configuration generators."""

from pathlib import Path

from taipanstack.config.generators import (
    generate_dependabot_config,
    generate_editorconfig,
    generate_pre_commit_config,
    generate_pyproject_config,
    generate_security_policy,
    write_config_file,
)
from taipanstack.config.models import StackConfig


class TestGeneratePyprojectConfig:
    """Tests for generate_pyproject_config function."""

    def test_generates_ruff_config(self) -> None:
        """Test that Ruff configuration is generated."""
        config = StackConfig(project_name="test-project")
        result = generate_pyproject_config(config)

        assert "[tool.ruff]" in result
        assert "line-length" in result

    def test_generates_mypy_config(self) -> None:
        """Test that Mypy configuration is generated."""
        config = StackConfig(project_name="test-project")
        result = generate_pyproject_config(config)

        assert "[tool.mypy]" in result
        assert "python_version" in result

    def test_generates_pytest_config(self) -> None:
        """Test that Pytest configuration is generated."""
        config = StackConfig(project_name="test-project")
        result = generate_pyproject_config(config)

        assert "[tool.pytest" in result


class TestGeneratePreCommitConfig:
    """Tests for generate_pre_commit_config function."""

    def test_generates_yaml(self) -> None:
        """Test that valid YAML is generated."""
        config = StackConfig(project_name="test-project")
        result = generate_pre_commit_config(config)

        assert "repos:" in result
        assert "hooks:" in result

    def test_includes_ruff_hook(self) -> None:
        """Test that Ruff hook is included."""
        config = StackConfig(project_name="test-project")
        result = generate_pre_commit_config(config)

        assert "ruff" in result.lower()

    def test_includes_mypy_hook(self) -> None:
        """Test that Mypy hook is included."""
        config = StackConfig(project_name="test-project")
        result = generate_pre_commit_config(config)

        assert "mypy" in result.lower()

    def test_bandit_severity_mapping(self) -> None:
        """Test that Bandit severity levels are correctly mapped."""
        for level, expected_arg in [
            ("low", "-lL"),
            ("medium", "-lM"),
            ("high", "-lH"),
        ]:
            config = StackConfig(
                project_name="test-project",
                security={"bandit_severity": level},
            )
            result = generate_pre_commit_config(config)
            assert expected_arg in result

    def test_paranoid_security_hooks_inclusion(self) -> None:
        """Test that paranoid security hooks are included."""
        config = StackConfig(
            project_name="test-project",
            security={"level": "paranoid"},
        )
        result = generate_pre_commit_config(config)

        assert "pip-audit" in result
        assert "vulture" in result
        assert "tryceratops" in result

    def test_security_hooks_toggling(self) -> None:
        """Test that individual security hooks can be disabled."""
        tools = [
            ("enable_bandit", "bandit"),
            ("enable_safety", "safety"),
            ("enable_semgrep", "semgrep"),
            ("enable_detect_secrets", "detect-secrets"),
        ]

        for flag, hook_id in tools:
            # Test enabled (default)
            config_enabled = StackConfig(project_name="test-project")
            result_enabled = generate_pre_commit_config(config_enabled)
            assert hook_id in result_enabled

            # Test disabled
            config_disabled = StackConfig(
                project_name="test-project",
                security={flag: False, "level": "standard"},
            )
            result_disabled = generate_pre_commit_config(config_disabled)
            assert hook_id not in result_disabled


class TestGenerateDependabotConfig:
    """Tests for generate_dependabot_config function."""

    def test_generates_yaml(self) -> None:
        """Test that valid YAML is generated."""
        result = generate_dependabot_config()

        assert "version:" in result
        assert "updates:" in result

    def test_includes_pip_ecosystem(self) -> None:
        """Test that pip ecosystem is included."""
        result = generate_dependabot_config()

        assert "pip" in result

    def test_includes_github_actions(self) -> None:
        """Test that GitHub Actions is included."""
        result = generate_dependabot_config()

        assert "github-actions" in result


class TestGenerateSecurityPolicy:
    """Tests for generate_security_policy function."""

    def test_generates_markdown(self) -> None:
        """Test that Markdown is generated."""
        result = generate_security_policy()

        assert "# Security Policy" in result

    def test_includes_reporting_instructions(self) -> None:
        """Test that reporting instructions are included."""
        result = generate_security_policy()

        assert "report" in result.lower() or "vulnerabilit" in result.lower()

    def test_includes_supported_versions(self) -> None:
        """Test that supported versions section exists."""
        result = generate_security_policy()

        assert "version" in result.lower()


class TestGenerateEditorconfig:
    """Tests for generate_editorconfig function."""

    def test_generates_editorconfig(self) -> None:
        """Test that valid EditorConfig is generated."""
        result = generate_editorconfig()

        assert "root = true" in result

    def test_includes_python_settings(self) -> None:
        """Test that Python settings are included."""
        result = generate_editorconfig()

        assert "*.py" in result or "[*.py]" in result

    def test_includes_indent_settings(self) -> None:
        """Test that indentation settings are included."""
        result = generate_editorconfig()

        assert "indent_" in result


class TestWriteConfigFile:
    """Tests for write_config_file function."""

    def test_writes_file(self, tmp_path: Path) -> None:
        """Test that file is written."""
        config = StackConfig(project_name="test-project", dry_run=False)
        file_path = tmp_path / "test.txt"

        result = write_config_file(file_path, "test content", config)

        assert result is True
        assert file_path.exists()
        assert file_path.read_text() == "test content"

    def test_dry_run_does_not_write(self, tmp_path: Path) -> None:
        """Test that dry_run mode doesn't write."""
        config = StackConfig(project_name="test-project", dry_run=True)
        file_path = tmp_path / "test.txt"

        result = write_config_file(file_path, "test content", config)

        assert result is False
        assert not file_path.exists()

    def test_overwrites_existing_file(self, tmp_path: Path) -> None:
        """Test that existing file is overwritten."""
        config = StackConfig(project_name="test-project", dry_run=False, force=True)
        file_path = tmp_path / "test.txt"
        file_path.write_text("original")

        write_config_file(file_path, "new content", config)

        assert file_path.read_text() == "new content"

    def test_creates_backup_without_force(self, tmp_path: Path) -> None:
        """Test that backup is created when not using force mode."""
        config = StackConfig(project_name="test-project", dry_run=False, force=False)
        file_path = tmp_path / "test.txt"
        file_path.write_text("original")

        write_config_file(file_path, "new content", config)

        assert file_path.read_text() == "new content"
        backup_path = tmp_path / "test.txt.bak"
        assert backup_path.exists()
        assert backup_path.read_text() == "original"


class TestConfigGeneratorsBranches:
    """Tests for config/generators.py branch coverage."""

    def test_generate_pre_commit_without_bandit(self) -> None:
        """Test pre-commit config without bandit enabled."""
        from taipanstack.config.generators import generate_pre_commit_config
        from taipanstack.config.models import SecurityConfig, StackConfig

        config = StackConfig(
            project_name="testproj",
            security=SecurityConfig(
                enable_bandit=False,
                enable_safety=False,
                enable_semgrep=False,
                enable_detect_secrets=False,
            ),
        )
        result = generate_pre_commit_config(config)
        assert "bandit" not in result

    def test_generate_pre_commit_with_safety_only(self) -> None:
        """Test pre-commit config with safety only."""
        from taipanstack.config.generators import generate_pre_commit_config
        from taipanstack.config.models import SecurityConfig, StackConfig

        config = StackConfig(
            project_name="testproj",
            security=SecurityConfig(
                enable_bandit=False,
                enable_safety=True,
                enable_semgrep=False,
                enable_detect_secrets=False,
            ),
        )
        result = generate_pre_commit_config(config)
        assert "safety" in result
        assert "bandit" not in result

    def test_generate_pre_commit_with_semgrep_only(self) -> None:
        """Test pre-commit config with semgrep only."""
        from taipanstack.config.generators import generate_pre_commit_config
        from taipanstack.config.models import SecurityConfig, StackConfig

        config = StackConfig(
            project_name="testproj",
            security=SecurityConfig(
                enable_bandit=False,
                enable_safety=False,
                enable_semgrep=True,
                enable_detect_secrets=False,
            ),
        )
        result = generate_pre_commit_config(config)
        assert "semgrep" in result

    def test_generate_pre_commit_with_detect_secrets_only(self) -> None:
        """Test pre-commit config with detect-secrets only."""
        from taipanstack.config.generators import generate_pre_commit_config
        from taipanstack.config.models import SecurityConfig, StackConfig

        config = StackConfig(
            project_name="testproj",
            security=SecurityConfig(
                enable_bandit=False,
                enable_safety=False,
                enable_semgrep=False,
                enable_detect_secrets=True,
            ),
        )
        result = generate_pre_commit_config(config)
        assert "detect-secrets" in result


class TestGeneratorsBranches:
    """Tests for generators branches."""

    def test_generate_pre_commit_basic(self) -> None:
        """Test generate_pre_commit_config function."""
        from taipanstack.config.generators import generate_pre_commit_config
        from taipanstack.config.models import StackConfig

        config = StackConfig(project_name="testproject")

        precommit = generate_pre_commit_config(config)
        assert "ruff" in precommit
        assert "repos:" in precommit


class TestGenerators100Percent:
    """Tests to reach 100% for generators."""

    def test_write_config_file_dry_run(self, tmp_path: Path) -> None:
        """Test write_config_file in dry_run mode."""
        from taipanstack.config.generators import write_config_file
        from taipanstack.config.models import StackConfig

        config = StackConfig(project_name="test", dry_run=True)
        target = tmp_path / "test.toml"

        result = write_config_file(target, "content", config)
        assert result is False  # Dry run returns False

    def test_write_config_file_force(self, tmp_path: Path) -> None:
        """Test write_config_file with force=True overwrites."""
        from taipanstack.config.generators import write_config_file
        from taipanstack.config.models import StackConfig

        config = StackConfig(project_name="test", force=True)
        target = tmp_path / "test.toml"
        target.write_text("old content")

        result = write_config_file(target, "new content", config)
        assert result is True
        assert target.read_text() == "new content"


class TestGeneratorsParanoidLevel:
    """Test for generators.py line 165 (paranoid security level)."""

    def test_pre_commit_config_paranoid_level(self) -> None:
        """Test generate_pre_commit_config with paranoid security level."""
        from taipanstack.config.generators import generate_pre_commit_config
        from taipanstack.config.models import SecurityConfig, StackConfig

        config = StackConfig(
            project_name="test-project",
            python_version="3.12",
            security=SecurityConfig(
                level="paranoid",
                enable_bandit=True,
                enable_safety=True,
                enable_semgrep=True,
                enable_detect_secrets=True,
            ),
        )

        result = generate_pre_commit_config(config)

        # Paranoid level should include pip-audit, vulture, tryceratops
        assert "pip-audit" in result
        assert "vulture" in result
        assert "tryceratops" in result
        assert "bandit" in result
        assert "safety" in result
        assert "semgrep" in result
        assert "detect-secrets" in result
