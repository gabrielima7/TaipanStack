"""Tests for guard_ssrf — SSRF protection guard."""

import ipaddress
import socket
from unittest.mock import patch

import pytest

from taipanstack.security.guards import SecurityError, guard_ssrf


class TestGuardSsrfTypeContract:
    """Test TypeError enforcement for non-string inputs."""

    def test_raises_type_error_for_int(self) -> None:
        """Raise TypeError when URL is an integer."""
        with pytest.raises(TypeError, match="URL must be str"):
            guard_ssrf(123)  # type: ignore[arg-type]

    def test_raises_type_error_for_none(self) -> None:
        """Raise TypeError when URL is None."""
        with pytest.raises(TypeError, match="URL must be str"):
            guard_ssrf(None)  # type: ignore[arg-type]

    def test_raises_type_error_for_bytes(self) -> None:
        """Raise TypeError when URL is bytes."""
        with pytest.raises(TypeError, match="URL must be str"):
            guard_ssrf(b"http://example.com")  # type: ignore[arg-type]

    @patch("taipanstack.security.guards.urlparse")
    def test_raises_value_error_from_urlparse(self, mock_urlparse) -> None:
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

    def test_empty_url_returns_err(self) -> None:
        """Empty string returns Err with appropriate message."""
        result = guard_ssrf("")
        assert result.is_err()
        err = result.err_value
        assert isinstance(err, SecurityError)
        assert err.guard_name == "ssrf"

    def test_disallowed_scheme_ftp_returns_err(self) -> None:
        """FTP scheme is rejected as not allowed."""
        result = guard_ssrf("ftp://example.com/file")
        assert result.is_err()
        err = result.err_value
        assert isinstance(err, SecurityError)
        assert "not allowed" in str(err)

    def test_disallowed_scheme_file_returns_err(self) -> None:
        """file:// scheme is rejected."""
        result = guard_ssrf("file:///etc/passwd")
        assert result.is_err()

    def test_no_hostname_returns_err(self) -> None:
        """URL without hostname returns Err."""
        result = guard_ssrf("http:///path-only")
        assert result.is_err()

    def test_unresolvable_hostname_returns_err(self) -> None:
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
        assert "Hostname could not be resolved:" in str(err)
        # Verify the value attribute contains the hostname truncated to 80 characters
        assert err.value == long_hostname[:80]


class TestGuardSsrfPrivateIpv4:
    """Test SSRF detection for private IPv4 ranges."""

    def _mock_getaddrinfo(
        self, ip: str
    ) -> list[tuple[int, int, int, str, tuple[str, int]]]:
        """Return a fake getaddrinfo response for the given IP."""
        return [(socket.AF_INET, socket.SOCK_STREAM, 0, "", (ip, 0))]

    def test_loopback_127_0_0_1_blocked(self) -> None:
        """127.0.0.1 (loopback) must be blocked."""
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=self._mock_getaddrinfo("127.0.0.1"),
        ):
            result = guard_ssrf("http://internal.svc/api")
        assert result.is_err()
        assert "SSRF" in str(result.err_value)

    def test_private_10_network_blocked(self) -> None:
        """10.0.0.1 (RFC-1918 class A) must be blocked."""
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=self._mock_getaddrinfo("10.0.0.1"),
        ):
            result = guard_ssrf("http://internal.svc/api")
        assert result.is_err()

    def test_private_172_16_network_blocked(self) -> None:
        """172.16.0.1 (RFC-1918 class B) must be blocked."""
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=self._mock_getaddrinfo("172.16.0.1"),
        ):
            result = guard_ssrf("http://internal.svc/api")
        assert result.is_err()

    def test_private_192_168_network_blocked(self) -> None:
        """192.168.1.1 (RFC-1918 class C) must be blocked."""
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=self._mock_getaddrinfo("192.168.1.1"),
        ):
            result = guard_ssrf("https://my-service.local/")
        assert result.is_err()

    def test_aws_metadata_endpoint_blocked(self) -> None:
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

    def test_link_local_169_254_blocked(self) -> None:
        """169.254.0.1 (link-local range) must be blocked."""
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=self._mock_getaddrinfo("169.254.0.1"),
        ):
            result = guard_ssrf("http://host.local/")
        assert result.is_err()

    def test_localhost_string_blocked(self) -> None:
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

    def test_ipv6_loopback_blocked(self) -> None:
        """::1 (IPv6 loopback) must be blocked."""
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=self._mock_getaddrinfo_v6("::1"),
        ):
            result = guard_ssrf("http://[::1]/path")
        assert result.is_err()

    def test_ipv6_unique_local_blocked(self) -> None:
        """fc00:: unique local (ULA) must be blocked."""
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=self._mock_getaddrinfo_v6("fc00::1"),
        ):
            result = guard_ssrf("https://host.example.com/")
        assert result.is_err()

    def test_ipv6_link_local_blocked(self) -> None:
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

    def test_public_http_url_accepted(self) -> None:
        """A URL resolving to a public IP returns Ok."""
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=self._mock_public_ip(),
        ):
            result = guard_ssrf("http://example.com/api")
        assert result.is_ok()
        assert result.ok_value == "http://example.com/api"

    def test_public_https_url_accepted(self) -> None:
        """A HTTPS URL resolving to a public IP returns Ok."""
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=self._mock_public_ip(),
        ):
            result = guard_ssrf("https://example.com/api")
        assert result.is_ok()

    def test_custom_allowed_schemes_accepted(self) -> None:
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

    def test_invalid_ip_in_addr_info_skipped(self) -> None:
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

    def test_security_error_guard_name_is_ssrf(self) -> None:
        """SecurityError.guard_name must equal 'ssrf'."""
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=self._mock_loopback(),
        ):
            result = guard_ssrf("http://internal/")
        err = result.err_value
        assert isinstance(err, SecurityError)
        assert err.guard_name == "ssrf"

    def test_security_error_value_is_ip_string(self) -> None:
        """SecurityError.value must contain the offending IP address."""
        with patch(
            "taipanstack.security.guards.socket.getaddrinfo",
            return_value=self._mock_loopback(),
        ):
            result = guard_ssrf("http://internal/")
        err = result.err_value
        assert isinstance(err, SecurityError)
        assert err.value is not None
        # Should contain the resolved IP address
        resolved = ipaddress.ip_address(err.value)
        assert resolved.is_loopback or resolved.is_private


class TestGuardSsrfCatchAllReserved:
    """Test the catch-all branch for reserved addresses outside explicit nets."""

    def _mock_getaddrinfo(
        self, ip: str
    ) -> list[tuple[int, int, int, str, tuple[str, int]]]:
        """Return a fake getaddrinfo response for the given IP."""
        return [(socket.AF_INET, socket.SOCK_STREAM, 0, "", (ip, 0))]

    def test_zero_address_blocked_by_catchall(self) -> None:
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
