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

# Build regex for traversal patterns.
# Note: we handle ~ specially to only match at start of path or after a separator
# to avoid false positives with Windows short paths (e.g., RUNNER~1).
TRAVERSAL_REGEX = re.compile(
    r"(?:\.\.|%2e%2e|%252e%252e)|(?:^|[\\/])~",
    re.IGNORECASE,
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

# Pre-compiled regex and lookup map for fast-path command injection detection
_DANGEROUS_COMMAND_RE = re.compile(
    "|".join(re.escape(p) for p, _ in _DANGEROUS_COMMAND_PATTERNS)
)
_DANGEROUS_COMMAND_LOOKUP = dict(_DANGEROUS_COMMAND_PATTERNS)

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

_SENSITIVE_ENV_VAR_PATTERN = re.compile(r"SECRET|PASSWORD|TOKEN|PRIVATE.*KEY|API.*KEY")

_SAFE_HASH_ALGORITHMS = frozenset(
    [
        "sha256",
        "sha384",
        "sha512",
        "sha3_256",
        "sha3_384",
        "sha3_512",
        "blake2b",
        "blake2s",
    ]
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


def _check_traversal_patterns(path_str: str) -> None:
    path_str_lower = path_str.lower()
    match = TRAVERSAL_REGEX.search(path_str_lower)
    if match:
        pattern = match.group(0)
        raise SecurityError(
            f"Path traversal pattern detected: {pattern}",
            guard_name="path_traversal",
            value=path_str[:50],  # Truncate for safety
        )


def _resolve_and_check_bounds(path: Path, base_dir: Path) -> tuple[Path, Path]:
    try:
        full_path = path if path.is_absolute() else (base_dir / path)
        resolved = full_path.resolve()
    except (OSError, ValueError) as e:
        raise SecurityError(
            f"Invalid path: {e}",
            guard_name="path_traversal",
        ) from e

    if not resolved.is_relative_to(base_dir):
        raise SecurityError(
            "Path escapes base directory",
            guard_name="path_traversal",
        )
    return full_path, resolved


def _check_symlink_safety(full_path: Path, base_dir: Path) -> None:
    current = full_path
    # Only check components from the user-provided path, not the base_dir
    while current not in (base_dir, current.parent):
        # We don't check .exists() because it returns False for broken symlinks
        if current.is_symlink():
            raise SecurityError(
                "Symlinks are not allowed",
                guard_name="path_traversal",
                value=str(current),
            )
        current = current.parent


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

    _check_traversal_patterns(str(path))
    full_path, resolved = _resolve_and_check_bounds(path, base_dir)

    if not allow_symlinks:
        _check_symlink_safety(full_path, base_dir)

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

        match = _DANGEROUS_COMMAND_RE.search(arg)
        if match:
            # We use the matched substring to look up the description.
            # Because the regex is an alternation of the patterns in order,
            # this preserves the existing behavior where earlier patterns
            # in the list take precedence (e.g. '>' matches before '>>').
            description = _DANGEROUS_COMMAND_LOOKUP[match.group(0)]
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


def _check_env_denied(
    name_upper: str, name: str, denied_names: Sequence[str] | None
) -> None:
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


def _check_env_sensitive(
    name_upper: str, name: str, allowed_names: Sequence[str] | None
) -> None:
    if not _SENSITIVE_ENV_VAR_PATTERN.search(name_upper):
        return

    # Only block if not explicitly allowed
    if allowed_names is not None:
        allowed = {n.upper() for n in allowed_names}
        if name_upper in allowed:
            return

    raise SecurityError(
        f"Access to potentially sensitive variable '{name}' is denied",
        guard_name="env_variable",
        value=name,
    )


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

    _check_env_denied(name_upper, name, denied_names)
    _check_env_sensitive(name_upper, name, allowed_names)

    # Get the variable
    value = os.environ.get(name)
    if value is None:
        raise SecurityError(
            f"Environment variable '{name}' is not set",
            guard_name="env_variable",
            value=name,
        )

    return value


def guard_hash_algorithm(
    algorithm: str,
    *,
    allowed_algorithms: Sequence[str] | None = None,
) -> str:
    """Validate hash algorithm against a whitelist of secure ones.

    Args:
        algorithm: The name of the hash algorithm to validate.
        allowed_algorithms: Optional whitelist of allowed algorithms.
            Defaults to a secure set (SHA-256, SHA-512, etc.).

    Returns:
        The normalized (lowercase) algorithm name.

    Raises:
        SecurityError: If the algorithm is potentially weak or not allowed.

    """
    if not isinstance(algorithm, str):
        raise TypeError(f"Algorithm name must be str, got {type(algorithm).__name__}")

    algo_lower = algorithm.lower().replace("-", "")

    allowed: frozenset[str]
    if allowed_algorithms is not None:
        allowed = frozenset(a.lower().replace("-", "") for a in allowed_algorithms)
    else:
        allowed = _SAFE_HASH_ALGORITHMS

    if algo_lower not in allowed:
        raise SecurityError(
            f"Hash algorithm '{algorithm}' is considered weak or is not allowed",
            guard_name="hash_algorithm",
            value=algorithm,
        )

    return algo_lower


# ── SSRF Private-Range Constants ─────────────────────────────────────────────
_ALLOWED_SSRF_SCHEMES: frozenset[str] = frozenset({"http", "https"})


def _validate_ssrf_url(
    url: str,
    allowed_schemes: frozenset[str],
) -> Result[str, SecurityError]:
    """Validate the URL format, scheme, and presence of hostname."""
    if not isinstance(url, str):
        raise TypeError(f"URL must be str, got {type(url).__name__}")

    if not url:
        return Err(SecurityError("URL cannot be empty", guard_name="ssrf"))

    try:
        parsed = urlparse(url)
    except ValueError as exc:  # pragma: no cover
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

    return Ok(hostname)


def _check_ip_addresses(hostname: str) -> Result[None, SecurityError]:
    """Resolve hostname to IP addresses and check for SSRF risk."""
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
        try:
            addr = ipaddress.ip_address(raw_ip)
        except ValueError:
            continue

        if (
            addr.is_private
            or addr.is_loopback
            or addr.is_link_local
            or addr.is_reserved
        ):
            return Err(
                SecurityError(
                    "SSRF detected: hostname resolves to private/reserved address",
                    guard_name="ssrf",
                )
            )

    return Ok(None)


def guard_ssrf(
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
    # 1. Validate format and scheme
    match _validate_ssrf_url(url, allowed_schemes):
        case Err(e):
            return Err(e)
        case Ok(hostname):
            # 2. Check IP safety
            match _check_ip_addresses(hostname):
                case Err(e):
                    return Err(e)
                case Ok():
                    return Ok(url)
