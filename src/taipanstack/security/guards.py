"""
Runtime guards for protection against errors and AI hallucinations.

These guards provide runtime protection against common security issues
and programming errors that can occur from incorrect AI-generated code.
All guards raise SecurityError on violation.
"""

import ipaddress
import os
import re
import socket
from collections.abc import Sequence
from pathlib import Path
from urllib.parse import urlparse

from result import Err, Ok, Result

_TRAVERSAL_PATTERNS: frozenset[str] = frozenset(
    p.lower()
    for p in [
        "..",
        "~",
        r"\.\.",
        "%2e%2e",  # URL encoded ..
        "%252e%252e",  # Double URL encoded
    ]
)

_DANGEROUS_COMMAND_PATTERNS: tuple[tuple[str, str], ...] = (
    (";", "command separator"),
    ("|", "pipe"),
    ("&", "background/and operator"),
    ("$", "variable expansion"),
    ("`", "command substitution"),
    ("$(", "command substitution"),
    ("${", "variable expansion"),
    (">", "redirect"),
    ("<", "redirect"),
    (">>", "redirect append"),
    ("||", "or operator"),
    ("&&", "and operator"),
    ("\n", "newline"),
    ("\r", "carriage return"),
    ("\x00", "null byte"),
)

_DEFAULT_DENIED_EXTENSIONS = frozenset(
    [
        "exe",
        "dll",
        "so",
        "dylib",  # Executables
        "sh",
        "bash",
        "zsh",
        "ps1",
        "bat",
        "cmd",  # Scripts
        "php",
        "jsp",
        "asp",
        "aspx",  # Server-side scripts
    ]
)

_DEFAULT_DENIED_ENV_VARS = frozenset(
    [
        "AWS_SECRET_ACCESS_KEY",
        "AWS_SESSION_TOKEN",
        "GITHUB_TOKEN",
        "GH_TOKEN",
        "GITLAB_TOKEN",
        "DATABASE_URL",
        "DB_PASSWORD",
        "PASSWORD",
        "SECRET_KEY",
        "PRIVATE_KEY",
        "API_KEY",
        "API_SECRET",
    ]
)

_SENSITIVE_ENV_VAR_PATTERNS = (
    re.compile(r".*SECRET.*"),
    re.compile(r".*PASSWORD.*"),
    re.compile(r".*TOKEN.*"),
    re.compile(r".*PRIVATE.*KEY.*"),
    re.compile(r".*API.*KEY.*"),
)


class SecurityError(Exception):
    """Raised when a security guard detects a violation.

    Attributes:
        guard_name: Name of the guard that was triggered.
        message: Description of the violation.
        value: The offending value (if safe to log).

    """

    def __init__(
        self,
        message: str,
        guard_name: str = "unknown",
        value: str | None = None,
    ) -> None:
        """Initialize SecurityError.

        Args:
            message: Description of the violation.
            guard_name: Name of the guard that triggered.
            value: The offending value (sanitized).

        """
        self.guard_name = guard_name
        self.value = value
        super().__init__(f"[{guard_name}] {message}")


def guard_path_traversal(
    path: Path | str,
    base_dir: Path | str | None = None,
    *,
    allow_symlinks: bool = False,
) -> Path:
    """Prevent path traversal attacks.

    Ensures that the given path does not escape the base directory
    using techniques like '..' or symlinks.

    Args:
        path: The path to validate.
        base_dir: The base directory to constrain to. Defaults to cwd.
        allow_symlinks: Whether to allow symlinks (default: False).

    Returns:
        The resolved, validated path.

    Raises:
        SecurityError: If path traversal is detected.

    Example:
        >>> guard_path_traversal("../etc/passwd", Path("/app"))
        SecurityError: [path_traversal] Path escapes base directory

    """
    if not isinstance(path, (str, Path)):
        raise TypeError(f"path must be str or Path, got {type(path).__name__}")
    path = Path(path) if isinstance(path, str) else path
    base_dir = Path(base_dir).resolve() if base_dir else Path.cwd().resolve()

    # Check for explicit traversal patterns before resolution
    path_str = str(path)
    path_str_lower = path_str.lower()

    for pattern in _TRAVERSAL_PATTERNS:
        if pattern in path_str_lower:
            raise SecurityError(
                f"Path traversal pattern detected: {pattern}",
                guard_name="path_traversal",
                value=path_str[:50],  # Truncate for safety
            )

    # Resolve the path
    try:
        resolved = path.resolve() if path.is_absolute() else (base_dir / path).resolve()
    except (OSError, ValueError) as e:
        raise SecurityError(
            f"Invalid path: {e}",
            guard_name="path_traversal",
        ) from e

    # Check if resolved path is within base_dir
    try:
        resolved.relative_to(base_dir)
    except ValueError as e:
        raise SecurityError(
            f"Path escapes base directory: {resolved} is not under {base_dir}",
            guard_name="path_traversal",
            value=str(resolved)[:100],
        ) from e

    # Check for symlinks if not allowed
    is_existing_symlink = (
        not allow_symlinks and resolved.exists() and resolved.is_symlink()
    )
    if is_existing_symlink:
        raise SecurityError(
            "Symlinks are not allowed",
            guard_name="path_traversal",
            value=str(resolved),
        )

    return resolved


def guard_command_injection(
    command: Sequence[str],
    *,
    allowed_commands: Sequence[str] | None = None,
) -> list[str]:
    """Prevent command injection attacks.

    Validates that command arguments don't contain shell metacharacters
    that could lead to command injection.

    Args:
        command: The command and arguments as a sequence.
        allowed_commands: Optional whitelist of allowed base commands.

    Returns:
        The validated command as a list.

    Raises:
        SecurityError: If command injection is detected.

    Example:
        >>> guard_command_injection(["echo", "hello; rm -rf /"])
        SecurityError: [command_injection] Dangerous characters detected

    """
    if not command:
        raise SecurityError(
            "Empty command is not allowed",
            guard_name="command_injection",
        )

    cmd_list = list(command)

    # Validate all items are strings and check for dangerous patterns
    for i, arg in enumerate(cmd_list):
        if not isinstance(arg, str):
            raise TypeError(
                f"All command arguments must be strings, "
                f"got {type(arg).__name__} at index {i}"
            )

        for pattern, description in _DANGEROUS_COMMAND_PATTERNS:
            if pattern in arg:
                raise SecurityError(
                    f"Dangerous shell character detected: {description}",
                    guard_name="command_injection",
                    value=arg[:50],
                )

    # Check against allowed commands whitelist
    if allowed_commands is not None:
        base_command = cmd_list[0]
        # Get just the command name without path
        command_name = Path(base_command).name
        cmd_not_allowed = (
            command_name not in allowed_commands
            and base_command not in allowed_commands
        )
        if cmd_not_allowed:
            raise SecurityError(
                f"Command not in allowed list: {command_name}",
                guard_name="command_injection",
                value=command_name,
            )

    return cmd_list


def guard_file_extension(
    filename: str | Path,
    *,
    allowed_extensions: Sequence[str] | None = None,
    denied_extensions: Sequence[str] | None = None,
) -> Path:
    """Validate file extension against allow/deny lists.

    Args:
        filename: The filename to check.
        allowed_extensions: Extensions to allow (with or without dot).
        denied_extensions: Extensions to deny (with or without dot).

    Returns:
        The filename as a Path.

    Raises:
        SecurityError: If extension is not allowed or is denied.

    """
    path = Path(filename)
    ext = path.suffix.lower().lstrip(".")

    # Normalize extension lists
    def normalize_ext(e: str) -> str:
        return e.lower().lstrip(".")

    if denied_extensions is not None:
        denied = frozenset(normalize_ext(e) for e in denied_extensions)
    else:
        denied = _DEFAULT_DENIED_EXTENSIONS

    if ext in denied:
        raise SecurityError(
            f"File extension '{ext}' is not allowed",
            guard_name="file_extension",
            value=str(path.name),
        )

    if allowed_extensions is not None:  # pragma: no branch
        allowed = {normalize_ext(e) for e in allowed_extensions}
        if ext not in allowed:
            raise SecurityError(
                f"File extension '{ext}' is not in allowed list",
                guard_name="file_extension",
                value=str(path.name),
            )

    return path


def guard_env_variable(
    name: str,
    *,
    allowed_names: Sequence[str] | None = None,
    denied_names: Sequence[str] | None = None,
) -> str:
    """Guard against accessing sensitive environment variables.

    Args:
        name: The environment variable name.
        allowed_names: Variable names to allow.
        denied_names: Variable names to deny.

    Returns:
        The environment variable value if safe.

    Raises:
        SecurityError: If variable access is not allowed.

    """
    # Validate input type
    if not isinstance(name, str):
        raise TypeError(f"Variable name must be str, got {type(name).__name__}")

    # Reject empty/whitespace-only variable names
    if not name or not name.strip():
        raise SecurityError(
            "Environment variable name cannot be empty or whitespace",
            guard_name="env_variable",
        )

    name_upper = name.upper()

    if denied_names is not None:
        denied = frozenset(n.upper() for n in denied_names)
    else:
        denied = _DEFAULT_DENIED_ENV_VARS

    if name_upper in denied:
        raise SecurityError(
            f"Access to sensitive variable '{name}' is denied",
            guard_name="env_variable",
            value=name,
        )

    for pattern in _SENSITIVE_ENV_VAR_PATTERNS:
        if pattern.match(name_upper):
            # Only block if not explicitly allowed
            if allowed_names is not None:
                allowed = {n.upper() for n in allowed_names}
                if name_upper not in allowed:
                    raise SecurityError(
                        f"Access to potentially sensitive variable '{name}' is denied",
                        guard_name="env_variable",
                        value=name,
                    )
            else:
                raise SecurityError(
                    f"Access to potentially sensitive variable '{name}' is denied",
                    guard_name="env_variable",
                    value=name,
                )

    # Get the variable
    value = os.environ.get(name)
    if value is None:
        raise SecurityError(
            f"Environment variable '{name}' is not set",
            guard_name="env_variable",
            value=name,
        )

    return value


# ── SSRF Private-Range Constants ─────────────────────────────────────────────
_PRIVATE_NETWORKS: tuple[ipaddress.IPv4Network | ipaddress.IPv6Network, ...] = (
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.0.0/16"),  # Link-local / AWS metadata
    ipaddress.ip_network("127.0.0.0/8"),  # Loopback
    ipaddress.ip_network("::1/128"),  # IPv6 loopback
    ipaddress.ip_network("fc00::/7"),  # IPv6 unique local
    ipaddress.ip_network("fe80::/10"),  # IPv6 link-local
)

_ALLOWED_SSRF_SCHEMES: frozenset[str] = frozenset({"http", "https"})


def guard_ssrf(  # noqa: PLR0911
    url: str,
    *,
    allowed_schemes: frozenset[str] = _ALLOWED_SSRF_SCHEMES,
) -> Result[str, SecurityError]:
    """Validate a URL against Server-Side Request Forgery (SSRF) attacks.

    Parse the URL, resolve its hostname via DNS, and reject it when the
    resulting IP address falls inside a private, loopback, link-local, or
    otherwise reserved network range.

    Args:
        url: The URL string to validate.
        allowed_schemes: Set of URL schemes considered safe.
            Defaults to ``{"http", "https"}``.

    Returns:
        ``Ok(url)`` when the URL is safe to fetch.
        ``Err(SecurityError)`` when an SSRF risk is detected.

    Raises:
        TypeError: If *url* is not a :class:`str`.

    Example:
        >>> guard_ssrf("https://example.com")
        Ok('https://example.com')
        >>> guard_ssrf("http://169.254.169.254/metadata")
        Err(SecurityError('[ssrf] ...))

    """
    if not isinstance(url, str):
        raise TypeError(f"URL must be str, got {type(url).__name__}")

    if not url:
        return Err(
            SecurityError(
                "URL cannot be empty",
                guard_name="ssrf",
            )
        )

    try:
        parsed = urlparse(url)
    except ValueError as exc:  # pragma: no cover — urlparse rarely raises
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

    # Resolve hostname → list of IP addresses via DNS
    try:
        addr_infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        return Err(
            SecurityError(
                f"Hostname could not be resolved: {exc}",
                guard_name="ssrf",
                value=hostname[:80],
            )
        )

    for addr_info in addr_infos:
        raw_ip = addr_info[4][0]
        try:
            addr = ipaddress.ip_address(raw_ip)
        except ValueError:
            continue

        for network in _PRIVATE_NETWORKS:
            if addr in network:
                return Err(
                    SecurityError(
                        f"SSRF detected: hostname '{hostname}' resolves to "
                        f"private/reserved address {addr}",
                        guard_name="ssrf",
                        value=str(addr),
                    )
                )

        # Catch-all for remaining special addresses not in the explicit list
        if (
            addr.is_private
            or addr.is_loopback
            or addr.is_link_local
            or addr.is_reserved
        ):
            return Err(
                SecurityError(
                    f"SSRF detected: '{hostname}' resolves to a reserved "
                    f"address {addr}",
                    guard_name="ssrf",
                    value=str(addr),
                )
            )

    return Ok(url)
