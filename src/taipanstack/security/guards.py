"""
Runtime guards for protection against errors and AI hallucinations.

These guards provide runtime protection against common security issues
and programming errors that can occur from incorrect AI-generated code.
All guards raise SecurityError on violation.
"""

import functools
import ipaddress
import os
import re
import socket
import unicodedata
from collections.abc import Sequence
from pathlib import Path
from urllib.parse import unquote, urlsplit

from result import Err, Ok, Result

from taipanstack.security.sanitizers import MAX_PATH_LENGTH
from taipanstack.security.validators import MAX_ENV_VAR_LENGTH, MAX_URL_LENGTH

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
    "|".join(re.escape(p) for p, _ in _DANGEROUS_COMMAND_PATTERNS),
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
    ],
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
    ],
)

_SENSITIVE_ENV_VAR_PATTERN = re.compile(
    r"SECRET|PASSWORD|TOKEN|PRIVATE.*?KEY|API.*?KEY",
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
    """Check for explicit traversal patterns before resolution."""
    match = TRAVERSAL_REGEX.search(path_str.lower())
    if match:
        raise SecurityError(
            f"Path traversal pattern detected: {match.group(0)}",
            guard_name="path_traversal",
            value=path_str[:50],  # Truncate for safety
        )


def _resolve_and_check_bounds(path: Path, base_dir: Path) -> tuple[Path, Path]:
    """Resolve the path and check if it is within base_dir."""
    try:
        full_path = path if path.is_absolute() else (base_dir / path)
        resolved = full_path.resolve()
    except (OSError, ValueError, RuntimeError) as e:
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
    """Check for symlinks recursively up to the base directory."""
    current = full_path
    # Only check components from the user-provided path, not the base_dir
    while current not in (base_dir, current.parent):
        # We don't check .exists() because it returns False for broken symlinks
        try:
            is_symlink = current.is_symlink()
        except OSError as e:
            raise SecurityError(
                f"Invalid path encountered during symlink check: {e}",
                guard_name="path_traversal",
                value=str(current)[:50],
            ) from e
        if is_symlink:
            raise SecurityError(
                "Symlinks are not allowed",
                guard_name="path_traversal",
                value=str(current),
            )
        current = current.parent


def _check_path_types(path: object, base_dir: object) -> None:
    """Validate types of path and base_dir."""
    if not isinstance(path, (str, Path)):
        raise TypeError(f"path must be str or Path, got {type(path).__name__}")
    if base_dir is not None and not isinstance(base_dir, (str, Path)):
        raise TypeError(f"base_dir must be str or Path, got {type(base_dir).__name__}")


def _check_path_lengths(path: object, base_dir: object) -> None:
    """Validate lengths of path and base_dir."""
    if len(str(path)) > MAX_PATH_LENGTH:
        raise SecurityError(
            f"Path length exceeds maximum allowed limit of {MAX_PATH_LENGTH}",
            guard_name="path_traversal",
        )

    if base_dir is not None and len(str(base_dir)) > MAX_PATH_LENGTH:
        raise SecurityError(
            f"Base directory length exceeds maximum allowed limit of {MAX_PATH_LENGTH}",
            guard_name="path_traversal",
        )


def _validate_path_types(path: object, base_dir: object) -> None:
    """Validate types and lengths of path and base_dir."""
    _check_path_types(path, base_dir)
    _check_path_lengths(path, base_dir)


def _check_path_null_bytes(path: Path | str, base_dir: Path | str | None) -> None:
    """Check for null bytes in path and base_dir."""
    if "\x00" in str(path) or (base_dir is not None and "\x00" in str(base_dir)):
        raise SecurityError(
            "Path contains null bytes",
            guard_name="path_traversal",
        )


def _resolve_base_dir(base_dir: Path | str | None) -> Path:
    """Resolve the base directory."""
    return Path(base_dir).resolve() if base_dir else Path.cwd().resolve()


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
    _validate_path_types(path, base_dir)
    _check_path_null_bytes(path, base_dir)

    path_obj = Path(path) if isinstance(path, str) else path
    base = _resolve_base_dir(base_dir)

    _check_traversal_patterns(str(path_obj))
    full_path, resolved = _resolve_and_check_bounds(path_obj, base)

    if not allow_symlinks:
        _check_symlink_safety(full_path, base)

    return resolved


def _check_command_not_empty(command: Sequence[str]) -> None:
    if not command:
        raise SecurityError(
            "Empty command is not allowed",
            guard_name="command_injection",
        )


def _check_command_null_bytes(cmd_list: list[str]) -> None:
    for arg in cmd_list:
        if isinstance(arg, str) and "\x00" in arg:
            raise SecurityError(
                "Dangerous shell character detected: null byte",
                guard_name="command_injection",
                value=arg[:50],
            )


def _check_command_patterns(cmd_list: list[str]) -> None:
    for i, arg in enumerate(cmd_list):
        if not isinstance(arg, str):
            raise TypeError(
                f"All command arguments must be strings, "
                f"got {type(arg).__name__} at index {i}",
            )

        match = _DANGEROUS_COMMAND_RE.search(arg)
        if match:
            description = _DANGEROUS_COMMAND_LOOKUP[match.group(0)]
            raise SecurityError(
                f"Dangerous shell character detected: {description}",
                guard_name="command_injection",
                value=arg[:50],
            )


def _check_allowed_commands(
    cmd_list: list[str],
    allowed_commands: Sequence[str] | None,
) -> None:
    if allowed_commands is None:
        return

    base_command = cmd_list[0]
    command_name = Path(base_command).name
    cmd_not_allowed = (
        command_name not in allowed_commands and base_command not in allowed_commands
    )
    if cmd_not_allowed:
        raise SecurityError(
            f"Command not in allowed list: {command_name}",
            guard_name="command_injection",
            value=command_name,
        )


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
    cmd_list = list(command)

    _check_command_not_empty(cmd_list)

    _check_command_null_bytes(cmd_list)
    _check_command_patterns(cmd_list)
    _check_allowed_commands(cmd_list, allowed_commands)

    return cmd_list


def _check_filename_null_bytes(filename_str: str) -> None:
    if "\x00" in filename_str:
        raise SecurityError(
            "Filename contains null bytes",
            guard_name="file_extension",
            value=filename_str,
        )


def _clean_filename_end(clean_name: str) -> str:
    end_idx = len(clean_name)
    while end_idx > 0:
        char = clean_name[end_idx - 1]
        if (
            char == "."
            or unicodedata.category(char).startswith(("Z", "C"))
            or char == "\xad"
        ):
            end_idx -= 1
        else:
            break
    return clean_name[:end_idx]


def _normalize_ext(e: str) -> str:
    return e.lower().lstrip(".")


def _check_denied_extension(
    ext: str,
    original_name: str,
    denied_extensions: Sequence[str] | None,
) -> None:
    if denied_extensions is not None:
        denied = frozenset(_normalize_ext(e) for e in denied_extensions)
    else:
        denied = _DEFAULT_DENIED_EXTENSIONS

    if ext in denied:
        raise SecurityError(
            f"File extension '{ext}' is not allowed",
            guard_name="file_extension",
            value=original_name,
        )


def _check_allowed_extension(
    ext: str,
    original_name: str,
    allowed_extensions: Sequence[str] | None,
) -> None:
    if allowed_extensions is not None:
        allowed = {_normalize_ext(e) for e in allowed_extensions}
        if ext not in allowed:
            raise SecurityError(
                f"File extension '{ext}' is not in allowed list",
                guard_name="file_extension",
                value=original_name,
            )


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
    filename_str = str(filename)
    if len(filename_str) > MAX_URL_LENGTH:  # Reuse constant to avoid PLR2004
        raise SecurityError(
            f"Filename length exceeds maximum allowed limit of {MAX_URL_LENGTH}",
            guard_name="file_extension",
            value=filename_str[:80],
        )
    _check_filename_null_bytes(filename_str)

    path = Path(filename)
    clean_name = _clean_filename_end(path.name)

    ext = "" if not clean_name else Path(clean_name).suffix.lower().lstrip(".")

    _check_denied_extension(ext, str(path.name), denied_extensions)
    _check_allowed_extension(ext, str(path.name), allowed_extensions)

    return path


def _check_env_denied(
    name_upper: str,
    name: str,
    denied_names: Sequence[str] | None,
) -> None:
    """Check if the environment variable is in the denied list."""
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
    name_upper: str,
    name: str,
    allowed_names: Sequence[str] | None,
) -> None:
    """Check if the environment variable matches sensitive patterns."""
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


def _check_env_var_type(name: object) -> str:
    if not isinstance(name, str):
        raise TypeError(f"Variable name must be str, got {type(name).__name__}")
    return name


def _check_env_var_length(name: str) -> None:
    if len(name) > MAX_ENV_VAR_LENGTH:
        raise SecurityError(
            "Environment variable name exceeds maximum length",
            guard_name="env_variable",
            value=name[:80],
        )


def _check_env_var_content(name: str) -> None:
    if not name or not name.strip():
        raise SecurityError(
            "Environment variable name cannot be empty or whitespace",
            guard_name="env_variable",
        )

    if "\x00" in name:
        raise SecurityError(
            "Environment variable name cannot contain null bytes",
            guard_name="env_variable",
        )


def _validate_env_var_name(name: object) -> str:
    """Validate environment variable name."""
    valid_name = _check_env_var_type(name)
    _check_env_var_length(valid_name)
    _check_env_var_content(valid_name)

    return valid_name


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
    # Validate input type and format
    name = _validate_env_var_name(name)

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


# ── SSRF Private-Range Constants ─────────────────────────────────────────────
_ALLOWED_SSRF_SCHEMES: frozenset[str] = frozenset({"http", "https"})


def _check_ssrf_url_length(url: str) -> Result[str, SecurityError]:
    if not isinstance(url, str):
        return Err(  # type: ignore[unreachable]
            SecurityError(
                f"URL must be str, got {type(url).__name__}",
                guard_name="ssrf",
            ),
        )

    if not url:
        return Err(SecurityError("URL cannot be empty", guard_name="ssrf"))

    if len(url) > MAX_URL_LENGTH:
        return Err(
            SecurityError(
                "URL length exceeds maximum allowed limit",
                guard_name="ssrf",
                value=url[:80],
            ),
        )
    return Ok(url)


def _has_invalid_url_chars(url: str) -> bool:
    if any(c <= "\x20" or c == "\x7f" for c in url):
        return True
    return bool("\x00" in url or not url.isprintable())


def _check_ssrf_url_characters(url: str) -> Result[str, SecurityError]:
    if _has_invalid_url_chars(url) or _has_invalid_url_chars(unquote(url)):
        return Err(
            SecurityError(
                "URL contains invalid characters",
                guard_name="ssrf",
                value=url[:80],
            ),
        )
    return Ok(url)


def _validate_ssrf_url_type_and_length(url: str) -> Result[str, SecurityError]:
    length_res = _check_ssrf_url_length(url)
    if not isinstance(length_res, Ok):
        return length_res

    return _check_ssrf_url_characters(url)


def _validate_ssrf_url_parse(
    url: str,
    allowed_schemes: frozenset[str],
) -> Result[str, SecurityError]:
    try:
        parsed = urlsplit(url)
    except ValueError as exc:
        return Err(
            SecurityError(
                f"Malformed URL: {exc}",
                guard_name="ssrf",
                value=url[:80],
            ),
        )

    if not parsed.scheme or parsed.scheme.lower() not in allowed_schemes:
        return Err(
            SecurityError(
                f"URL scheme '{parsed.scheme}' is not allowed",
                guard_name="ssrf",
                value=url[:80],
            ),
        )

    hostname = parsed.hostname
    if not hostname:
        return Err(
            SecurityError(
                "URL has no resolvable hostname",
                guard_name="ssrf",
                value=url[:80],
            ),
        )

    return Ok(hostname)


def _validate_ssrf_url(
    url: str,
    allowed_schemes: frozenset[str],
) -> Result[str, SecurityError]:
    """Validate the URL format, scheme, and presence of hostname."""
    type_len_res = _validate_ssrf_url_type_and_length(url)
    if not isinstance(type_len_res, Ok):
        return type_len_res

    return _validate_ssrf_url_parse(url, allowed_schemes)


def _is_ip_address_unsafe_bounds(
    addr: ipaddress.IPv4Address | ipaddress.IPv6Address,
) -> bool:
    return addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_reserved


def _is_ip_address_safe(addr: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    """Evaluate if an ipaddress object represents a safe, public IP."""
    if _is_ip_address_unsafe_bounds(addr):
        return False
    return not (
        getattr(addr, "is_multicast", False) or getattr(addr, "is_unspecified", False)  # type: ignore[misc]
    )


@functools.lru_cache(maxsize=1024)  # type: ignore[misc]
def _is_ip_safe(raw_ip: str) -> bool:
    """Check if a single IP address is safe (not private/loopback/reserved)."""
    try:
        addr = ipaddress.ip_address(raw_ip)
    except ValueError:
        return True

    return _is_ip_address_safe(addr)


def _check_ip_safety(hostname: str) -> Result[None, SecurityError]:
    """Resolve hostname to IP addresses and check for SSRF risk."""
    try:
        addr_infos = socket.getaddrinfo(hostname, None)
    except (socket.gaierror, UnicodeError):
        return Err(
            SecurityError(
                "Hostname could not be resolved or contains invalid characters",
                guard_name="ssrf",
            ),
        )

    for addr_info in addr_infos:
        raw_ip = addr_info[4][0]
        if not _is_ip_safe(raw_ip):
            return Err(
                SecurityError(
                    "SSRF detected: hostname resolves to private/reserved address",
                    guard_name="ssrf",
                ),
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
    val_res = _validate_ssrf_url(url, allowed_schemes)
    if not isinstance(val_res, Ok):
        return val_res

    # 2. Check IP safety
    ip_res = _check_ip_safety(val_res.ok_value)
    if not isinstance(ip_res, Ok):
        return ip_res

    return Ok(url)
