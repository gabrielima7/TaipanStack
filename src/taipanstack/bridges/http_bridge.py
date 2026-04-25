"""
HTTP Bridge — safe httpx client with SSRF protection and resilience.

Wraps ``httpx.AsyncClient`` with TaipanStack's ``guard_ssrf``,
retry, and circuit breaker integrations.  All outbound URLs are
validated against SSRF before the request is sent.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable, Mapping, Sequence
from typing import TYPE_CHECKING, cast

from typing_extensions import TypedDict, Unpack

from taipanstack.core.result import Err, Ok, Result
from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
)
from taipanstack.resilience.retry import RetryConfig, calculate_delay
from taipanstack.security.guards import guard_ssrf

logger = logging.getLogger("taipanstack.bridges.http")


class HttpRequestKwargs(TypedDict, total=False):
    """Type definitions for HTTP request kwargs."""

    content: bytes | str | None
    data: (
        dict[str, str | int | float | bool | None]
        | list[tuple[str, str]]
        | bytes
        | str
        | None
    )
    files: dict[str, bytes | tuple[str, bytes]]
    json: dict[str, object] | list[object] | str | int | float | bool | None
    params: (
        dict[
            str,
            str | int | float | bool | None | Sequence[str | int | float | bool | None],
        ]
        | list[tuple[str, str | int | float | bool | None]]
        | str
        | bytes
        | None
    )
    headers: dict[str, str]
    cookies: dict[str, str]
    auth: tuple[str, str]
    follow_redirects: bool
    extensions: dict[str, object]


class HttpClientKwargs(TypedDict, total=False):
    """Type definitions for HTTP client kwargs."""

    base_url: str
    headers: dict[str, str]
    cookies: dict[str, str]
    verify: bool | str
    cert: str | tuple[str, str] | tuple[str, str, str]
    http1: bool
    http2: bool
    proxy: str
    mounts: Mapping[str, httpx.AsyncBaseTransport | None]
    follow_redirects: bool
    max_redirects: int
    event_hooks: dict[str, list[Callable[..., object]]]
    trust_env: bool
    default_encoding: str | Callable[[bytes], str]


# --- optional httpx import ------------------------------------------------

try:
    import httpx

    _HAS_HTTPX = True  # pragma: no cover
except ImportError:  # pragma: no cover
    _HAS_HTTPX = False

if TYPE_CHECKING:
    import httpx

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


def _should_retry_status(
    response: httpx.Response,
    retry_config: RetryConfig | None,
    retryable_status_codes: frozenset[int],
    attempt: int,
    max_attempts: int,
) -> bool:
    """Determine if a request should be retried based on status code."""
    return (
        retry_config is not None
        and response.status_code in retryable_status_codes
        and attempt < max_attempts
    )


async def _handle_http_exception(
    exc: Exception,
    attempt: int,
    max_attempts: int,
    retry_config: RetryConfig | None,
    circuit_breaker: CircuitBreaker | None,
) -> bool:
    """Handle exception and return True if we should retry, False otherwise."""
    if circuit_breaker is not None:  # pragma: no branch
        circuit_breaker._record_failure(exc)
    if retry_config is not None and attempt < max_attempts:
        delay = calculate_delay(attempt, retry_config)
        await asyncio.sleep(min(delay, 3600.0))
        return True
    return False


async def _execute_with_retries(
    request_func: Callable[[], Awaitable[httpx.Response]],
    retry_config: RetryConfig | None,
    circuit_breaker: CircuitBreaker | None,
    retryable_status_codes: frozenset[int],
) -> Result[httpx.Response, Exception]:
    """Execute a request function with optional retries and circuit breaker.

    Args:
        request_func: Async callable that performs the request.
        retry_config: Optional retry configuration.
        circuit_breaker: Optional circuit breaker.
        retryable_status_codes: Status codes to retry on.

    Returns:
        ``Ok(Response)`` on success, ``Err`` on failure.

    """
    max_attempts = retry_config.max_attempts if retry_config is not None else 1
    last_error: Exception | None = None

    for attempt in range(1, max_attempts + 1):
        try:
            response = await request_func()
            if _should_retry_status(
                response,
                retry_config,
                retryable_status_codes,
                attempt,
                max_attempts,
            ):
                # Config is not None if we reach here
                delay = calculate_delay(attempt, cast(RetryConfig, retry_config))
                await asyncio.sleep(min(delay, 3600.0))
                continue
            return Ok(response)
        except Exception as exc:
            last_error = exc
            should_retry = await _handle_http_exception(
                exc, attempt, max_attempts, retry_config, circuit_breaker
            )
            if should_retry:
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
    timeout: float | None = 10.0,
    **kwargs: Unpack[HttpRequestKwargs],
) -> Result[httpx.Response, Exception]:
    """Perform a one-shot HTTP request with safety features.

    Args:
        method: HTTP method (GET, POST, etc.).
        url: Target URL.
        ssrf_protection: Validate URL against SSRF.
        retry_config: Optional retry configuration.
        circuit_breaker: Optional circuit breaker.
        retryable_status_codes: Status codes that trigger retries.
        timeout: Explicit timeout in seconds (default: 10.0).
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

    async def _do_request() -> httpx.Response:
        async with httpx.AsyncClient(timeout=timeout) as client:  # nosemgrep
            request_func = cast(
                Callable[..., Awaitable[httpx.Response]], client.request
            )
            response = await request_func(method, url, **kwargs)
            return response

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
        timeout: float = 10.0,
        **client_kwargs: Unpack[HttpClientKwargs],
    ) -> None:
        """Initialize the safe HTTP client.

        Args:
            ssrf_protection: Enable SSRF validation.
            retry_config: Retry configuration.
            circuit_breaker: Circuit breaker instance.
            retryable_status_codes: Status codes to retry.
            **client_kwargs: Keyword args for httpx.AsyncClient.
                Default timeout is 10.0 seconds if not provided.

        """
        self._ssrf_protection = ssrf_protection
        self._retry_config = retry_config
        self._circuit_breaker = circuit_breaker
        self._retryable_status_codes = retryable_status_codes
        self._client_kwargs = client_kwargs
        self._timeout = timeout
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> SafeHttpClient:
        """Enter the async context manager."""
        if not _HAS_HTTPX:
            msg = (
                "httpx is required for SafeHttpClient. "
                "Install with: pip install taipanstack[bridges-http]"
            )
            raise ImportError(msg)
        self._client = httpx.AsyncClient(
            timeout=self._timeout,
            **self._client_kwargs,
        )  # nosemgrep
        return self

    async def __aexit__(
        self,
        _exc_type: type[BaseException] | None,
        _exc_val: BaseException | None,
        _exc_tb: object,
    ) -> None:
        """Exit the async context manager."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def request(
        self,
        method: str,
        url: str,
        **kwargs: Unpack[HttpRequestKwargs],
    ) -> Result[httpx.Response, Exception]:
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

        async def _do_request() -> httpx.Response:
            # We explicitly verified client is not None above
            client: httpx.AsyncClient = cast(httpx.AsyncClient, self._client)
            request_func = cast(
                Callable[..., Awaitable[httpx.Response]], client.request
            )
            response = await request_func(method, url, **kwargs)
            return response

        return await _execute_with_retries(
            _do_request,
            self._retry_config,
            self._circuit_breaker,
            self._retryable_status_codes,
        )

    async def get(
        self, url: str, **kw: Unpack[HttpRequestKwargs]
    ) -> Result[httpx.Response, Exception]:
        """Send a GET request."""
        return await self.request("GET", url, **kw)

    async def post(
        self, url: str, **kw: Unpack[HttpRequestKwargs]
    ) -> Result[httpx.Response, Exception]:
        """Send a POST request."""
        return await self.request("POST", url, **kw)

    async def put(
        self, url: str, **kw: Unpack[HttpRequestKwargs]
    ) -> Result[httpx.Response, Exception]:
        """Send a PUT request."""
        return await self.request("PUT", url, **kw)

    async def delete(
        self, url: str, **kw: Unpack[HttpRequestKwargs]
    ) -> Result[httpx.Response, Exception]:
        """Send a DELETE request."""
        return await self.request("DELETE", url, **kw)

    async def patch(
        self, url: str, **kw: Unpack[HttpRequestKwargs]
    ) -> Result[httpx.Response, Exception]:
        """Send a PATCH request."""
        return await self.request("PATCH", url, **kw)
