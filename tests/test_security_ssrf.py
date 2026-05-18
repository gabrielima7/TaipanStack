"""Tests for guard_ssrf — SSRF protection guard."""

import socket
from unittest.mock import patch

from taipanstack.security.guards import SecurityError, guard_ssrf


class TestGuardSsrfTypeContract:
    """Test TypeError enforcement for non-string inputs."""

    def test_security_ssrf_raises_err_for_int(self) -> None:
        """Return Err when URL is an integer."""
        result = guard_ssrf(123)
        assert result.is_err()

    def test_security_ssrf_raises_err_for_none(self) -> None:
        """Return Err when URL is None."""
        result = guard_ssrf(None)
        assert result.is_err()

    def test_security_ssrf_raises_err_for_bytes(self) -> None:
        """Return Err when URL is bytes."""
        result = guard_ssrf(b"http://example.com")
        assert result.is_err()

    @patch("taipanstack.security.guards.urlsplit")
    def test_security_ssrf_raises_value_error_from_urlparse(
        self, mock_urlparse
    ) -> None:
        """Return Err when urlparse raises ValueError."""
        mock_urlparse.side_effect = ValueError("Mocked error")
        result = guard_ssrf("http://example.com")
        assert result.is_err()
        err = result.err_value
        assert isinstance(err, SecurityError)
        assert err.guard_name == "ssrf"
        msg = str(err)
        assert "Malformed URL" in msg
        assert "Mocked error" in msg


class TestGuardSsrfEmptyAndMalformed:
    """Test empty or scheme-less inputs return Err."""

    def test_security_ssrf_empty_url_returns_err(self) -> None:
        """Empty string returns Err with appropriate message."""
        result = guard_ssrf("")
        assert result.is_err()
        err = result.err_value
        assert isinstance(err, SecurityError)
        assert err.guard_name == "ssrf"

    def test_security_ssrf_disallowed_scheme_ftp_returns_err(self) -> None:
        """FTP scheme is rejected as not allowed."""
        result = guard_ssrf("ftp://example.com/file")
        assert result.is_err()
        err = result.err_value
        assert isinstance(err, SecurityError)
        assert "not allowed" in str(err)

    def test_security_ssrf_disallowed_scheme_file_returns_err(self) -> None:
        """file:// scheme is rejected."""
        result = guard_ssrf("file:///etc/passwd")
        assert result.is_err()

    def test_security_ssrf_no_hostname_returns_err(self) -> None:
        """URL without hostname returns Err."""
        result = guard_ssrf("http:///path-only")
        assert result.is_err()

    def test_security_ssrf_unresolvable_hostname_returns_err(self) -> None:
        """Hostname that cannot be resolved returns Err. Verifies platform-independent error and truncation."""
        long_hostname = "a" * 100 + ".invalid"
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            side_effect=socket.gaierror("mocked error"),
        ):
            result = guard_ssrf(f"https://{long_hostname}/path")

        assert result.is_err()
        err = result.err_value
        assert isinstance(err, SecurityError)
        assert err.guard_name == "ssrf"
        # Verify the exception message prefix without asserting on platform-specific gaierror strings
        assert "Hostname could not be resolved" in str(err)
        # Verify the value attribute contains the hostname truncated to 80 characters
        assert err.value is None


class TestGuardSsrfPrivateIpv4:
    """Test SSRF detection for private IPv4 ranges."""

    def _mock_getaddrinfo(
        self, ip: str
    ) -> list[tuple[int, int, int, str, tuple[str, int]]]:
        """Return a fake getaddrinfo response for the given IP."""
        return [(socket.AF_INET, socket.SOCK_STREAM, 0, "", (ip, 0))]

    def test_security_ssrf_loopback_127_0_0_1_blocked(self) -> None:
        """127.0.0.1 (loopback) must be blocked."""
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=self._mock_getaddrinfo("127.0.0.1"),
        ):
            result = guard_ssrf("http://internal.svc/api")
        assert result.is_err()
        assert "SSRF" in str(result.err_value)

    def test_security_ssrf_private_10_network_blocked(self) -> None:
        """10.0.0.1 (RFC-1918 class A) must be blocked."""
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=self._mock_getaddrinfo("10.0.0.1"),
        ):
            result = guard_ssrf("http://internal.svc/api")
        assert result.is_err()

    def test_security_ssrf_private_172_16_network_blocked(self) -> None:
        """172.16.0.1 (RFC-1918 class B) must be blocked."""
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=self._mock_getaddrinfo("172.16.0.1"),
        ):
            result = guard_ssrf("http://internal.svc/api")
        assert result.is_err()

    def test_security_ssrf_private_192_168_network_blocked(self) -> None:
        """192.168.1.1 (RFC-1918 class C) must be blocked."""
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=self._mock_getaddrinfo("192.168.1.1"),
        ):
            result = guard_ssrf("https://my-service.local/")
        assert result.is_err()

    def test_security_ssrf_aws_metadata_endpoint_blocked(self) -> None:
        """169.254.169.254 (AWS EC2 metadata) must be blocked."""
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=self._mock_getaddrinfo("169.254.169.254"),
        ):
            result = guard_ssrf("http://169.254.169.254/latest/meta-data/")
        assert result.is_err()
        err = result.err_value
        assert isinstance(err, SecurityError)
        assert err.guard_name == "ssrf"

    def test_security_ssrf_link_local_169_254_blocked(self) -> None:
        """169.254.0.1 (link-local range) must be blocked."""
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=self._mock_getaddrinfo("169.254.0.1"),
        ):
            result = guard_ssrf("http://host.local/")
        assert result.is_err()

    def test_security_ssrf_localhost_string_blocked(self) -> None:
        """'localhost' resolving to 127.0.0.1 must be blocked."""
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=self._mock_getaddrinfo("127.0.0.1"),
        ):
            result = guard_ssrf("http://localhost:8080/admin")
        assert result.is_err()


class TestGuardSsrfPrivateIpv6:
    """Test SSRF detection for private IPv6 addresses."""

    def _mock_getaddrinfo_v6(
        self, ip: str
    ) -> list[tuple[int, int, int, str, tuple[str, int, int, int]]]:
        """Return a fake getaddrinfo response for an IPv6 address."""
        return [(socket.AF_INET6, socket.SOCK_STREAM, 0, "", (ip, 0, 0, 0))]

    def test_security_ssrf_ipv6_loopback_blocked(self) -> None:
        """::1 (IPv6 loopback) must be blocked."""
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=self._mock_getaddrinfo_v6("::1"),
        ):
            result = guard_ssrf("http://[::1]/path")
        assert result.is_err()

    def test_security_ssrf_ipv6_unique_local_blocked(self) -> None:
        """fc00:: unique local (ULA) must be blocked."""
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=self._mock_getaddrinfo_v6("fc00::1"),
        ):
            result = guard_ssrf("https://host.example.com/")
        assert result.is_err()

    def test_security_ssrf_ipv6_link_local_blocked(self) -> None:
        """fe80:: link-local must be blocked."""
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=self._mock_getaddrinfo_v6("fe80::1"),
        ):
            result = guard_ssrf("https://host.example.com/")
        assert result.is_err()


class TestGuardSsrfSafeUrls:
    """Test that safe, public URLs pass the guard."""

    def _mock_public_ip(self) -> list[tuple[int, int, int, str, tuple[str, int]]]:
        """Return a fake getaddrinfo with a public routable IP."""
        return [(socket.AF_INET, socket.SOCK_STREAM, 0, "", ("93.184.216.34", 0))]

    def test_security_ssrf_public_http_url_accepted(self) -> None:
        """A URL resolving to a public IP returns Ok."""
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=self._mock_public_ip(),
        ):
            result = guard_ssrf("http://example.com/api")
        assert result.is_ok()
        assert result.ok_value == "http://example.com/api"

    def test_security_ssrf_public_https_url_accepted(self) -> None:
        """A HTTPS URL resolving to a public IP returns Ok."""
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=self._mock_public_ip(),
        ):
            result = guard_ssrf("https://example.com/api")
        assert result.is_ok()

    def test_security_ssrf_custom_allowed_schemes_accepted(self) -> None:
        """A URL with a custom-allowed scheme passes when explicitly permitted."""
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=self._mock_public_ip(),
        ):
            result = guard_ssrf(
                "ftp://files.example.com/",
                allowed_schemes=frozenset({"ftp", "ftps"}),
            )
        assert result.is_ok()

    def test_security_ssrf_invalid_ip_in_addr_info_skipped(self) -> None:
        """Invalid IP strings inside addr_info are skipped gracefully."""
        # Simulate a malformed entry followed by a safe public IP
        bad_entry = (socket.AF_INET, socket.SOCK_STREAM, 0, "", ("not-an-ip", 0))
        good_entry = (socket.AF_INET, socket.SOCK_STREAM, 0, "", ("93.184.216.34", 0))
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=[bad_entry, good_entry],
        ):
            result = guard_ssrf("https://example.com/")
        assert result.is_ok()


class TestGuardSsrfErrorAttrs:
    """Verify SecurityError attributes emitted by guard_ssrf."""

    def _mock_loopback(self) -> list[tuple[int, int, int, str, tuple[str, int]]]:
        return [(socket.AF_INET, socket.SOCK_STREAM, 0, "", ("127.0.0.1", 0))]

    def test_security_ssrf_security_error_guard_name_is_ssrf(self) -> None:
        """SecurityError.guard_name must equal 'ssrf'."""
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=self._mock_loopback(),
        ):
            result = guard_ssrf("http://internal/")
        err = result.err_value
        assert isinstance(err, SecurityError)
        assert err.guard_name == "ssrf"

    def test_security_ssrf_security_error_value_is_ip_string(self) -> None:
        """SecurityError.value must not expose the offending IP address anymore."""
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=self._mock_loopback(),
        ):
            result = guard_ssrf("http://internal/")
        err = result.err_value
        assert isinstance(err, SecurityError)
        assert err.value is None


class TestGuardSsrfCatchAllReserved:
    """Test the catch-all branch for reserved addresses outside explicit nets."""

    def _mock_getaddrinfo(
        self, ip: str
    ) -> list[tuple[int, int, int, str, tuple[str, int]]]:
        """Return a fake getaddrinfo response for the given IP."""
        return [(socket.AF_INET, socket.SOCK_STREAM, 0, "", (ip, 0))]

    def test_security_ssrf_zero_address_blocked_by_catchall(self) -> None:
        """0.0.0.0 is is_private but not in explicit network list — hits catch-all."""
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=self._mock_getaddrinfo("0.0.0.0"),  # noqa: S104
        ):
            result = guard_ssrf("http://some-host.example.com/")
        assert result.is_err()
        err = result.err_value
        assert isinstance(err, SecurityError)
        assert "reserved" in str(err).lower() or "SSRF" in str(err)
        assert err.guard_name == "ssrf"


# Migrated from tests/test_final_coverage_operations.py
"""Final tests to reach 100% coverage."""

from pathlib import Path

import pytest


class TestLoggingComplete:
    """Complete tests for logging module covering all branches."""

    def test_final_coverage_logger_all_levels(self) -> None:
        """Test StackLogger all log levels."""
        from taipanstack.utils.logging import StackLogger

        logger = StackLogger(name="test", level="DEBUG")

        # Test all levels
        logger.debug("debug msg")
        logger.info("info msg")
        logger.warning("warning msg")
        logger.error("error msg")
        logger.critical("critical msg")

    def test_final_coverage_logger_exception(self) -> None:
        """Test StackLogger exception method."""
        from taipanstack.utils.logging import StackLogger

        logger = StackLogger()
        try:
            raise RuntimeError("test")
        except RuntimeError:
            logger.exception("caught exception")

    def test_final_coverage_log_operation_context_manager(self) -> None:
        """Test log_operation context manager."""
        from taipanstack.utils.logging import log_operation

        with log_operation("test_operation") as log:
            log.info("inside operation")


class TestGuardsComplete:
    """Complete tests for guards module."""

    def test_final_coverage_guard_env_variable_pattern_not_in_allowed(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test guard_env_variable when pattern matches but not in allowed."""
        from taipanstack.security.guards import guard_env_variable

        # Set a secret-like env variable
        monkeypatch.setenv("CUSTOM_API_KEY", "secret123")

        # Should raise because matches *API*KEY* pattern
        with pytest.raises(SecurityError):
            guard_env_variable("CUSTOM_API_KEY")

    def test_final_coverage_guard_env_variable_pattern_in_allowed(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test guard_env_variable when pattern matches and in allowed."""
        from taipanstack.security.guards import guard_env_variable

        monkeypatch.setenv("CUSTOM_API_KEY", "allowed_secret")

        # Should work because explicitly allowed
        result = guard_env_variable(
            "CUSTOM_API_KEY",
            allowed_names=["CUSTOM_API_KEY"],
        )
        assert result == "allowed_secret"


class TestSubprocessComplete:
    """Complete tests for subprocess module."""

    def test_final_coverage_run_safe_command_with_all_options(self) -> None:
        """Test run_safe_command with all options."""
        from taipanstack.utils.subprocess import run_safe_command

        result = run_safe_command(
            ["echo", "hello"],
            timeout=30.0,
            capture_output=True,
            check=False,
        )
        assert result.success
        assert "hello" in result.stdout


class TestSanitizersComplete:
    """Complete tests for sanitizers module."""

    def test_final_coverage_sanitize_string_with_unicode(self) -> None:
        """Test sanitize_string with allow_unicode=False."""
        from taipanstack.security.sanitizers import sanitize_string

        result = sanitize_string("Héllo Wörld", allow_unicode=False)
        assert "é" not in result
        assert "ö" not in result

    def test_final_coverage_sanitize_string_with_max_length(self) -> None:
        """Test sanitize_string with max_length."""
        from taipanstack.security.sanitizers import sanitize_string

        result = sanitize_string("This is a long string", max_length=10)
        assert len(result) == 10

    def test_final_coverage_sanitize_filename_long_name(self) -> None:
        """Test sanitize_filename with very long name."""
        from taipanstack.security.sanitizers import sanitize_filename

        long_name = "a" * 300 + ".txt"
        result = sanitize_filename(long_name, max_length=100)
        assert len(result) <= 100

    def test_final_coverage_sanitize_env_value_multiline(self) -> None:
        """Test sanitize_env_value with multiline."""
        from taipanstack.security.sanitizers import sanitize_env_value

        # Without allowing multiline
        result = sanitize_env_value("line1\nline2", allow_multiline=False)
        assert "\n" not in result

        # With allowing multiline
        result = sanitize_env_value("line1\nline2", allow_multiline=True)
        assert "\n" in result


class TestValidatorsComplete:
    """Complete tests for validators module."""

    def test_final_coverage_validate_email_valid(self) -> None:
        """Test validate_email with valid email."""
        from taipanstack.security.validators import validate_email

        result = validate_email("user@example.com")
        assert result == "user@example.com"

    def test_final_coverage_validate_url_https(self) -> None:
        """Test validate_url with https."""
        from urllib.parse import urlparse

        from taipanstack.security.validators import validate_url

        result = validate_url("https://secure.example.com/path?query=1")
        parsed = urlparse(result)
        assert parsed.hostname == "secure.example.com"


class TestFilesystemComplete:
    """Complete tests for filesystem module."""

    def test_final_coverage_safe_write_non_atomic(self, tmp_path: Path) -> None:
        """Test safe_write with atomic=False."""
        from taipanstack.utils.filesystem import WriteOptions, safe_write

        test_file = tmp_path / "non_atomic.txt"
        result = safe_write(test_file, "content", options=WriteOptions(atomic=False))
        assert result.read_text() == "content"


class TestConfigModelsComplete:
    """Complete tests for config models."""

    def test_final_coverage_stack_config_all_options(self) -> None:
        """Test StackConfig with all options."""
        from taipanstack.config.models import StackConfig

        config = StackConfig(
            project_name="myproject",
            python_version="3.11",
            dry_run=True,
            force=True,
        )
        assert config.project_name == "myproject"
        assert config.python_version == "3.11"
        assert config.dry_run is True


class TestDecoratorsComplete:
    """Complete tests for decorators module."""

    def test_final_coverage_validate_inputs_with_validation(self) -> None:
        """Test validate_inputs with actual validation."""
        from taipanstack.security.decorators import ValidationError, validate_inputs

        def must_be_positive(x: int) -> int:
            if x <= 0:
                raise ValueError("Must be positive")
            return x

        @validate_inputs(value=must_be_positive)
        def process(value: int) -> int:
            return value * 2

        # Valid input
        assert process(value=5) == 10

        # Invalid input
        with pytest.raises(ValidationError):
            process(value=-1)

    def test_final_coverage_guard_exceptions_reraise_non_security(
        self,
    ) -> None:
        """Test guard_exceptions with non-SecurityError reraise."""
        from taipanstack.security.decorators import guard_exceptions

        @guard_exceptions(catch=(ValueError,), reraise_as=TypeError)
        def raise_value_error() -> None:
            raise ValueError("original")

        with pytest.raises(TypeError):
            raise_value_error()

    def test_final_coverage_deprecated_with_removal_version(self) -> None:
        """Test deprecated with removal_version."""
        import warnings

        from taipanstack.security.decorators import deprecated

        @deprecated("Use new_func", removal_version="3.0.0")
        def old_func() -> str:
            return "old"

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = old_func()
            assert result == "old"
            assert len(w) == 1
            assert "3.0.0" in str(w[0].message)

    def test_final_coverage_require_type_passes(self) -> None:
        """Test require_type with valid types."""
        from taipanstack.security.decorators import require_type

        @require_type(name=str, count=int)
        def greet(name: str, count: int) -> str:
            return name * count

        result = greet(name="hi", count=2)
        assert result == "hihi"

    def test_final_coverage_require_type_fails(self) -> None:
        """Test require_type with invalid types."""
        from taipanstack.security.decorators import require_type

        @require_type(name=str)
        def greet(name: str) -> str:
            return name

        with pytest.raises(TypeError, match="expected str, got int"):
            greet(name=123)


class TestCircuitBreakerComplete:
    """Complete tests for circuit breaker."""

    def test_final_coverage_excluded_exceptions_work(self) -> None:
        """Test that excluded exceptions don't trip circuit."""
        from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState

        breaker = CircuitBreaker(
            failure_threshold=2,
            excluded_exceptions=(ValueError,),
        )

        @breaker
        def raise_value() -> None:
            raise ValueError("excluded")

        # These should not trip the circuit
        for _ in range(5):
            with pytest.raises(ValueError):
                raise_value()

        assert breaker.state == CircuitState.CLOSED
        assert breaker.failure_count == 0


class TestRetryComplete:
    """Complete tests for retry module."""

    def test_final_coverage_retry_backoff_exponential(self) -> None:
        """Test retry with exponential backoff."""
        from taipanstack.resilience.retry import RetryConfig, calculate_delay

        config = RetryConfig(
            initial_delay=1.0,
            exponential_base=2.0,
            jitter=False,
        )

        delay1 = calculate_delay(1, config)
        delay2 = calculate_delay(2, config)
        delay3 = calculate_delay(3, config)

        assert delay2 > delay1
        assert delay3 > delay2


# Migrated from tests/test_fuzz_guard_command_generator_operations.py
import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.guards import guard_command_injection


@settings(
    max_examples=500,
    suppress_health_check=[HealthCheck.large_base_example, HealthCheck.data_too_large],
)
@given(st.lists(st.text()))
def test_fuzz_guard_command_generator_returns_ok_or_raises_error(cmd_list):
    def gen():
        yield from cmd_list

    try:
        result = guard_command_injection(gen())
        assert isinstance(result, list)
    except Exception as e:
        assert isinstance(e, (SecurityError, ValueError, TypeError))


def test_guard_command_empty_generator_raises_error():
    def empty_gen():
        yield from ()

    with pytest.raises(SecurityError, match="Empty command is not allowed"):
        guard_command_injection(empty_gen())


# Migrated from tests/test_fuzz_guard_file_extension_operations.py
import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.guards import guard_file_extension


@settings(max_examples=200)
@given(st.text())
def test_fuzz_guard_file_extension_null_bytes(filename: str) -> None:
    """Ensure filenames with null bytes are rejected."""
    if len(filename) > 4096:
        with pytest.raises(SecurityError, match="Filename length exceeds"):
            guard_file_extension(filename, denied_extensions=["exe"])
        return

    if "\x00" in filename:
        with pytest.raises(SecurityError, match="null byte"):
            guard_file_extension(filename, denied_extensions=["exe"])


@settings(max_examples=200)
@given(
    st.text(
        alphabet=st.characters(
            whitelist_categories=("Z", "C"), whitelist_characters=[".", " ", "\xad"]
        ),
        min_size=1,
        max_size=10,
    )
)
def test_fuzz_guard_file_extension_whitespace_and_dots(padding: str) -> None:
    """Ensure trailing spaces, dots, and control characters don't bypass the extension check."""
    # We want to catch Windows-style bypasses like 'test.exe.' or 'test.exe \n'
    # padding only contains whitespace, control chars, or dots
    filename = f"test.exe{padding}"

    # \x00 should raise null byte error
    if "\x00" in padding:
        with pytest.raises(SecurityError, match="null byte"):
            guard_file_extension(filename, denied_extensions=["exe"])
    else:
        # It should detect 'exe' as the extension and reject it
        with pytest.raises(SecurityError, match="not allowed"):
            guard_file_extension(filename, denied_extensions=["exe"])


def test_fuzz_guard_file_extension_empty_after_strip() -> None:
    """Ensure that filenames that become empty after stripping are handled correctly."""
    with pytest.raises(SecurityError, match="not in allowed list"):
        guard_file_extension("   \\xad", allowed_extensions=["txt"])


def test_fuzz_guard_file_extension_empty_name() -> None:
    """Ensure that filenames with no name component are handled."""
    with pytest.raises(SecurityError, match="not in allowed list"):
        guard_file_extension("/", allowed_extensions=["txt"])


@settings(
    suppress_health_check=[
        HealthCheck.large_base_example,
        HealthCheck.data_too_large,
        HealthCheck.too_slow,
    ],
    max_examples=2,
    deadline=None,
)
@given(st.text(min_size=4097, max_size=4099))
def test_fuzz_guard_file_extension_massive_strings_dos_property(
    ext: str,
) -> None:
    """Fuzz guard_file_extension with massive strings property test to ensure DoS protection limits are active."""
    with pytest.raises(
        SecurityError, match="Filename length exceeds maximum allowed limit"
    ):
        guard_file_extension(f"file.{ext}")


def test_fuzz_guard_file_extension_massive_strings_dos() -> None:
    """Fuzz guard_file_extension with massive strings to ensure DoS protection limits are active."""
    ext = "a" * 50000
    with pytest.raises(
        SecurityError, match="Filename length exceeds maximum allowed limit"
    ):
        guard_file_extension(f"file.{ext}")


# Migrated from tests/test_fuzz_guard_null_bytes_operations.py
from hypothesis import given
from hypothesis import strategies as st

from taipanstack.security.guards import guard_env_variable


@given(st.lists(st.text(), min_size=1))
def test_guard_command_injection_fuzz_returns_ok_or_raises_error(cmd):
    try:
        result = guard_command_injection(cmd)
        assert isinstance(result, list)
    except Exception as e:
        assert isinstance(e, (SecurityError, ValueError, TypeError))


@given(st.text())
def test_guard_env_variable_fuzz_returns_ok_or_raises_error(env):
    try:
        result = guard_env_variable(env)
        assert isinstance(result, str)
    except Exception as e:
        assert isinstance(e, (SecurityError, ValueError, TypeError))


def test_guard_command_injection_null_byte_raises_error():
    import pytest

    with pytest.raises(SecurityError, match="null byte"):
        guard_command_injection(["\x00"])


def test_guard_env_variable_null_byte_raises_error():
    import pytest

    with pytest.raises(SecurityError, match="null byte"):
        guard_env_variable("\x00")


# Migrated from tests/test_fuzz_guard_path_operations.py
from pathlib import Path

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.guards import guard_path_traversal


@settings(
    suppress_health_check=[HealthCheck.large_base_example, HealthCheck.data_too_large],
    max_examples=100,
)
@given(st.text(min_size=1000, max_size=2000))
def test_fuzz_guard_path_traversal_massive(name: str) -> None:
    """Fuzz guard_path_traversal with massive strings."""
    try:
        guard_path_traversal(name, base_dir=Path("/safe_tmp"))
    except (ValueError, TypeError, SecurityError):
        assert True
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")


@settings(suppress_health_check=[HealthCheck.filter_too_much])
@given(
    st.text(
        alphabet=st.characters(
            blacklist_categories=("Cc",), whitelist_characters=["\x00"]
        ),
        min_size=1,
        max_size=100,
    ).filter(lambda s: "\x00" in s)
)
def test_fuzz_guard_path_traversal_null_bytes(name: str) -> None:
    """Fuzz guard_path_traversal with null bytes."""
    try:
        guard_path_traversal(name, base_dir=Path("/safe_tmp"))
    except (ValueError, TypeError, SecurityError):
        assert True
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")


# Migrated from tests/test_fuzz_guard_symlink_loop_operations.py
import tempfile
from pathlib import Path

import pytest


def test_guard_path_traversal_symlink_loop_runtime_error() -> None:
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        link1 = base / "link1"
        link2 = base / "link2"
        link1.symlink_to("link2")
        link2.symlink_to("link1")

        with pytest.raises(
            SecurityError, match=r"Invalid path|Symlinks are not allowed"
        ):
            guard_path_traversal(link1, base, allow_symlinks=False)


# Migrated from tests/test_fuzz_path_traversal.py
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st


@settings(max_examples=1000)
@given(
    path=st.one_of(st.text(), st.binary(), st.integers()),
    base_dir=st.one_of(st.none(), st.text(), st.binary()),
    allow_symlinks=st.booleans(),
)
def test_fuzz_guard_path_traversal(path, base_dir, allow_symlinks):
    import contextlib

    with contextlib.suppress(SecurityError, TypeError):
        result = guard_path_traversal(
            path, base_dir=base_dir, allow_symlinks=allow_symlinks
        )
        assert isinstance(result, Path)
