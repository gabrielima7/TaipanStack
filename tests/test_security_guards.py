"""Tests for stack.security.guards module."""

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from stack.security.guards import (
    SecurityError,
    guard_command_injection,
    guard_file_extension,
    guard_path_traversal,
)


class TestGuardPathTraversal:
    """Tests for guard_path_traversal function."""

    def test_safe_path_passes(self, tmp_path: Path) -> None:
        """Test that safe paths pass validation."""
        safe_file = tmp_path / "test.txt"
        safe_file.touch()

        result = guard_path_traversal(safe_file, tmp_path)
        assert result == safe_file.resolve()

    def test_relative_path_within_base(self, tmp_path: Path) -> None:
        """Test that relative paths within base dir pass."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        test_file = subdir / "test.txt"
        test_file.touch()

        result = guard_path_traversal(Path("subdir/test.txt"), tmp_path)
        assert result == test_file.resolve()

    def test_path_traversal_blocked(self, tmp_path: Path) -> None:
        """Test that path traversal attempts are blocked."""
        with pytest.raises(SecurityError) as exc_info:
            guard_path_traversal("../etc/passwd", tmp_path)

        assert "path_traversal" in str(exc_info.value)
        assert exc_info.value.guard_name == "path_traversal"

    def test_double_dot_blocked(self, tmp_path: Path) -> None:
        """Test that .. patterns are blocked."""
        with pytest.raises(SecurityError):
            guard_path_traversal("foo/../../../etc/passwd", tmp_path)

    def test_url_encoded_traversal_blocked(self, tmp_path: Path) -> None:
        """Test that URL encoded traversal is blocked."""
        with pytest.raises(SecurityError):
            guard_path_traversal("%2e%2e/etc/passwd", tmp_path)

    def test_path_escapes_base_dir(self, tmp_path: Path) -> None:
        """Test that paths escaping base dir are blocked."""
        with TemporaryDirectory() as other_dir:
            with pytest.raises(SecurityError) as exc_info:
                guard_path_traversal(Path(other_dir), tmp_path)
            assert "escapes base directory" in str(exc_info.value)


class TestGuardCommandInjection:
    """Tests for guard_command_injection function."""

    def test_safe_command_passes(self) -> None:
        """Test that safe commands pass validation."""
        cmd = ["python", "-m", "pytest", "-v"]
        result = guard_command_injection(cmd)
        assert result == cmd

    def test_empty_command_blocked(self) -> None:
        """Test that empty commands are blocked."""
        with pytest.raises(SecurityError) as exc_info:
            guard_command_injection([])
        assert "Empty command" in str(exc_info.value)

    def test_semicolon_blocked(self) -> None:
        """Test that semicolons are blocked."""
        with pytest.raises(SecurityError):
            guard_command_injection(["echo", "hello; rm -rf /"])

    def test_pipe_blocked(self) -> None:
        """Test that pipe characters are blocked."""
        with pytest.raises(SecurityError):
            guard_command_injection(["cat", "file | rm -rf /"])

    def test_backtick_blocked(self) -> None:
        """Test that backticks are blocked."""
        with pytest.raises(SecurityError):
            guard_command_injection(["echo", "`whoami`"])

    def test_dollar_expansion_blocked(self) -> None:
        """Test that dollar expansion is blocked."""
        with pytest.raises(SecurityError):
            guard_command_injection(["echo", "$(whoami)"])

    def test_allowed_commands_whitelist(self) -> None:
        """Test command whitelist functionality."""
        cmd = ["python", "-c", "print('hello')"]
        result = guard_command_injection(cmd, allowed_commands=["python"])
        assert result == cmd

    def test_command_not_in_whitelist_blocked(self) -> None:
        """Test that commands not in whitelist are blocked."""
        with pytest.raises(SecurityError) as exc_info:
            guard_command_injection(["rm", "-rf", "/"], allowed_commands=["python"])
        assert "not in allowed list" in str(exc_info.value)


class TestGuardFileExtension:
    """Tests for guard_file_extension function."""

    def test_safe_extension_passes(self) -> None:
        """Test that safe extensions pass."""
        result = guard_file_extension("script.py", allowed_extensions=["py", "txt"])
        assert result == Path("script.py")

    def test_dangerous_extension_blocked(self) -> None:
        """Test that dangerous extensions are blocked."""
        with pytest.raises(SecurityError) as exc_info:
            guard_file_extension("evil.exe")
        assert "not allowed" in str(exc_info.value)

    def test_custom_denied_extensions(self) -> None:
        """Test custom denied extensions."""
        with pytest.raises(SecurityError):
            guard_file_extension("config.yaml", denied_extensions=["yaml", "yml"])

    def test_extension_with_dot(self) -> None:
        """Test that extensions with dots are handled."""
        result = guard_file_extension("file.txt", allowed_extensions=[".txt"])
        assert result == Path("file.txt")
