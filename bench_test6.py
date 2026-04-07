import socket
from urllib.parse import urlsplit
from result import Ok, Err, Result
from taipanstack.security.guards import guard_ssrf, _is_ip_safe, SecurityError, _ALLOWED_SSRF_SCHEMES
import time
from unittest.mock import patch

def guard_ssrf_inlined(
    url: str,
    *,
    allowed_schemes: frozenset[str] = _ALLOWED_SSRF_SCHEMES,
) -> Result[str, SecurityError]:
    if type(url) is not str:
        raise TypeError(f"URL must be str, got {type(url).__name__}")

    if not url:
        return Err(SecurityError("URL cannot be empty", guard_name="ssrf"))

    try:
        parsed = urlsplit(url)
    except ValueError as exc:
        return Err(
            SecurityError(
                f"Malformed URL: {exc}",
                guard_name="ssrf",
                value=url[:80],
            )
        )

    if not parsed.scheme or parsed.scheme.lower() not in allowed_schemes:
        return Err(
            SecurityError(
                f"URL scheme '{parsed.scheme}' is not allowed",
                guard_name="ssrf",
                value=url[:80],
            )
        )

    hostname = parsed.hostname
    if not hostname:
        return Err(
            SecurityError(
                "URL has no resolvable hostname",
                guard_name="ssrf",
                value=url[:80],
            )
        )

    try:
        addr_infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return Err(
            SecurityError(
                "Hostname could not be resolved",
                guard_name="ssrf",
            )
        )

    for addr_info in addr_infos:
        raw_ip = addr_info[4][0]
        if not _is_ip_safe(raw_ip):
            return Err(
                SecurityError(
                    "SSRF detected: hostname resolves to private/reserved address",
                    guard_name="ssrf",
                )
            )

    return Ok(url)

public_ip = [(socket.AF_INET, socket.SOCK_STREAM, 0, "", ("93.184.216.34", 80))]

with patch("taipanstack.security.guards.socket.getaddrinfo", return_value=public_ip):
    start = time.time()
    for _ in range(100000):
        guard_ssrf("https://example.com")
    print("guard_ssrf:", time.time() - start)

    start = time.time()
    for _ in range(100000):
        guard_ssrf_inlined("https://example.com")
    print("guard_ssrf_inlined:", time.time() - start)
