"""Taipan Bridges — universal integration layer.

Provides adapters connecting TaipanStack's security, resilience,
and error handling with popular Python libraries.

Sub-modules:
    http_bridge: Safe httpx client with SSRF protection.
    web_bridge:  ASGI middleware for rate limiting / security headers.
    db_bridge:   Resilient SQLAlchemy / Redis wrappers.
"""

from taipanstack.bridges._imports import get_attr_or_err, require_dependency
from taipanstack.bridges.db_bridge import ResilientDatabase, ResilientRedis
from taipanstack.bridges.http_bridge import SafeHttpClient, safe_request
from taipanstack.bridges.web_bridge import (
    SecurityHeadersConfig,
    TaipanMiddleware,
    result_to_response,
)

__all__ = (
    "ResilientDatabase",
    "ResilientRedis",
    "SafeHttpClient",
    "SecurityHeadersConfig",
    "TaipanMiddleware",
    "get_attr_or_err",
    "require_dependency",
    "result_to_response",
    "safe_request",
)
