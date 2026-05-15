"""
Web Bridge — ASGI middleware for rate limiting and security headers.

Provides a framework-agnostic ASGI middleware that integrates
TaipanStack's rate limiter and security headers into any ASGI
application (FastAPI, Litestar, Starlette, etc.).
"""

from __future__ import annotations

import json
import logging
from collections.abc import Awaitable, Callable, MutableMapping
from dataclasses import dataclass
from typing import TypeAlias, TypeVar

from taipanstack.core.result import Ok, Result
from taipanstack.utils.rate_limit import RateLimiter

logger = logging.getLogger("taipanstack.bridges.web")

T = TypeVar("T")

# ASGI type aliases
Scope: TypeAlias = MutableMapping[str, object]
Receive: TypeAlias = Callable[[], Awaitable[MutableMapping[str, object]]]
Send: TypeAlias = Callable[[MutableMapping[str, object]], Awaitable[None]]
ASGIApp: TypeAlias = Callable[[Scope, Receive, Send], Awaitable[None]]


@dataclass(frozen=True)
class SecurityHeadersConfig:
    """Configuration for security response headers.

    Attributes:
        x_content_type_options: Value for X-Content-Type-Options.
        x_frame_options: Value for X-Frame-Options.
        x_xss_protection: Value for X-XSS-Protection.
        strict_transport_security: Value for Strict-Transport-Security.
        referrer_policy: Value for Referrer-Policy.
        content_security_policy: Value for Content-Security-Policy.

    """

    x_content_type_options: str = "nosniff"
    x_frame_options: str = "DENY"
    x_xss_protection: str = "1; mode=block"
    strict_transport_security: str = "max-age=31536000; includeSubDomains"
    referrer_policy: str = "strict-origin-when-cross-origin"
    content_security_policy: str = "default-src 'self'"

    def to_headers(self) -> list[tuple[bytes, bytes]]:
        """Convert config to ASGI header pairs.

        Returns:
            List of (name, value) byte tuples.

        """
        return [
            (b"x-content-type-options", self.x_content_type_options.encode()),
            (b"x-frame-options", self.x_frame_options.encode()),
            (b"x-xss-protection", self.x_xss_protection.encode()),
            (
                b"strict-transport-security",
                self.strict_transport_security.encode(),
            ),
            (b"referrer-policy", self.referrer_policy.encode()),
            (b"content-security-policy", self.content_security_policy.encode()),
        ]


def result_to_response(
    result: Result[T, Exception],
    *,
    status_ok: int = 200,
    status_err: int = 500,
) -> dict[str, object]:
    """Convert a ``Result`` to a JSON-friendly response dict.

    Args:
        result: The Result to convert.
        status_ok: HTTP status for ``Ok`` values.
        status_err: HTTP status for ``Err`` values.

    Returns:
        Dict with ``status``, ``data``/``error`` keys.

    Example:
        >>> result_to_response(Ok({"id": 1}))
        {"status": 200, "data": {"id": 1}}

    """
    if isinstance(result, Ok):
        return {"status": status_ok, "data": result.ok_value}
    return {"status": status_err, "error": str(result.err_value)}


async def _send_json_response(
    send: Send,
    *,
    status: int,
    body: dict[str, object],
    extra_headers: list[tuple[bytes, bytes]] | None = None,
) -> None:
    """Send a JSON response via ASGI send.

    Args:
        send: ASGI send callable.
        status: HTTP status code.
        body: JSON-serializable body.
        extra_headers: Additional headers to include.

    """
    payload = json.dumps(body).encode("utf-8")
    headers: list[tuple[bytes, bytes]] = [
        (b"content-type", b"application/json"),
        (b"content-length", str(len(payload)).encode()),
    ]
    if extra_headers:
        headers.extend(extra_headers)

    await send(
        {
            "type": "http.response.start",
            "status": status,
            "headers": headers,
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": payload,
        }
    )


class TaipanMiddleware:
    """ASGI middleware providing rate limiting and security headers.

    Args:
        app: The wrapped ASGI application.
        rate_limiter: Optional rate limiter instance.
        security_headers: Whether to inject security headers.
        headers_config: Custom security headers configuration.

    Example:
        >>> from taipanstack.utils.rate_limit import RateLimiter
        >>> app = TaipanMiddleware(
        ...     my_asgi_app,
        ...     rate_limiter=RateLimiter(max_calls=100, time_window=60),
        ...     security_headers=True,
        ... )

    """

    def __init__(
        self,
        app: ASGIApp,
        *,
        rate_limiter: RateLimiter | None = None,
        security_headers: bool = True,
        headers_config: SecurityHeadersConfig | None = None,
    ) -> None:
        """Initialize the middleware.

        Args:
            app: ASGI application to wrap.
            rate_limiter: Optional rate limiter.
            security_headers: Inject security headers.
            headers_config: Custom headers config.

        """
        self._app = app
        self._rate_limiter = rate_limiter
        self._security_headers = security_headers
        self._headers_config = headers_config or SecurityHeadersConfig()

    def _wrap_send_with_security_headers(self, send: Send) -> Send:
        """Wrap the send callable to inject security headers if enabled.

        Args:
            send: The original ASGI send callable.

        Returns:
            The wrapped ASGI send callable.

        """
        if not self._security_headers:
            return send

        extra_headers = self._headers_config.to_headers()

        async def send_with_headers(message: MutableMapping[str, object]) -> None:
            if message.get("type") == "http.response.start":
                headers = message.get("headers")
                existing = list(headers) if isinstance(headers, list) else []
                existing.extend(extra_headers)
                message["headers"] = existing
            await send(message)

        return send_with_headers

    async def _handle_rate_limit(self, send: Send) -> bool:
        """Apply rate limiting and send response if exceeded.

        Args:
            send: ASGI send callable.

        Returns:
            True if rate limit was exceeded, False otherwise.

        """
        if self._rate_limiter is None or self._rate_limiter.consume():
            return False

        logger.warning("Rate limit exceeded for request")
        security_hdrs = (
            self._headers_config.to_headers() if self._security_headers else None
        )
        await _send_json_response(
            send,
            status=429,
            body={"error": "Rate limit exceeded", "retry_after": 1},
            extra_headers=security_hdrs,
        )
        return True

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        """Process an ASGI request.

        Args:
            scope: ASGI scope dict.
            receive: ASGI receive callable.
            send: ASGI send callable.

        """
        # Only handle HTTP requests
        if scope.get("type") != "http":
            await self._app(scope, receive, send)
            return

        # Rate limiting
        if await self._handle_rate_limit(send):
            return

        # Wrap send to inject security headers
        send = self._wrap_send_with_security_headers(send)

        # Call the actual application
        try:
            await self._app(scope, receive, send)
        except Exception as exc:
            logger.exception("Unhandled exception in ASGI app", exc_info=exc)
            await _send_json_response(
                send,
                status=500,
                body={"error": "Internal server error"},
            )
