"""Tests for the HTTP Bridge."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from taipanstack.core.result import Err, Ok
from taipanstack.resilience.circuit_breaker import CircuitBreaker
from taipanstack.resilience.retry import RetryConfig
from taipanstack.security.guards import SecurityError


class TestSafeRequest:
    """Tests for the safe_request standalone function."""

    @pytest.mark.asyncio
    async def test_timeout_default_passed_expected(self) -> None:
        """Verifies that safe_request passes default timeout to httpx.AsyncClient."""
        from taipanstack.bridges.http_bridge import safe_request

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with (
            patch("taipanstack.bridges.http_bridge._HAS_HTTPX", True),
            patch(
                "taipanstack.bridges.http_bridge.guard_ssrf",
                return_value=Ok("https://example.com"),
            ),
            patch("taipanstack.bridges.http_bridge.httpx") as mock_httpx,
        ):
            mock_httpx.AsyncClient.return_value = mock_client
            result = await safe_request("GET", "https://example.com")

        assert isinstance(result, Ok)
        mock_httpx.AsyncClient.assert_called_once_with(timeout=10.0)
        mock_client.request.assert_awaited_once_with("GET", "https://example.com")

    @pytest.mark.asyncio
    async def test_timeout_custom_passed_expected(self) -> None:
        """Verifies that safe_request passes custom timeout to httpx.AsyncClient."""
        from taipanstack.bridges.http_bridge import safe_request

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with (
            patch("taipanstack.bridges.http_bridge._HAS_HTTPX", True),
            patch(
                "taipanstack.bridges.http_bridge.guard_ssrf",
                return_value=Ok("https://example.com"),
            ),
            patch("taipanstack.bridges.http_bridge.httpx") as mock_httpx,
        ):
            mock_httpx.AsyncClient.return_value = mock_client
            result = await safe_request("GET", "https://example.com", timeout=5.0)

        assert isinstance(result, Ok)
        mock_httpx.AsyncClient.assert_called_once_with(timeout=5.0)
        mock_client.request.assert_awaited_once_with("GET", "https://example.com")

    @pytest.mark.asyncio
    async def test_no_httpx_returns_err_expected(self) -> None:
        """Returns Err when httpx is not installed."""
        from taipanstack.bridges.http_bridge import safe_request

        with patch("taipanstack.bridges.http_bridge._HAS_HTTPX", False):
            result = await safe_request("GET", "https://example.com")
        assert isinstance(result, Err)
        assert isinstance(result.err_value, ImportError)

    @pytest.mark.asyncio
    async def test_ssrf_blocks_private_ip_expected(self) -> None:
        """SSRF protection blocks requests to private IPs."""
        from taipanstack.bridges.http_bridge import safe_request

        with patch("taipanstack.bridges.http_bridge._HAS_HTTPX", True):
            result = await safe_request("GET", "http://127.0.0.1/admin")
        assert isinstance(result, Err)
        assert isinstance(result.err_value, SecurityError)

    @pytest.mark.asyncio
    async def test_ssrf_disabled_expected(self) -> None:
        """Requests pass when SSRF protection is disabled."""
        from taipanstack.bridges.http_bridge import safe_request

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with (
            patch("taipanstack.bridges.http_bridge._HAS_HTTPX", True),
            patch("taipanstack.bridges.http_bridge.httpx") as mock_httpx,
        ):
            mock_httpx.AsyncClient.return_value = mock_client
            result = await safe_request(
                "GET", "http://127.0.0.1/test", ssrf_protection=False
            )
        assert isinstance(result, Ok)

    @pytest.mark.asyncio
    async def test_ssrf_ok_path_calls_request_expected(self) -> None:
        """SSRF-enabled requests proceed when the guard returns Ok."""
        from taipanstack.bridges.http_bridge import safe_request

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with (
            patch("taipanstack.bridges.http_bridge._HAS_HTTPX", True),
            patch(
                "taipanstack.bridges.http_bridge.guard_ssrf",
                return_value=Ok("https://example.com"),
            ),
            patch("taipanstack.bridges.http_bridge.httpx") as mock_httpx,
        ):
            mock_httpx.AsyncClient.return_value = mock_client
            result = await safe_request("GET", "https://example.com")

        assert isinstance(result, Ok)
        mock_client.request.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_circuit_breaker_open_returns_err_expected(self) -> None:
        """Returns Err when circuit breaker is OPEN."""
        from taipanstack.bridges.http_bridge import safe_request

        breaker = CircuitBreaker(name="test", failure_threshold=1)
        # Trip the breaker
        breaker._record_failure(Exception("fail"))

        with patch("taipanstack.bridges.http_bridge._HAS_HTTPX", True):
            result = await safe_request(
                "GET",
                "https://example.com",
                ssrf_protection=False,
                circuit_breaker=breaker,
            )
        assert isinstance(result, Err)

    @pytest.mark.asyncio
    async def test_retry_on_server_error_expected(self) -> None:
        """Retries on 5xx status codes."""
        from taipanstack.bridges.http_bridge import safe_request

        response_500 = MagicMock()
        response_500.status_code = 500
        response_200 = MagicMock()
        response_200.status_code = 200

        call_count = 0

        async def fake_request(*a: object, **kw: object) -> MagicMock:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return response_500
            return response_200

        mock_client = AsyncMock()
        mock_client.request = fake_request
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with (
            patch("taipanstack.bridges.http_bridge._HAS_HTTPX", True),
            patch("taipanstack.bridges.http_bridge.httpx") as mock_httpx,
        ):
            mock_httpx.AsyncClient.return_value = mock_client
            result = await safe_request(
                "GET",
                "https://example.com",
                ssrf_protection=False,
                retry_config=RetryConfig(
                    max_attempts=2, initial_delay=0.01, max_delay=0.02, jitter=False
                ),
            )
        assert isinstance(result, Ok)
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_retry_on_connection_error_expected(self) -> None:
        """Retries on connection errors."""
        from taipanstack.bridges.http_bridge import safe_request

        response_200 = MagicMock()
        response_200.status_code = 200

        call_count = 0

        async def fake_request(*a: object, **kw: object) -> MagicMock:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ConnectionError("refused")
            return response_200

        mock_client = AsyncMock()
        mock_client.request = fake_request
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with (
            patch("taipanstack.bridges.http_bridge._HAS_HTTPX", True),
            patch("taipanstack.bridges.http_bridge.httpx") as mock_httpx,
        ):
            mock_httpx.AsyncClient.return_value = mock_client
            result = await safe_request(
                "GET",
                "https://example.com",
                ssrf_protection=False,
                retry_config=RetryConfig(
                    max_attempts=2, initial_delay=0.01, max_delay=0.02, jitter=False
                ),
            )
        assert isinstance(result, Ok)

    @pytest.mark.asyncio
    async def test_all_retries_fail_expected(self) -> None:
        """Returns Err when all retries are exhausted."""
        from taipanstack.bridges.http_bridge import safe_request

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(side_effect=ConnectionError("fail"))
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with (
            patch("taipanstack.bridges.http_bridge._HAS_HTTPX", True),
            patch("taipanstack.bridges.http_bridge.httpx") as mock_httpx,
        ):
            mock_httpx.AsyncClient.return_value = mock_client
            result = await safe_request(
                "GET",
                "https://example.com",
                ssrf_protection=False,
                retry_config=RetryConfig(
                    max_attempts=2, initial_delay=0.01, max_delay=0.02, jitter=False
                ),
            )
        assert isinstance(result, Err)

    @pytest.mark.asyncio
    async def test_zero_attempts_returns_runtime_error_expected(self) -> None:
        """A zero-attempt retry config returns a runtime error wrapper."""
        from taipanstack.bridges.http_bridge import safe_request

        result = await safe_request(
            "GET",
            "https://example.com",
            ssrf_protection=False,
            retry_config=RetryConfig(max_attempts=0, jitter=False),
        )

        assert isinstance(result, Err)
        assert isinstance(result.err_value, RuntimeError)
        assert str(result.err_value) == "Request failed"

    @pytest.mark.asyncio
    async def test_circuit_breaker_records_failure_on_request_exception_expected(
        self,
    ) -> None:
        """A closed circuit breaker records failures raised during the request."""
        from taipanstack.bridges.http_bridge import safe_request

        breaker = CircuitBreaker(name="record-http", failure_threshold=5)
        mock_client = AsyncMock()
        mock_client.request = AsyncMock(side_effect=ConnectionError("fail"))
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with (
            patch("taipanstack.bridges.http_bridge._HAS_HTTPX", True),
            patch("taipanstack.bridges.http_bridge.httpx") as mock_httpx,
        ):
            mock_httpx.AsyncClient.return_value = mock_client
            result = await safe_request(
                "GET",
                "https://example.com",
                ssrf_protection=False,
                circuit_breaker=breaker,
            )

        assert isinstance(result, Err)
        assert breaker.failure_count == 1


class TestSafeHttpClient:
    """Tests for the SafeHttpClient async context manager."""

    @pytest.mark.asyncio
    async def test_client_timeout_default_expected(self) -> None:
        """Verifies that SafeHttpClient uses a default timeout of 10.0."""
        from taipanstack.bridges.http_bridge import SafeHttpClient

        mock_client = AsyncMock()
        mock_client.aclose = AsyncMock()

        with (
            patch("taipanstack.bridges.http_bridge._HAS_HTTPX", True),
            patch("taipanstack.bridges.http_bridge.httpx") as mock_httpx,
        ):
            mock_httpx.AsyncClient.return_value = mock_client

            async with SafeHttpClient(ssrf_protection=False):
                assert True

        mock_httpx.AsyncClient.assert_called_once_with(timeout=10.0)

    @pytest.mark.asyncio
    async def test_no_httpx_raises_expected(self) -> None:
        """Entering the context raises ImportError without httpx."""
        from taipanstack.bridges.http_bridge import SafeHttpClient

        with patch("taipanstack.bridges.http_bridge._HAS_HTTPX", False):
            with pytest.raises(ImportError):
                async with SafeHttpClient():
                    assert True

    @pytest.mark.asyncio
    async def test_lifecycle_expected(self) -> None:
        """Client opens and closes properly."""
        from taipanstack.bridges.http_bridge import SafeHttpClient

        mock_client = AsyncMock()
        mock_client.aclose = AsyncMock()

        with (
            patch("taipanstack.bridges.http_bridge._HAS_HTTPX", True),
            patch("taipanstack.bridges.http_bridge.httpx") as mock_httpx,
        ):
            mock_httpx.AsyncClient.return_value = mock_client

            async with SafeHttpClient(ssrf_protection=False) as client:
                assert client._client is not None

        mock_client.aclose.assert_called_once()

    @pytest.mark.asyncio
    async def test_request_without_context_returns_err_expected(self) -> None:
        """Request without entering context returns Err."""
        from taipanstack.bridges.http_bridge import SafeHttpClient

        client = SafeHttpClient()
        result = await client.request("GET", "https://example.com")
        assert isinstance(result, Err)
        assert "not initialised" in str(result.err_value)

    @pytest.mark.asyncio
    async def test_get_post_put_delete_patch_expected(self) -> None:
        """Convenience methods delegate to request."""
        from taipanstack.bridges.http_bridge import SafeHttpClient

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_response)
        mock_client.aclose = AsyncMock()

        with (
            patch("taipanstack.bridges.http_bridge._HAS_HTTPX", True),
            patch("taipanstack.bridges.http_bridge.httpx") as mock_httpx,
        ):
            mock_httpx.AsyncClient.return_value = mock_client

            async with SafeHttpClient(ssrf_protection=False) as client:
                for method in ("get", "post", "put", "delete", "patch"):
                    result = await getattr(client, method)("https://example.com")
                    assert isinstance(result, Ok)

    @pytest.mark.asyncio
    async def test_ssrf_blocks_in_client_expected(self) -> None:
        """SSRF protection blocks requests in the client."""
        from taipanstack.bridges.http_bridge import SafeHttpClient

        mock_client = AsyncMock()
        mock_client.aclose = AsyncMock()

        with (
            patch("taipanstack.bridges.http_bridge._HAS_HTTPX", True),
            patch("taipanstack.bridges.http_bridge.httpx") as mock_httpx,
        ):
            mock_httpx.AsyncClient.return_value = mock_client

            async with SafeHttpClient(ssrf_protection=True) as client:
                result = await client.get("http://127.0.0.1/admin")
            assert isinstance(result, Err)

    @pytest.mark.asyncio
    async def test_client_ssrf_ok_path_calls_request_expected(self) -> None:
        """SSRF-enabled client requests proceed when the guard returns Ok."""
        from taipanstack.bridges.http_bridge import SafeHttpClient

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_response)
        mock_client.aclose = AsyncMock()

        with (
            patch("taipanstack.bridges.http_bridge._HAS_HTTPX", True),
            patch(
                "taipanstack.bridges.http_bridge.guard_ssrf",
                return_value=Ok("https://example.com"),
            ),
            patch("taipanstack.bridges.http_bridge.httpx") as mock_httpx,
        ):
            mock_httpx.AsyncClient.return_value = mock_client

            async with SafeHttpClient(ssrf_protection=True) as client:
                result = await client.get("https://example.com")

        assert isinstance(result, Ok)
        mock_client.request.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_client_retry_on_status_expected(self) -> None:
        """Client retries on retryable status codes."""
        from taipanstack.bridges.http_bridge import SafeHttpClient

        response_503 = MagicMock()
        response_503.status_code = 503
        response_200 = MagicMock()
        response_200.status_code = 200

        call_count = 0

        async def fake_request(*a: object, **kw: object) -> MagicMock:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return response_503
            return response_200

        mock_client = AsyncMock()
        mock_client.request = fake_request
        mock_client.aclose = AsyncMock()

        with (
            patch("taipanstack.bridges.http_bridge._HAS_HTTPX", True),
            patch("taipanstack.bridges.http_bridge.httpx") as mock_httpx,
        ):
            mock_httpx.AsyncClient.return_value = mock_client

            async with SafeHttpClient(
                ssrf_protection=False,
                retry_config=RetryConfig(
                    max_attempts=2, initial_delay=0.01, max_delay=0.02, jitter=False
                ),
            ) as client:
                result = await client.get("https://example.com")

        assert isinstance(result, Ok)

    @pytest.mark.asyncio
    async def test_client_retry_on_exception_expected(self) -> None:
        """Client retries on connection exceptions."""
        from taipanstack.bridges.http_bridge import SafeHttpClient

        response_200 = MagicMock()
        response_200.status_code = 200

        call_count = 0

        async def fake_request(*a: object, **kw: object) -> MagicMock:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ConnectionError("refused")
            return response_200

        mock_client = AsyncMock()
        mock_client.request = fake_request
        mock_client.aclose = AsyncMock()

        with (
            patch("taipanstack.bridges.http_bridge._HAS_HTTPX", True),
            patch("taipanstack.bridges.http_bridge.httpx") as mock_httpx,
        ):
            mock_httpx.AsyncClient.return_value = mock_client

            async with SafeHttpClient(
                ssrf_protection=False,
                retry_config=RetryConfig(
                    max_attempts=2, initial_delay=0.01, max_delay=0.02, jitter=False
                ),
            ) as client:
                result = await client.get("https://example.com")

        assert isinstance(result, Ok)

    @pytest.mark.asyncio
    async def test_client_breaker_integration_expected(self) -> None:
        """Client respects circuit breaker state."""
        from taipanstack.bridges.http_bridge import SafeHttpClient

        breaker = CircuitBreaker(name="http", failure_threshold=1)
        breaker._record_failure(Exception("trip"))

        mock_client = AsyncMock()
        mock_client.aclose = AsyncMock()

        with (
            patch("taipanstack.bridges.http_bridge._HAS_HTTPX", True),
            patch("taipanstack.bridges.http_bridge.httpx") as mock_httpx,
        ):
            mock_httpx.AsyncClient.return_value = mock_client

            async with SafeHttpClient(
                ssrf_protection=False,
                circuit_breaker=breaker,
            ) as client:
                result = await client.get("https://example.com")

        assert isinstance(result, Err)

    @pytest.mark.asyncio
    async def test_client_all_retries_fail_expected(self) -> None:
        """Client returns Err when all retries exhausted."""
        from taipanstack.bridges.http_bridge import SafeHttpClient

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(side_effect=ConnectionError("fail"))
        mock_client.aclose = AsyncMock()

        breaker = CircuitBreaker(name="http_fail", failure_threshold=10)

        with (
            patch("taipanstack.bridges.http_bridge._HAS_HTTPX", True),
            patch("taipanstack.bridges.http_bridge.httpx") as mock_httpx,
        ):
            mock_httpx.AsyncClient.return_value = mock_client

            async with SafeHttpClient(
                ssrf_protection=False,
                retry_config=RetryConfig(
                    max_attempts=2, initial_delay=0.01, max_delay=0.02, jitter=False
                ),
                circuit_breaker=breaker,
            ) as client:
                result = await client.get("https://example.com")

        assert isinstance(result, Err)

    @pytest.mark.asyncio
    async def test_client_zero_attempts_returns_runtime_error_expected(self) -> None:
        """Client returns a runtime error wrapper when retries are disabled."""
        from taipanstack.bridges.http_bridge import SafeHttpClient

        mock_client = AsyncMock()
        mock_client.aclose = AsyncMock()

        with (
            patch("taipanstack.bridges.http_bridge._HAS_HTTPX", True),
            patch("taipanstack.bridges.http_bridge.httpx") as mock_httpx,
        ):
            mock_httpx.AsyncClient.return_value = mock_client

            async with SafeHttpClient(
                ssrf_protection=False,
                retry_config=RetryConfig(max_attempts=0, jitter=False),
            ) as client:
                result = await client.get("https://example.com")

        assert isinstance(result, Err)
        assert isinstance(result.err_value, RuntimeError)
        assert str(result.err_value) == "Request failed"

    @pytest.mark.asyncio
    async def test_aexit_without_client_is_noop_expected(self) -> None:
        """Exiting without an initialised client is a no-op."""
        from taipanstack.bridges.http_bridge import SafeHttpClient

        client = SafeHttpClient()

        await client.__aexit__(None, None, None)

        assert client._client is None


def test_bridge_http_http_bridge_import_error_coverage_expected() -> None:
    """Test http_bridge import error fallback branches."""
    import importlib
    import sys

    original_httpx = sys.modules.pop("httpx", None)
    sys.modules["httpx"] = None  # type: ignore
    try:
        import taipanstack.bridges.http_bridge as http_mod

        importlib.reload(http_mod)
        assert http_mod._HAS_HTTPX is False
    finally:
        if original_httpx is not None:
            sys.modules["httpx"] = original_httpx
        else:
            sys.modules.pop("httpx", None)
        importlib.reload(http_mod)

def test_bridge_http_import_error_coverage_expected():
    import importlib
    import sys

    sys.modules.get("taipanstack.bridges.http_bridge")
    original_httpx = sys.modules.pop("httpx", None)

    try:
        sys.modules["httpx"] = None

        from taipanstack.bridges import http_bridge
        importlib.reload(http_bridge)

        assert http_bridge._HAS_HTTPX is False
    finally:
        if original_httpx is not None:
            sys.modules["httpx"] = original_httpx
        else:
            sys.modules.pop("httpx", None)

        importlib.reload(http_bridge)

def test_bridge_http_success_coverage_expected():
    import importlib
    import sys
    from unittest.mock import MagicMock

    sys.modules.get("taipanstack.bridges.http_bridge")
    original_httpx = sys.modules.pop("httpx", None)

    try:
        sys.modules["httpx"] = MagicMock()

        from taipanstack.bridges import http_bridge
        importlib.reload(http_bridge)

        assert http_bridge._HAS_HTTPX is True
    finally:
        if original_httpx is not None:
            sys.modules["httpx"] = original_httpx
        else:
            sys.modules.pop("httpx", None)

        importlib.reload(http_bridge)
