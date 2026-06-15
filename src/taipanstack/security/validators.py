"""
Input validators for type-safe validation.

Provides validation functions for common input types like email,
project names, URLs, etc. All validators raise ValueError on invalid input.
"""

import re
from urllib.parse import SplitResult, unquote, urlsplit

# Constants to avoid magic values (PLR2004)
PYTHON_MAJOR_VERSION = 3
MIN_PYTHON_MINOR_VERSION = 10
MAX_PYTHON_VERSION_LENGTH = 20
MAX_EMAIL_LOCAL_LENGTH = 64
MAX_EMAIL_DOMAIN_LENGTH = 255
MAX_URL_LENGTH = 2048
MAX_ENV_VAR_LENGTH = 256
LOCALHOST_DOMAINS = ("localhost", "127.0.0.1", "::1")
PROJECT_NAME_RESERVED = frozenset(
    {
        "test",
        "tests",
        "src",
        "lib",
        "bin",
        "build",
        "dist",
        "setup",
        "config",
        "settings",
        "core",
        "main",
        "app",
        "site-packages",
    },
)


def _validate_type(
    value: object,
    expected_type: type | tuple[type, ...],
    name: str,
) -> None:
    """Validate input type.

    Args:
        value: The value to check.
        expected_type: The expected type(s).
        name: Name of the variable for the error message.

    Raises:
        TypeError: If value is not of the expected type.

    """
    if not isinstance(value, expected_type):
        type_name = (
            expected_type.__name__
            if isinstance(expected_type, type)
            else " | ".join(t.__name__ for t in expected_type)
        )
        msg = f"{name} must be {type_name}, got {type(value).__name__}"
        raise TypeError(msg)


def _check_project_name_length(name: str, max_length: int) -> None:
    """Check project name length.

    Args:
        name: The project name.
        max_length: Maximum allowed length.

    Raises:
        ValueError: If length is invalid.

    """
    if not name:
        msg = "Project name cannot be empty"
        raise ValueError(msg)

    if len(name) > max_length:
        msg = f"Project name exceeds maximum length of {max_length}"
        raise ValueError(msg)


def _build_project_name_pattern(allow_hyphen: bool, allow_underscore: bool) -> str:
    """Build the regex pattern for allowed characters."""
    allowed = r"a-zA-Z0-9"
    if allow_hyphen:
        allowed += r"-"
    if allow_underscore:
        allowed += r"_"
    return rf"^[a-zA-Z][{allowed}]*\Z"


def _build_invalid_chars_msg(allow_hyphen: bool, allow_underscore: bool) -> str:
    """Build the error message for invalid characters."""
    hyphen_msg = ", hyphens" if allow_hyphen else ""
    underscore_msg = ", underscores" if allow_underscore else ""
    return (
        f"Project name contains invalid characters. "
        f"Allowed: letters, numbers{hyphen_msg}{underscore_msg}"
    )


def _check_project_name_chars(
    name: str,
    allow_hyphen: bool,
    allow_underscore: bool,
) -> None:
    """Check project name characters.

    Args:
        name: The project name.
        allow_hyphen: Whether to allow hyphens.
        allow_underscore: Whether to allow underscores.

    Raises:
        ValueError: If name contains invalid characters.

    """
    pattern = _build_project_name_pattern(allow_hyphen, allow_underscore)

    if not re.match(pattern, name):
        if not name or not name[0].isalpha():
            msg = "Project name must start with a letter"
            raise ValueError(msg)
        msg = _build_invalid_chars_msg(allow_hyphen, allow_underscore)
        raise ValueError(msg)


def _check_project_name_reserved(name: str) -> None:
    """Check if project name is reserved.

    Args:
        name: The project name.

    Raises:
        ValueError: If name is reserved.

    """
    if name.lower() in PROJECT_NAME_RESERVED:
        msg = f"Project name '{name}' is reserved"
        raise ValueError(msg)


def validate_project_name(
    name: str,
    *,
    max_length: int = 100,
    allow_hyphen: bool = True,
    allow_underscore: bool = True,
) -> str:
    """Validate a project name.

    Args:
        name: The project name to validate.
        max_length: Maximum allowed length.
        allow_hyphen: Allow hyphens in name.
        allow_underscore: Allow underscores in name.

    Returns:
        The validated project name.

    Raises:
        ValueError: If the name is invalid.

    Example:
        >>> validate_project_name("my_project")
        'my_project'
        >>> validate_project_name("123project")
        ValueError: Project name must start with a letter

    """
    _validate_type(name, str, "Project name")
    _check_project_name_length(name, max_length)
    _check_project_name_chars(name, allow_hyphen, allow_underscore)
    _check_project_name_reserved(name)

    return name


def _check_version_format(version: str) -> None:
    """Check the basic formatting and safety of a version string."""
    # Prevent DoS from massive integer string conversion limit in Python
    if len(version) > MAX_PYTHON_VERSION_LENGTH:
        msg = "Version string exceeds maximum length"
        raise ValueError(msg)

    if "\x00" in version or not version.isprintable():
        msg = "Version contains invalid characters"
        raise ValueError(msg)

    if not version.isascii():
        msg = f"Invalid version format: '{version}'. Use 'X.Y' format (e.g., '3.12')"
        raise ValueError(msg)

    pattern = r"^\d+\.\d+\Z"

    if not re.match(pattern, version):
        msg = f"Invalid version format: '{version}'. Use 'X.Y' format (e.g., '3.12')"
        raise ValueError(msg)


def _check_version_numbers(version: str) -> None:
    """Check the major and minor version numbers."""
    try:
        major, minor = map(int, version.split("."))
    except ValueError as e:
        msg = f"Invalid version numbers in '{version}'"
        raise ValueError(msg) from e

    if major != PYTHON_MAJOR_VERSION:
        msg = f"Only Python 3.x is supported, got {major}.x"
        raise ValueError(msg)

    if minor < MIN_PYTHON_MINOR_VERSION:
        msg = (
            f"Python 3.{minor} is not supported. "
            f"Minimum is 3.{MIN_PYTHON_MINOR_VERSION}"
        )
        raise ValueError(msg)


def validate_python_version(version: str) -> str:
    """Validate Python version string.

    Args:
        version: Version string like "3.12" or "3.10".

    Returns:
        The validated version string.

    Raises:
        ValueError: If version format is invalid or unsupported.

    """
    _validate_type(version, str, "Version")
    _check_version_format(version)
    _check_version_numbers(version)
    return version


def _check_email_basics(email: str) -> None:
    """Check basic email constraints like empty, length and invalid characters."""
    if not email:
        msg = "Email cannot be empty"
        raise ValueError(msg)

    if len(email) > MAX_EMAIL_LOCAL_LENGTH + 1 + MAX_EMAIL_DOMAIN_LENGTH:
        msg = "Email length exceeds maximum allowed"
        raise ValueError(msg)

    if "\x00" in email or not email.isprintable():
        msg = "Email contains invalid characters"
        raise ValueError(msg)


def _check_email_format(email: str) -> None:
    """Check email format and basic constraints."""
    _check_email_basics(email)

    # RFC 5322 compliant pattern (simplified)
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\Z"

    if not re.match(pattern, email):
        msg = f"Invalid email format: {email}"
        raise ValueError(msg)


def _check_email_parts(email: str) -> None:
    """Check local and domain parts of the email."""
    local, domain = email.rsplit("@", 1)

    if len(local) > MAX_EMAIL_LOCAL_LENGTH:
        msg = f"Email local part exceeds {MAX_EMAIL_LOCAL_LENGTH} characters"
        raise ValueError(msg)

    if len(domain) > MAX_EMAIL_DOMAIN_LENGTH:
        msg = f"Email domain exceeds {MAX_EMAIL_DOMAIN_LENGTH} characters"
        raise ValueError(msg)


def validate_email(email: str) -> str:
    """Validate email address format.

    Uses a reasonable regex pattern that covers most valid emails
    without being overly strict.

    Args:
        email: The email address to validate.

    Returns:
        The validated email address.

    Raises:
        ValueError: If email format is invalid.

    """
    _validate_type(email, str, "Email")
    _check_email_format(email)
    _check_email_parts(email)
    return email


def _check_url_length(url: str) -> None:
    """Check URL length constraints."""
    if not url:
        msg = "URL cannot be empty"
        raise ValueError(msg)

    if len(url) > MAX_URL_LENGTH:
        msg = f"URL length exceeds maximum allowed length of {MAX_URL_LENGTH}"
        raise ValueError(msg)


def _has_invalid_url_chars(url: str) -> bool:
    if any(c <= "\x20" or c == "\x7f" for c in url):
        return True
    return bool("\x00" in url or not url.isprintable())


def _check_url_characters(url: str) -> None:
    """Check URL character constraints."""
    if _has_invalid_url_chars(url) or _has_invalid_url_chars(unquote(url)):
        msg = "URL contains invalid characters"
        raise ValueError(msg)


def _check_url_basics(url: str) -> None:
    """Check basic URL constraints like empty, length and invalid characters."""
    _validate_type(url, str, "URL")
    _check_url_length(url)
    _check_url_characters(url)


def _check_scheme(
    parsed: SplitResult,
    allowed_schemes: tuple[str, ...],
) -> None:
    """Validate the URL scheme."""
    if not parsed.scheme:
        msg = "URL must have a scheme (e.g., https://)"
        raise ValueError(msg)

    if parsed.scheme not in allowed_schemes:
        msg = f"URL scheme '{parsed.scheme}' is not allowed. Allowed: {allowed_schemes}"
        raise ValueError(msg)


def _check_tld(domain: str) -> None:
    """Validate that the domain has a TLD."""
    has_no_tld = "." not in domain or domain.endswith(".")
    is_localhost = domain.lower() in LOCALHOST_DOMAINS
    if has_no_tld and not is_localhost:
        msg = f"URL domain must have a TLD: {domain}"
        raise ValueError(msg)


def _check_url_domain(
    parsed: SplitResult,
    allowed_schemes: tuple[str, ...],
    require_tld: bool,
) -> None:
    """Validate URL scheme and domain."""
    _check_scheme(parsed, allowed_schemes)

    if not parsed.hostname:
        msg = "URL must have a domain"
        raise ValueError(msg)

    if require_tld:
        _check_tld(parsed.hostname)


def validate_url(
    url: str,
    *,
    allowed_schemes: tuple[str, ...] = ("http", "https"),
    require_tld: bool = True,
) -> str:
    """Validate URL format and scheme.

    Args:
        url: The URL to validate.
        allowed_schemes: Tuple of allowed URL schemes.
        require_tld: Whether to require a TLD in the domain.

    Returns:
        The validated URL.

    Raises:
        ValueError: If URL format is invalid.

    """
    _check_url_basics(url)

    try:
        parsed = urlsplit(url)
        _ = parsed.port
    except ValueError as e:
        msg = f"Invalid URL format: {e}"
        raise ValueError(msg) from e

    _check_url_domain(parsed, allowed_schemes, require_tld)

    return url
