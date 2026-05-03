"""Chaos tests for the HTTP Bridge."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.core.result import Err, Ok


@pytest.mark.asyncio
async def test_chaos_http_bridge_safe_client_exception_extreme() -> None:
    """Simulate a severe exception thrown during safe client initialization."""
    from taipanstack.bridges.http_bridge import SafeHttpClient

    with patch("taipanstack.bridges.http_bridge.httpx") as mock_httpx:
        # Simulate extreme unexpected exception type during AsyncClient instantiation
        mock_httpx.AsyncClient.side_effect = MemoryError("OOM")

        with pytest.raises(MemoryError):
            async with SafeHttpClient():
                pass


@pytest.mark.asyncio
async def test_chaos_http_bridge_request_extreme_delay() -> None:
    """Test HTTP bridge handles extreme delays simulating stuck network."""
    from taipanstack.bridges.http_bridge import SafeHttpClient

    async def stuck_request(*args, **kwargs):
        # We don't want to actually sleep forever in the test, so we just raise
        # TimeoutError directly, but we want to simulate the behavior as if it
        # took a long time.
        raise TimeoutError("Stuck")

    mock_client = AsyncMock()
    mock_client.request = stuck_request
    mock_client.aclose = AsyncMock()

    with (
        patch("taipanstack.bridges.http_bridge._HAS_HTTPX", True),
        patch("taipanstack.bridges.http_bridge.httpx") as mock_httpx,
    ):
        mock_httpx.AsyncClient.return_value = mock_client

        async with SafeHttpClient(ssrf_protection=False) as client:
            result = await client.get("https://example.com")

    assert isinstance(result, Err)
    assert isinstance(result.err_value, TimeoutError)

@settings(
    suppress_health_check=[
        HealthCheck.large_base_example,
        HealthCheck.data_too_large,
        HealthCheck.too_slow,
        HealthCheck.function_scoped_fixture,
    ],
    deadline=None,
    max_examples=50
)
@given(
    url=st.text(min_size=1000, max_size=8000),
    method=st.sampled_from(["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD", "\x00", "B" * 50000]),
)
def test_fuzz_http_bridge_malformed_inputs(url: str, method: str) -> None:
    """Fuzz HTTP bridge with massive strings for URL and methods to ensure no crashes."""
    from taipanstack.bridges.http_bridge import safe_request

    async def run_test():
        with (
            patch("taipanstack.bridges.http_bridge._HAS_HTTPX", True),
            patch("taipanstack.bridges.http_bridge._check_ssrf", return_value=Ok(None)),
            patch("taipanstack.bridges.http_bridge.httpx") as mock_httpx,
        ):
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_client.request = AsyncMock(return_value=mock_response)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=False)

            mock_httpx.AsyncClient.return_value = mock_client

            result = await safe_request(method, url, ssrf_protection=False)

            # Should either be Ok or Err, but no unhandled exceptions
            assert isinstance(result, (Ok, Err))

    asyncio.run(run_test())
