"""Tests for the Web Bridge ASGI middleware."""

import json
from typing import Any
from unittest.mock import AsyncMock

import pytest

from taipanstack.bridges.web_bridge import (
    SecurityHeadersConfig,
    TaipanMiddleware,
    _send_json_response,
    result_to_response,
)
from taipanstack.core.result import Err, Ok
from taipanstack.utils.rate_limit import RateLimiter

# --- helpers ----------------------------------------------------------------


async def _make_dummy_app(
    scope: dict[str, Any],
    receive: Any,
    send: Any,
) -> None:
    """Minimal ASGI app that returns 200 OK."""
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"text/plain")],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": b"OK",
        }
    )


async def _make_crashing_app(
    scope: dict[str, Any],
    receive: Any,
    send: Any,
) -> None:
    """ASGI app that raises an unhandled exception."""
    msg = "boom"
    raise RuntimeError(msg)


class _ResponseCapture:
    """Capture ASGI send messages."""

    def __init__(self) -> None:
        self.messages: list[dict[str, Any]] = []

    async def __call__(self, message: dict[str, Any]) -> None:
        self.messages.append(message)

    @property
    def status(self) -> int | None:
        """Extract the HTTP status code."""
        for m in self.messages:
            if m.get("type") == "http.response.start":
                return m.get("status")  # type: ignore[return-value]
        return None

    @property
    def body(self) -> bytes:
        """Extract the response body."""
        for m in self.messages:
            if m.get("type") == "http.response.body":
                return m.get("body", b"")  # type: ignore[return-value]
        return b""

    @property
    def headers(self) -> dict[str, str]:
        """Extract all response headers as a dict."""
        result: dict[str, str] = {}
        for m in self.messages:
            if m.get("type") == "http.response.start":
                for name, value in m.get("headers", []):
                    result[name.decode()] = value.decode()
        return result


# --- result_to_response -----------------------------------------------------


class TestResultToResponse:
    """Tests for result_to_response."""

    def test_bridge_web_ok_value_expected(self) -> None:
        """Ok result produces status 200 and data."""
        resp = result_to_response(Ok({"id": 1}))
        assert resp["status"] == 200
        assert resp["data"] == {"id": 1}

    def test_bridge_web_err_value_expected(self) -> None:
        """Err result produces status 500 and error string."""
        resp = result_to_response(Err(ValueError("bad")))
        assert resp["status"] == 500
        assert "bad" in resp["error"]

    def test_bridge_web_custom_status_codes_expected(self) -> None:
        """Custom status codes are respected."""
        resp = result_to_response(Ok("yes"), status_ok=201)
        assert resp["status"] == 201

        resp_err = result_to_response(Err(RuntimeError("x")), status_err=422)
        assert resp_err["status"] == 422


# --- SecurityHeadersConfig ---------------------------------------------------


class TestSecurityHeadersConfig:
    """Tests for SecurityHeadersConfig."""

    def test_bridge_web_default_headers_expected(self) -> None:
        """Default config produces all 6 security headers."""
        config = SecurityHeadersConfig()
        headers = config.to_headers()
        assert len(headers) == 6
        names = [h[0] for h in headers]
        assert b"x-content-type-options" in names
        assert b"x-frame-options" in names

    def test_bridge_web_custom_values_expected(self) -> None:
        """Custom values are reflected in output."""
        config = SecurityHeadersConfig(x_frame_options="SAMEORIGIN")
        headers = dict(config.to_headers())
        assert headers[b"x-frame-options"] == b"SAMEORIGIN"


# --- TaipanMiddleware ---------------------------------------------------------


class TestTaipanMiddleware:
    """Tests for the ASGI middleware."""

    @pytest.mark.asyncio
    async def test_bridge_web_passthrough_http_expected(self) -> None:
        """HTTP requests pass through to the app."""
        mw = TaipanMiddleware(_make_dummy_app, security_headers=False)
        capture = _ResponseCapture()

        await mw({"type": "http"}, AsyncMock(), capture)
        assert capture.status == 200

    @pytest.mark.asyncio
    async def test_bridge_web_passthrough_non_http_expected(self) -> None:
        """Non-HTTP requests (e.g. websocket) pass through unchanged."""
        called = False

        async def ws_app(scope: Any, receive: Any, send: Any) -> None:
            nonlocal called
            called = True

        mw = TaipanMiddleware(ws_app)
        await mw({"type": "websocket"}, AsyncMock(), AsyncMock())
        assert called

    @pytest.mark.asyncio
    async def test_bridge_web_rate_limit_returns_429_expected(self) -> None:
        """429 when rate limit is exceeded."""
        limiter = RateLimiter(max_calls=1, time_window=60.0)
        mw = TaipanMiddleware(
            _make_dummy_app,
            rate_limiter=limiter,
            security_headers=False,
        )

        # First request — passes
        cap1 = _ResponseCapture()
        await mw({"type": "http"}, AsyncMock(), cap1)
        assert cap1.status == 200

        # Second request — rate limited
        cap2 = _ResponseCapture()
        await mw({"type": "http"}, AsyncMock(), cap2)
        assert cap2.status == 429
        body = json.loads(cap2.body)
        assert "Rate limit" in body["error"]

    @pytest.mark.asyncio
    async def test_bridge_web_security_headers_injected_expected(self) -> None:
        """Security headers are added to responses."""
        mw = TaipanMiddleware(_make_dummy_app, security_headers=True)
        capture = _ResponseCapture()

        await mw({"type": "http"}, AsyncMock(), capture)
        headers = capture.headers
        assert headers.get("x-content-type-options") == "nosniff"
        assert headers.get("x-frame-options") == "DENY"

    @pytest.mark.asyncio
    async def test_bridge_web_security_headers_on_429_expected(self) -> None:
        """Security headers are also on 429 responses."""
        limiter = RateLimiter(max_calls=1, time_window=60.0)
        mw = TaipanMiddleware(
            _make_dummy_app,
            rate_limiter=limiter,
            security_headers=True,
        )
        # Drain the single token so next request is rate-limited
        limiter.consume()
        capture = _ResponseCapture()
        await mw({"type": "http"}, AsyncMock(), capture)
        assert capture.status == 429
        assert "x-content-type-options" in capture.headers

    @pytest.mark.asyncio
    async def test_bridge_web_unhandled_exception_returns_500_expected(self) -> None:
        """Unhandled exceptions produce a 500 JSON response."""
        mw = TaipanMiddleware(
            _make_crashing_app,
            security_headers=False,
        )
        capture = _ResponseCapture()

        await mw({"type": "http"}, AsyncMock(), capture)
        assert capture.status == 500
        body = json.loads(capture.body)
        assert "Internal server error" in body["error"]


# --- _send_json_response -----------------------------------------------------


class TestSendJsonResponse:
    """Tests for _send_json_response helper."""

    @pytest.mark.asyncio
    async def test_bridge_web_sends_json_expected(self) -> None:
        """Sends a valid JSON response."""
        capture = _ResponseCapture()
        await _send_json_response(
            capture,
            status=201,
            body={"created": True},
        )
        assert capture.status == 201
        parsed = json.loads(capture.body)
        assert parsed["created"] is True

    @pytest.mark.asyncio
    async def test_bridge_web_extra_headers_expected(self) -> None:
        """Extra headers are included."""
        capture = _ResponseCapture()
        await _send_json_response(
            capture,
            status=200,
            body={"ok": True},
            extra_headers=[(b"x-custom", b"value")],
        )
        assert capture.headers.get("x-custom") == "value"


def test_send_json_response_err() -> None:
    import asyncio

    from taipanstack.core.result import Err

    async def run_test():
        class MockSend:
            called = False

            async def __call__(self, message):
                self.called = True

        from taipanstack.bridges.web_bridge import result_to_response

        result_to_response(Err(ValueError("err")))

    asyncio.run(run_test())
