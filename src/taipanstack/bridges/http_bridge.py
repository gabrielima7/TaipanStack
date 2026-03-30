"""
HTTP Bridge — safe httpx client with SSRF protection and resilience.

Wraps ``httpx.AsyncClient`` with TaipanStack's ``guard_ssrf``,
retry, and circuit breaker integrations.  All outbound URLs are
validated against SSRF before the request is sent.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import Any

from taipanstack.core.result import Err, Ok, Result
from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
)
from taipanstack.resilience.retry import RetryConfig, calculate_delay
from taipanstack.security.guards import guard_ssrf

logger = logging.getLogger("taipanstack.bridges.http")

# --- optional httpx import ------------------------------------------------

try:
    import httpx

    _HAS_HTTPX = True  # pragma: no cover
except ImportError:  # pragma: no cover
    httpx = None  # type: ignore[assignment]
    _HAS_HTTPX = False

# Default status codes that trigger a retry
_RETRYABLE_STATUS_CODES: frozenset[int] = frozenset({500, 502, 503, 504, 429})


def _check_circuit_breaker(
    circuit_breaker: CircuitBreaker,
) -> CircuitBreakerError | None:
    """Check circuit breaker state and return error if OPEN.

    Args:
        circuit_breaker: The circuit breaker to check.

    Returns:
        ``CircuitBreakerError`` if open, ``None`` otherwise.

    """
    if not circuit_breaker._should_attempt():
        return CircuitBreakerError(
            f"Circuit '{circuit_breaker.name}' is open",
            state=circuit_breaker.state,
        )
    return None


def _check_ssrf(url: str, ssrf_protection: bool) -> Result[None, Exception]:
    """Validate URL against SSRF if protection is enabled.

    Args:
        url: The URL to validate.
        ssrf_protection: Whether SSRF protection is enabled.

    Returns:
        ``Ok(None)`` if valid or protection disabled, ``Err(Exception)`` otherwise.

    """
    if not ssrf_protection:
        return Ok(None)

    ssrf_result = guard_ssrf(url)
    match ssrf_result:
        case Err(security_err):
            return Err(security_err)
        case Ok():  # pragma: no branch
            return Ok(None)


async def _execute_with_retries(
    request_func: Callable[[], Awaitable[Any]],
    retry_config: RetryConfig | None,
    circuit_breaker: CircuitBreaker | None,
    retryable_status_codes: frozenset[int],
) -> Result[Any, Exception]:
    """Execute a request function with optional retries and circuit breaker.

    Args:
        request_func: Async callable that performs the request.
        retry_config: Optional retry configuration.
        circuit_breaker: Optional circuit breaker.
        retryable_status_codes: Status codes to retry on.

    Returns:
        ``Ok(Response)`` on success, ``Err`` on failure.

    """
    max_attempts = 1
    if retry_config is not None:
        max_attempts = retry_config.max_attempts

    last_error: Exception | None = None

    for attempt in range(1, max_attempts + 1):
        try:
            response = await request_func()

            # Check if we should retry on status code
            if (
                retry_config is not None
                and response.status_code in retryable_status_codes
                and attempt < max_attempts
            ):
                delay = calculate_delay(attempt, retry_config)
                await asyncio.sleep(delay)
                continue

            return Ok(response)

        except Exception as exc:
            last_error = exc
            if circuit_breaker is not None:  # pragma: no branch
                circuit_breaker._record_failure(exc)
            if retry_config is not None and attempt < max_attempts:
                delay = calculate_delay(attempt, retry_config)
                await asyncio.sleep(delay)
                continue
            break

    return Err(last_error or RuntimeError("Request failed"))


async def safe_request(
    method: str,
    url: str,
    *,
    ssrf_protection: bool = True,
    retry_config: RetryConfig | None = None,
    circuit_breaker: CircuitBreaker | None = None,
    retryable_status_codes: frozenset[int] = _RETRYABLE_STATUS_CODES,
    **kwargs: Any,
) -> Result[Any, Exception]:
    """Perform a one-shot HTTP request with safety features.

    Args:
        method: HTTP method (GET, POST, etc.).
        url: Target URL.
        ssrf_protection: Validate URL against SSRF.
        retry_config: Optional retry configuration.
        circuit_breaker: Optional circuit breaker.
        retryable_status_codes: Status codes that trigger retries.
        **kwargs: Passed to ``httpx.AsyncClient.request``.

    Returns:
        ``Ok(Response)`` on success, ``Err`` on failure.

    """
    if not _HAS_HTTPX:
        return Err(
            ImportError(
                "httpx is required for HTTP bridge. "
                "Install with: pip install taipanstack[bridges-http]"
            )
        )

    # SSRF check
    ssrf_check = _check_ssrf(url, ssrf_protection)
    if isinstance(ssrf_check, Err):
        return ssrf_check

    # Circuit breaker gate
    if circuit_breaker is not None:
        cb_err = _check_circuit_breaker(circuit_breaker)
        if cb_err is not None:
            return Err(cb_err)

    async def _do_request() -> Any:
        async with httpx.AsyncClient() as client:
            return await client.request(method, url, **kwargs)

    return await _execute_with_retries(
        _do_request,
        retry_config,
        circuit_breaker,
        retryable_status_codes,
    )


class SafeHttpClient:
    """Async context manager wrapping httpx with TaipanStack safety.

    Args:
        ssrf_protection: Enable SSRF validation on all requests.
        retry_config: Retry configuration for transient failures.
        circuit_breaker: Optional circuit breaker for all requests.
        retryable_status_codes: HTTP status codes to retry on.
        **client_kwargs: Passed to ``httpx.AsyncClient``.

    Example:
        >>> async with SafeHttpClient() as client:
        ...     result = await client.get("https://api.example.com/data")
        ...     match result:
        ...         case Ok(response): print(response.json())
        ...         case Err(e): print(f"Error: {e}")

    """

    def __init__(
        self,
        *,
        ssrf_protection: bool = True,
        retry_config: RetryConfig | None = None,
        circuit_breaker: CircuitBreaker | None = None,
        retryable_status_codes: frozenset[int] = _RETRYABLE_STATUS_CODES,
        **client_kwargs: Any,
    ) -> None:
        """Initialize the safe HTTP client.

        Args:
            ssrf_protection: Enable SSRF validation.
            retry_config: Retry configuration.
            circuit_breaker: Circuit breaker instance.
            retryable_status_codes: Status codes to retry.
            **client_kwargs: Keyword args for httpx.AsyncClient.

        """
        self._ssrf_protection = ssrf_protection
        self._retry_config = retry_config
        self._circuit_breaker = circuit_breaker
        self._retryable_status_codes = retryable_status_codes
        self._client_kwargs = client_kwargs
        self._client: Any = None

    async def __aenter__(self) -> SafeHttpClient:
        """Enter the async context manager."""
        if not _HAS_HTTPX:
            msg = (
                "httpx is required for SafeHttpClient. "
                "Install with: pip install taipanstack[bridges-http]"
            )
            raise ImportError(msg)
        self._client = httpx.AsyncClient(**self._client_kwargs)
        return self

    async def __aexit__(
        self,
        _exc_type: type[BaseException] | None,
        _exc_val: BaseException | None,
        _exc_tb: Any,
    ) -> None:
        """Exit the async context manager."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def request(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> Result[Any, Exception]:
        """Send an HTTP request with safety features.

        Args:
            method: HTTP method.
            url: Target URL.
            **kwargs: Passed to the underlying client.

        Returns:
            ``Ok(Response)`` on success, ``Err`` on failure.

        """
        if self._client is None:
            return Err(RuntimeError("Client not initialised. Use 'async with'."))

        # SSRF check
        ssrf_check = _check_ssrf(url, self._ssrf_protection)
        if isinstance(ssrf_check, Err):
            return ssrf_check

        # Circuit breaker gate
        if self._circuit_breaker is not None:
            cb_err = _check_circuit_breaker(self._circuit_breaker)
            if cb_err is not None:
                return Err(cb_err)

        async def _do_request() -> Any:
            return await self._client.request(method, url, **kwargs)

        return await _execute_with_retries(
            _do_request,
            self._retry_config,
            self._circuit_breaker,
            self._retryable_status_codes,
        )

    async def get(self, url: str, **kw: Any) -> Result[Any, Exception]:
        """Send a GET request."""
        return await self.request("GET", url, **kw)

    async def post(self, url: str, **kw: Any) -> Result[Any, Exception]:
        """Send a POST request."""
        return await self.request("POST", url, **kw)

    async def put(self, url: str, **kw: Any) -> Result[Any, Exception]:
        """Send a PUT request."""
        return await self.request("PUT", url, **kw)

    async def delete(self, url: str, **kw: Any) -> Result[Any, Exception]:
        """Send a DELETE request."""
        return await self.request("DELETE", url, **kw)

    async def patch(self, url: str, **kw: Any) -> Result[Any, Exception]:
        """Send a PATCH request."""
        return await self.request("PATCH", url, **kw)
