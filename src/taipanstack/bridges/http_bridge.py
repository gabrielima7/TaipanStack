"""
HTTP Bridge — safe httpx client with SSRF protection and resilience.

Wraps ``httpx.AsyncClient`` with TaipanStack's ``guard_ssrf``,
retry, and circuit breaker integrations.  All outbound URLs are
validated against SSRF before the request is sent.
"""

from __future__ import annotations

import asyncio
import logging
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


def _check_request_preconditions(
    url: str,
    ssrf_protection: bool,
    circuit_breaker: CircuitBreaker | None,
) -> Result[Any, Exception] | None:
    """Check preconditions for an HTTP request.

    Args:
        url: The target URL.
        ssrf_protection: Whether SSRF protection is enabled.
        circuit_breaker: Optional circuit breaker.

    Returns:
        An ``Err`` if a precondition fails, ``None`` otherwise.

    """
    if ssrf_protection:
        ssrf_result = guard_ssrf(url)
        if isinstance(ssrf_result, Err):
            return ssrf_result

    if circuit_breaker is not None:
        cb_err = _check_circuit_breaker(circuit_breaker)
        if cb_err is not None:
            return Err(cb_err)

    return None


def _should_retry_status(
    response: Any,
    retry_config: RetryConfig | None,
    retryable_status_codes: frozenset[int],
    attempt: int,
) -> bool:
    """Check if a request should be retried based on status code.

    Args:
        response: The HTTP response.
        retry_config: Optional retry configuration.
        retryable_status_codes: Status codes that trigger retries.
        attempt: The current attempt number.

    Returns:
        True if the request should be retried, False otherwise.

    """
    if retry_config is None:
        return False

    return (
        response.status_code in retryable_status_codes
        and attempt < retry_config.max_attempts
    )


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

    # Preconditions check (SSRF and Circuit Breaker)
    precondition_err = _check_request_preconditions(
        url, ssrf_protection, circuit_breaker
    )
    if precondition_err is not None:
        return precondition_err

    max_attempts = 1
    if retry_config is not None:
        max_attempts = retry_config.max_attempts

    last_error: Exception | None = None

    for attempt in range(1, max_attempts + 1):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(method, url, **kwargs)

            # Check if we should retry on status code
            if _should_retry_status(
                response, retry_config, retryable_status_codes, attempt
            ):
                delay = calculate_delay(attempt, retry_config)  # type: ignore[arg-type]
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
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
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

        # Preconditions check (SSRF and Circuit Breaker)
        precondition_err = _check_request_preconditions(
            url, self._ssrf_protection, self._circuit_breaker
        )
        if precondition_err is not None:
            return precondition_err

        max_attempts = 1
        if self._retry_config is not None:
            max_attempts = self._retry_config.max_attempts

        last_error: Exception | None = None

        for attempt in range(1, max_attempts + 1):
            try:
                response = await self._client.request(method, url, **kwargs)

                if _should_retry_status(
                    response, self._retry_config, self._retryable_status_codes, attempt
                ):
                    delay = calculate_delay(attempt, self._retry_config)  # type: ignore[arg-type]
                    await asyncio.sleep(delay)
                    continue

                return Ok(response)

            except Exception as exc:
                last_error = exc
                if self._circuit_breaker is not None:
                    self._circuit_breaker._record_failure(exc)
                if self._retry_config is not None and attempt < max_attempts:
                    delay = calculate_delay(attempt, self._retry_config)
                    await asyncio.sleep(delay)
                    continue
                break

        return Err(last_error or RuntimeError("Request failed"))

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
