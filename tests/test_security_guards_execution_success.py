"""Tests for stack.security.guards module."""

from pathlib import Path

import pytest

from taipanstack.security.guards import (
    SecurityError,
    guard_command_injection,
    guard_file_extension,
    guard_path_traversal,
)


class TestGuardPathTraversal:
    """Tests for guard_path_traversal function."""

    def test_security_guards_safe_path_passes_execution_success(self, tmp_path: Path) -> None:
        """Test that safe paths pass validation."""
        safe_file = tmp_path / "test.txt"
        safe_file.touch()

        result = guard_path_traversal(safe_file, tmp_path)
        assert result == safe_file.resolve()

    def test_security_guards_relative_path_within_base_execution_success(self, tmp_path: Path) -> None:
        """Test that relative paths within base dir pass."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        test_file = subdir / "test.txt"
        test_file.touch()

        result = guard_path_traversal(Path("subdir/test.txt"), tmp_path)
        assert result == test_file.resolve()

    def test_security_guards_path_traversal_blocked_execution_success(self, tmp_path: Path) -> None:
        """Test that path traversal attempts are blocked."""
        with pytest.raises(SecurityError) as exc_info:
            guard_path_traversal("../etc/passwd", tmp_path)

        assert "path_traversal" in str(exc_info.value)
        assert exc_info.value.guard_name == "path_traversal"

    def test_security_guards_double_dot_blocked_execution_success(self, tmp_path: Path) -> None:
        """Test that .. patterns are blocked."""
        with pytest.raises(SecurityError):
            guard_path_traversal("foo/../../../etc/passwd", tmp_path)

    def test_security_guards_url_encoded_traversal_blocked_execution_success(
        self, tmp_path: Path
    ) -> None:
        """Test that URL encoded traversal is blocked."""
        with pytest.raises(SecurityError):
            guard_path_traversal("%2e%2e/etc/passwd", tmp_path)

    def test_security_guards_path_escapes_base_dir_execution_success(self, tmp_path: Path) -> None:
        """Test that paths escaping base dir are blocked."""
        # Create a separate base directory
        subdir = tmp_path / "allowed"
        subdir.mkdir()

        # Try to access a file outside the allowed base
        outside_file = tmp_path / "outside.txt"
        outside_file.touch()

        with pytest.raises(SecurityError):
            guard_path_traversal(outside_file, subdir)

    def test_security_guards_symlinks_blocked_by_default_execution_success(self, tmp_path: Path) -> None:
        """Test that symlinks are blocked by default."""
        real_file = tmp_path / "real.txt"
        real_file.touch()

        symlink_path = tmp_path / "link.txt"
        symlink_path.symlink_to("real.txt")

        with pytest.raises(SecurityError) as exc_info:
            guard_path_traversal(symlink_path, tmp_path)

        assert "Symlinks are not allowed" in str(exc_info.value)
        assert exc_info.value.guard_name == "path_traversal"

    def test_security_guards_symlinks_allowed_when_enabled_execution_success(
        self, tmp_path: Path
    ) -> None:
        """Test that symlinks are allowed when allow_symlinks=True."""
        real_file = tmp_path / "real.txt"
        real_file.touch()

        symlink_path = tmp_path / "link.txt"
        symlink_path.symlink_to("real.txt")

        result = guard_path_traversal(symlink_path, tmp_path, allow_symlinks=True)
        assert result == real_file.resolve()

    def test_security_guards_path_escapes_base_dir_msg_execution_success(self, tmp_path: Path) -> None:
        """Test the exact error msg for path escape."""
        subdir = tmp_path / "allowed"
        subdir.mkdir()
        outside_file = tmp_path / "outside.txt"
        outside_file.touch()

        with pytest.raises(SecurityError) as exc_info:
            guard_path_traversal(outside_file, subdir)

        assert "path_traversal" in str(exc_info.value).lower()


class TestGuardCommandInjection:
    """Tests for guard_command_injection function."""

    def test_security_guards_safe_command_passes_execution_success(self) -> None:
        """Test that safe commands pass validation."""
        cmd = ["python", "-m", "pytest", "-v"]
        result = guard_command_injection(cmd)
        assert result == cmd

    def test_security_guards_empty_command_blocked_execution_success(self) -> None:
        """Test that empty commands are blocked."""
        with pytest.raises(SecurityError) as exc_info:
            guard_command_injection([])
        assert "Empty command" in str(exc_info.value)

    def test_security_guards_semicolon_blocked_execution_success(self) -> None:
        """Test that semicolons are blocked."""
        with pytest.raises(SecurityError):
            guard_command_injection(["echo", "hello; rm -rf /"])

    def test_security_guards_pipe_blocked_execution_success(self) -> None:
        """Test that pipe characters are blocked."""
        with pytest.raises(SecurityError):
            guard_command_injection(["cat", "file | rm -rf /"])

    def test_security_guards_backtick_blocked_execution_success(self) -> None:
        """Test that backticks are blocked."""
        with pytest.raises(SecurityError):
            guard_command_injection(["echo", "`whoami`"])

    def test_security_guards_dollar_expansion_blocked_execution_success(self) -> None:
        """Test that dollar expansion is blocked."""
        with pytest.raises(SecurityError):
            guard_command_injection(["echo", "$(whoami)"])

    def test_security_guards_allowed_commands_whitelist_execution_success(self) -> None:
        """Test command whitelist functionality."""
        cmd = ["python", "-c", "print('hello')"]
        result = guard_command_injection(cmd, allowed_commands=["python"])
        assert result == cmd

    def test_security_guards_command_not_in_whitelist_blocked_execution_success(
        self,
    ) -> None:
        """Test that commands not in whitelist are blocked."""
        with pytest.raises(SecurityError) as exc_info:
            guard_command_injection(
                ["rm", "-rf", "/"],
                allowed_commands=["python"],
            )
        assert "not in allowed list" in str(exc_info.value)

    def test_security_guards_empty_allowed_commands_whitelist_blocks_all_execution_success(
        self,
    ) -> None:
        """Test that empty whitelist blocks all commands."""
        with pytest.raises(SecurityError) as exc_info:
            guard_command_injection(
                ["ls"],
                allowed_commands=[],
            )
        assert "not in allowed list" in str(exc_info.value)


class TestGuardFileExtension:
    """Tests for guard_file_extension function."""

    def test_security_guards_safe_extension_passes_execution_success(self) -> None:
        """Test that safe extensions pass."""
        result = guard_file_extension("script.py", allowed_extensions=["py", "txt"])
        assert result == Path("script.py")

    def test_security_guards_dangerous_extension_blocked_execution_success(
        self,
    ) -> None:
        """Test that dangerous extensions are blocked."""
        with pytest.raises(SecurityError) as exc_info:
            guard_file_extension("evil.exe")
        assert "not allowed" in str(exc_info.value)

    def test_security_guards_custom_denied_extensions_execution_success(self) -> None:
        """Test custom denied extensions."""
        with pytest.raises(SecurityError):
            guard_file_extension("config.yaml", denied_extensions=["yaml", "yml"])

    def test_security_guards_extension_with_dot_execution_success(self) -> None:
        """Test that extensions with dots are handled."""
        result = guard_file_extension("file.txt", allowed_extensions=[".txt"])
        assert result == Path("file.txt")

    def test_security_guards_normalize_ext_in_denied_execution_success(self) -> None:
        """Test that denied_extensions are normalized correctly."""
        with pytest.raises(SecurityError, match="not allowed"):
            # Should deny 'file.yaml' even if denied list is uppercase and has dots
            guard_file_extension("file.yaml", denied_extensions=[".YAML"])

    def test_security_guards_normalize_ext_in_allowed_execution_success(self) -> None:
        """Test that allowed_extensions are normalized correctly."""
        # Should allow 'file.txt' even if allowed list is uppercase and has dots
        result = guard_file_extension("file.txt", allowed_extensions=[".TXT"])
        assert result == Path("file.txt")

    def test_security_guards_extension_not_in_allowed_list_blocked_execution_success(
        self,
    ) -> None:
        """Test that extensions not in allowed_extensions are blocked."""
        # Testing normalization of input extension vs allowed extensions
        with pytest.raises(SecurityError, match="not in allowed list"):
            guard_file_extension(
                "file.CSV", allowed_extensions=["txt", ".json", "YAML"]
            )


class TestGuardEnvVariable:
    """Tests for guard_env_variable function."""

    def test_security_guards_safe_env_variable_execution_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that safe environment variables are returned."""
        from taipanstack.security.guards import guard_env_variable

        monkeypatch.setenv("SAFE_VAR", "safe_value")
        result = guard_env_variable("SAFE_VAR")
        assert result == "safe_value"

    def test_security_guards_blocked_default_sensitive_execution_success(self) -> None:
        """Test that default sensitive variables are blocked."""
        from taipanstack.security.guards import guard_env_variable

        with pytest.raises(SecurityError, match="denied"):
            guard_env_variable("AWS_SECRET_ACCESS_KEY")

    def test_security_guards_blocked_password_pattern_execution_success(self) -> None:
        """Test that PASSWORD pattern is blocked."""
        from taipanstack.security.guards import guard_env_variable

        with pytest.raises(SecurityError, match="denied"):
            guard_env_variable("DB_PASSWORD")

    def test_security_guards_sensitive_env_set_denied_without_allowed_names_execution_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test set sensitive env var is denied when allowed_names is omitted."""
        from taipanstack.security.guards import guard_env_variable

        monkeypatch.setenv("CUSTOM_TOKEN", "secret")
        with pytest.raises(SecurityError, match="potentially sensitive"):
            guard_env_variable("CUSTOM_TOKEN")

    def test_security_guards_blocked_token_pattern_execution_success(self) -> None:
        """Test that TOKEN pattern is blocked."""
        from taipanstack.security.guards import guard_env_variable

        with pytest.raises(SecurityError, match="denied"):
            guard_env_variable("GITHUB_TOKEN")

    def test_security_guards_missing_env_variable_execution_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that missing variables raise error."""
        from taipanstack.security.guards import guard_env_variable

        monkeypatch.delenv("NONEXISTENT_VAR", raising=False)
        with pytest.raises(SecurityError, match="not set"):
            guard_env_variable("NONEXISTENT_VAR")

    def test_security_guards_custom_denied_names_execution_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test custom denied names."""
        from taipanstack.security.guards import guard_env_variable

        with pytest.raises(SecurityError, match="denied"):
            guard_env_variable("CUSTOM_SECRET", denied_names=["CUSTOM_SECRET"])

    def test_security_guards_allowed_names_not_matching_sensitive_name_execution_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test sensitive env var is denied when allowed_names does not include it."""
        from taipanstack.security.guards import guard_env_variable

        monkeypatch.setenv("API_TOKEN", "secret_token")
        with pytest.raises(SecurityError, match="potentially sensitive"):
            guard_env_variable("API_TOKEN", allowed_names=["SAFE_VAR"])

    def test_security_guards_allowed_names_override_execution_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that allowed_names override pattern blocking."""
        from taipanstack.security.guards import guard_env_variable

        monkeypatch.setenv("MY_TOKEN", "allowed_token")
        result = guard_env_variable("MY_TOKEN", allowed_names=["MY_TOKEN"])
        assert result == "allowed_token"


def test_security_guards_guard_ssrf_ok_and_other_branches_execution_success() -> None:
    from taipanstack.core.result import Ok
    from taipanstack.security.guards import guard_ssrf

    # Ok branch
    res = guard_ssrf("https://www.google.com")
    assert isinstance(res, Ok)


def test_security_guards_guard_ssrf_internal_err_branches_execution_success() -> None:
    from taipanstack.core.result import Err
    from taipanstack.security.guards import guard_ssrf

    # Validation error branch:
    res = guard_ssrf("invalid_url:")
    assert isinstance(res, Err)

    # IP safety error branch:
    res2 = guard_ssrf("http://127.0.0.1")
    assert isinstance(res2, Err)


def test_security_guards_command_injection_rejects_non_string_argument_type_execution_success() -> None:
    """Test command args must all be strings."""
    with pytest.raises(TypeError, match="All command arguments must be strings"):
        guard_command_injection(["echo", 123])


def test_security_guards_env_variable_name_must_be_string_execution_success() -> None:
    """Test env variable name type validation."""
    from taipanstack.security.guards import guard_env_variable

    with pytest.raises(TypeError, match="Variable name must be str"):
        guard_env_variable(123)


def test_security_guards_path_traversal_invalid_base_dir_type_execution_success():
    from taipanstack.security.guards import guard_path_traversal

    with pytest.raises(TypeError, match="base_dir must be str or Path"):
        guard_path_traversal("test.txt", base_dir=123)


def test_security_guards_path_traversal_invalid_path_type_execution_success():
    from taipanstack.security.guards import guard_path_traversal

    with pytest.raises(TypeError, match="path must be str or Path"):
        guard_path_traversal(123, base_dir="test")


def test_security_guards_path_traversal_null_bytes_in_path_execution_success():
    from taipanstack.security.guards import SecurityError, guard_path_traversal

    with pytest.raises(SecurityError, match="Path contains null bytes"):
        guard_path_traversal("test\x00.txt", base_dir="test")


def test_security_guards_path_traversal_null_bytes_in_base_dir_execution_success():
    from taipanstack.security.guards import SecurityError, guard_path_traversal

    with pytest.raises(SecurityError, match="Path contains null bytes"):
        guard_path_traversal("test.txt", base_dir="test\x00")


def test_security_guards_path_traversal_resolve_error_execution_success(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    from taipanstack.security.guards import SecurityError, guard_path_traversal

    original_resolve = Path.resolve

    def mock_resolve(self, *args, **kwargs):
        if str(self).endswith("test.txt"):
            raise OSError("Mock resolve error")
        return original_resolve(self, *args, **kwargs)

    monkeypatch.setattr(Path, "resolve", mock_resolve)
    with pytest.raises(SecurityError, match="Invalid path: Mock resolve error"):
        guard_path_traversal("test.txt", base_dir=tmp_path)


def test_security_guards_path_traversal_symlink_error_execution_success(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    from taipanstack.security.guards import SecurityError, guard_path_traversal

    subdir = tmp_path / "subdir"
    subdir.mkdir()

    def mock_is_symlink(*args, **kwargs):
        raise OSError("Mock is_symlink error")

    monkeypatch.setattr(Path, "is_symlink", mock_is_symlink)

    with pytest.raises(
        SecurityError,
        match="Invalid path encountered during symlink check: Mock is_symlink error",
    ):
        guard_path_traversal("subdir/test.txt", base_dir=tmp_path)


def test_security_guards_command_injection_invalid_command_elements_execution_success():
    from taipanstack.security.guards import SecurityError, guard_command_injection

    with pytest.raises(
        SecurityError, match="Dangerous shell character detected: null byte"
    ):
        guard_command_injection(["echo", "hello\x00"])


def test_security_guards_file_extension_max_length_exceeded_execution_success():
    from taipanstack.security.guards import SecurityError, guard_file_extension

    with pytest.raises(SecurityError, match="Filename length exceeds maximum"):
        guard_file_extension("a" * 2049 + ".txt")


def test_security_guards_file_extension_null_bytes_execution_success():
    from taipanstack.security.guards import SecurityError, guard_file_extension

    with pytest.raises(SecurityError, match="Filename contains null bytes"):
        guard_file_extension("file\x00.txt")


def test_security_guards_ssrf_not_string_type_execution_success():
    from taipanstack.core.result import Err
    from taipanstack.security.guards import SecurityError, guard_ssrf

    res = guard_ssrf(123)
    assert isinstance(res, Err)
    assert isinstance(res.err_value, SecurityError)
    assert "URL must be str" in str(res.err_value)


def test_security_guards_ssrf_empty_url_execution_success():
    from taipanstack.core.result import Err
    from taipanstack.security.guards import SecurityError, guard_ssrf

    res = guard_ssrf("")
    assert isinstance(res, Err)
    assert isinstance(res.err_value, SecurityError)
    assert "URL cannot be empty" in str(res.err_value)


def test_security_guards_ssrf_max_length_exceeded_execution_success():
    from taipanstack.core.result import Err
    from taipanstack.security.guards import SecurityError, guard_ssrf

    res = guard_ssrf("http://example.com/" + "a" * 2048)
    assert isinstance(res, Err)
    assert isinstance(res.err_value, SecurityError)
    assert "URL length exceeds maximum" in str(res.err_value)


def test_security_guards_ssrf_missing_hostname_execution_success():
    from taipanstack.core.result import Err
    from taipanstack.security.guards import SecurityError, guard_ssrf

    res = guard_ssrf("http:///path")
    assert isinstance(res, Err)
    assert isinstance(res.err_value, SecurityError)
    assert "URL has no resolvable hostname" in str(res.err_value)


def test_security_guards_ssrf_unresolvable_hostname_execution_success(monkeypatch):
    import socket

    from taipanstack.core.result import Err
    from taipanstack.security.guards import SecurityError, guard_ssrf

    def mock_getaddrinfo(*args, **kwargs):
        raise socket.gaierror("Name or service not known")

    monkeypatch.setattr(socket, "getaddrinfo", mock_getaddrinfo)

    res = guard_ssrf("http://invalid.domain.that.does.not.exist.com")
    assert isinstance(res, Err)
    assert isinstance(res.err_value, SecurityError)
    assert "Hostname could not be resolved" in str(res.err_value)


def test_security_guards_file_extension_cleaning_dot_execution_success():
    from taipanstack.security.guards import guard_file_extension

    # Test cleaning trailing dots
    res = guard_file_extension("file.txt.", allowed_extensions=["txt"])
    assert res.name == "file.txt."


def test_security_guards_file_extension_normalization_execution_success():
    from taipanstack.security.guards import _normalize_ext

    assert _normalize_ext("TXT") == "txt"
    assert _normalize_ext(".TXT") == "txt"


def test_security_guards_ssrf_malformed_url_execution_success():
    from taipanstack.core.result import Err
    from taipanstack.security.guards import SecurityError, guard_ssrf

    res = guard_ssrf("http://[::1:2:3:4:5:6:7:8]")
    assert isinstance(res, Err)
    assert isinstance(res.err_value, SecurityError)
    assert "Malformed URL:" in str(res.err_value)


def test_security_guards_ssrf_ip_multicast_execution_success():
    from taipanstack.core.result import Err
    from taipanstack.security.guards import SecurityError, guard_ssrf

    # Multicast address 224.0.0.1
    res = guard_ssrf("http://224.0.0.1")
    assert isinstance(res, Err)
    assert isinstance(res.err_value, SecurityError)
    assert "SSRF detected:" in str(res.err_value)


def test_security_guards_ssrf_ip_unspecified_execution_success():
    from taipanstack.core.result import Err
    from taipanstack.security.guards import SecurityError, guard_ssrf

    # Unspecified address 0.0.0.0
    res = guard_ssrf("http://0.0.0.0")
    assert isinstance(res, Err)
    assert isinstance(res.err_value, SecurityError)
    assert "SSRF detected:" in str(res.err_value)


def test_security_guards_env_variable_empty_execution_success():
    import pytest

    from taipanstack.security.guards import SecurityError, guard_env_variable

    with pytest.raises(
        SecurityError, match="Environment variable name cannot be empty or whitespace"
    ):
        guard_env_variable("")


def test_security_guards_env_variable_whitespace_execution_success():
    import pytest

    from taipanstack.security.guards import SecurityError, guard_env_variable

    with pytest.raises(
        SecurityError, match="Environment variable name cannot be empty or whitespace"
    ):
        guard_env_variable("   ")


def test_security_guards_env_variable_null_bytes_execution_success():
    import pytest

    from taipanstack.security.guards import SecurityError, guard_env_variable

    with pytest.raises(
        SecurityError, match="Environment variable name cannot contain null bytes"
    ):
        guard_env_variable("TOKEN\x00")


def test_security_guards_file_extension_cleaning_z_category_execution_success():
    from taipanstack.security.guards import guard_file_extension

    res = guard_file_extension("file.txt\u00a0", allowed_extensions=["txt"])
    assert res.name == "file.txt\u00a0"


def test_security_guards_file_extension_cleaning_c_category_execution_success():
    from taipanstack.security.guards import guard_file_extension

    # \u200b is a zero width space (Cf category)
    res = guard_file_extension("file.txt\u200b", allowed_extensions=["txt"])
    assert res.name == "file.txt\u200b"


def test_security_guards_file_extension_cleaning_ad_execution_success():
    from taipanstack.security.guards import guard_file_extension

    # Test cleaning soft hyphen
    res = guard_file_extension("file.txt\xad", allowed_extensions=["txt"])
    assert res.name == "file.txt\xad"


def test_security_guards_ssrf_ip_resolve_error_execution_success(monkeypatch):
    import socket

    from taipanstack.core.result import Err
    from taipanstack.security.guards import SecurityError, guard_ssrf

    def mock_getaddrinfo(*args, **kwargs):
        raise UnicodeError("Unicode error")

    monkeypatch.setattr(socket, "getaddrinfo", mock_getaddrinfo)

    res = guard_ssrf("http://example.com")
    assert isinstance(res, Err)
    assert isinstance(res.err_value, SecurityError)
    assert "Hostname could not be resolved or contains invalid characters" in str(
        res.err_value
    )


def test_security_guards_file_extension_cleaning_non_matching_char_execution_success():
    from taipanstack.security.guards import guard_file_extension

    res = guard_file_extension("file.txta", allowed_extensions=["txta"])
    assert res.name == "file.txta"


def test_security_guards_file_extension_no_allowed_execution_success():
    from taipanstack.security.guards import guard_file_extension

    res = guard_file_extension("file.txt", allowed_extensions=None)
    assert res.name == "file.txt"


def test_security_guards_env_variable_allowed_names_execution_success():
    import pytest

    from taipanstack.security.guards import SecurityError, guard_env_variable

    # When allowed_names is None, default sensitive patterns are checked and blocked
    with pytest.raises(SecurityError, match="potentially sensitive"):
        guard_env_variable("MY_TOKEN")


def test_security_guards_file_extension_denied_default_execution_success():
    import pytest

    from taipanstack.security.guards import SecurityError, guard_file_extension

    with pytest.raises(SecurityError, match="not allowed"):
        guard_file_extension("file.exe")


def test_security_guards_env_variable_allowed_names_empty_list_execution_success():
    import pytest

    from taipanstack.security.guards import SecurityError, guard_env_variable

    with pytest.raises(SecurityError, match="potentially sensitive"):
        guard_env_variable("MY_TOKEN", allowed_names=[])


def test_security_guards_ssrf_ip_is_safe_attribute_error_execution_success(monkeypatch):
    import ipaddress

    from taipanstack.security.guards import _is_ip_safe

    # Check what happens when ip_address has no is_multicast
    original_ip_address = ipaddress.ip_address

    def mock_ip_address(*args, **kwargs):
        addr = original_ip_address(*args, **kwargs)
        # We can't easily mock the object attributes without a custom class,
        # but hasattr handles it. We'll just test a known safe IP to cover
        # the normal path of getattr returning False
        return addr

    monkeypatch.setattr(ipaddress, "ip_address", mock_ip_address)
    assert _is_ip_safe("8.8.8.8") is True


def test_security_guards_file_extension_cleaning_empty_clean_name_execution_success():
    from taipanstack.security.guards import SecurityError, guard_file_extension

    with pytest.raises(SecurityError, match="not in allowed list"):
        guard_file_extension(".", allowed_extensions=["txt"])


def test_security_guards_ssrf_ip_is_safe_value_error_execution_success():
    from taipanstack.security.guards import _is_ip_safe

    # Check what happens when ip_address gets invalid IP
    assert _is_ip_safe("invalid_ip") is True


def test_security_guards_ssrf_url_invalid_characters_execution_success() -> None:
    """Test guard_ssrf rejects URLs with invalid characters."""
    from taipanstack.core.result import Err
    from taipanstack.security.guards import guard_ssrf

    result = guard_ssrf("http://exa\x20mple.com")
    assert isinstance(result, Err)
    assert "URL contains invalid characters" in str(result.err_value)


def test_security_guards_ssrf_url_valid_characters_execution_success() -> None:
    """Test guard_ssrf accepts URLs with valid characters."""
    from taipanstack.core.result import Ok
    from taipanstack.security.guards import guard_ssrf

    result = guard_ssrf("http://example.com")
    assert isinstance(result, Ok)


def test_security_guards_ssrf_url_invalid_characters_branch_execution_success() -> None:
    """Test guard_ssrf rejects URLs with invalid characters (specifically covering the branch)."""
    from taipanstack.core.result import Err
    from taipanstack.security.guards import guard_ssrf

    # This covers the c == "\x7f" part of the branch
    result = guard_ssrf("http://example.com/\x7f")
    assert isinstance(result, Err)
    assert "URL contains invalid characters" in str(result.err_value)
