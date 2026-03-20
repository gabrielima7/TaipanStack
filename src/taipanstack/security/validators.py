"""
Input validators for type-safe validation.

Provides validation functions for common input types like email,
project names, URLs, etc. All validators raise ValueError on invalid input.
"""

import re
from urllib.parse import urlparse

# Constants to avoid magic values (PLR2004)
PYTHON_MAJOR_VERSION = 3
MIN_PYTHON_MINOR_VERSION = 10
MAX_EMAIL_LOCAL_LENGTH = 64
MAX_EMAIL_DOMAIN_LENGTH = 255
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
    }
)


def _validate_type(
    value: object, expected_type: type | tuple[type, ...], name: str
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


def _check_project_name_chars(
    name: str, allow_hyphen: bool, allow_underscore: bool
) -> None:
    """Check project name characters.

    Args:
        name: The project name.
        allow_hyphen: Whether to allow hyphens.
        allow_underscore: Whether to allow underscores.

    Raises:
        ValueError: If name contains invalid characters.

    """
    # Build allowed characters
    allowed = r"a-zA-Z0-9"
    if allow_hyphen:
        allowed += r"-"
    if allow_underscore:
        allowed += r"_"

    pattern = f"^[a-zA-Z][{allowed}]*\\Z"

    if not re.match(pattern, name):
        if not name[0].isalpha():
            msg = "Project name must start with a letter"
            raise ValueError(msg)
        hyphen_msg = ", hyphens" if allow_hyphen else ""
        underscore_msg = ", underscores" if allow_underscore else ""
        msg = (
            f"Project name contains invalid characters. "
            f"Allowed: letters, numbers{hyphen_msg}{underscore_msg}"
        )
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

    pattern = r"^\d+\.\d+\Z"

    if not re.match(pattern, version):
        msg = f"Invalid version format: '{version}'. Use 'X.Y' format (e.g., '3.12')"
        raise ValueError(msg)

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

    return version


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

    if not email:
        msg = "Email cannot be empty"
        raise ValueError(msg)

    # RFC 5322 compliant pattern (simplified)
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\Z"

    if not re.match(pattern, email):
        msg = f"Invalid email format: {email}"
        raise ValueError(msg)

    # Additional checks
    local, domain = email.rsplit("@", 1)

    if len(local) > MAX_EMAIL_LOCAL_LENGTH:
        msg = f"Email local part exceeds {MAX_EMAIL_LOCAL_LENGTH} characters"
        raise ValueError(msg)

    if len(domain) > MAX_EMAIL_DOMAIN_LENGTH:
        msg = f"Email domain exceeds {MAX_EMAIL_DOMAIN_LENGTH} characters"
        raise ValueError(msg)

    return email


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
    _validate_type(url, str, "URL")

    if not url:
        msg = "URL cannot be empty"
        raise ValueError(msg)

    try:
        parsed = urlparse(url)
        _ = parsed.port
    except ValueError as e:
        msg = f"Invalid URL format: {e}"
        raise ValueError(msg) from e

    if not parsed.scheme:
        msg = "URL must have a scheme (e.g., https://)"
        raise ValueError(msg)

    if parsed.scheme not in allowed_schemes:
        msg = f"URL scheme '{parsed.scheme}' is not allowed. Allowed: {allowed_schemes}"
        raise ValueError(msg)

    if not parsed.netloc:
        msg = "URL must have a domain"
        raise ValueError(msg)

    if require_tld:
        # Check for TLD (at least one dot)
        domain = parsed.netloc.split(":")[0]  # Remove port if present
        has_no_tld = "." not in domain or domain.endswith(".")
        is_localhost = domain.lower() in LOCALHOST_DOMAINS
        if has_no_tld and not is_localhost:
            msg = f"URL domain must have a TLD: {domain}"
            raise ValueError(msg)

    return url
