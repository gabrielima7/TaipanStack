"""
Pydantic-compatible security types.

Provide ``Annotated`` type aliases that integrate TaipanStack's
runtime security guards with Pydantic v2 validation, enabling
declarative, type-safe input validation inside ``BaseModel``
definitions.
"""

import html
import re
from typing import Annotated

from pydantic.functional_validators import AfterValidator

from taipanstack.core.result import Err, Ok
from taipanstack.security.guards import (
    SecurityError,
    guard_command_injection,
    guard_path_traversal,
    guard_ssrf,
)
from taipanstack.security.validators import (
    validate_project_name,
    validate_url,
)


def _validate_safe_url(url: str) -> str:
    """Validate a URL is safe from SSRF attacks.

    Args:
        url: The URL string to validate.

    Returns:
        The validated URL.

    Raises:
        ValueError: If the URL fails SSRF validation.

    """
    match guard_ssrf(url):
        case Ok(val):
            return val
        case Err(err):
            raise ValueError(str(err)) from err


def _validate_safe_path(path: str) -> str:
    """Validate a path is safe from traversal attacks.

    Args:
        path: The path string to validate.

    Returns:
        The validated path string.

    Raises:
        ValueError: If path traversal is detected.

    """
    try:
        guard_path_traversal(path)
    except SecurityError as exc:
        raise ValueError(str(exc)) from exc
    return path


def _validate_safe_command(command: str) -> str:
    """Validate a command string is safe from injection attacks.

    Args:
        command: The command string to validate.

    Returns:
        The validated command string.

    Raises:
        ValueError: If command injection is detected.

    """
    try:
        guard_command_injection([command])
    except SecurityError as exc:
        raise ValueError(str(exc)) from exc
    return command


def _validate_safe_project_name(name: str) -> str:
    """Validate a project name conforms to safe naming rules.

    Args:
        name: The project name to validate.

    Returns:
        The validated project name.

    Raises:
        ValueError: If the name is invalid.

    """
    return validate_project_name(name)


def _validate_safe_url_format(url: str) -> str:
    """Validate a URL has a correct format and allowed scheme.

    Args:
        url: The URL string to validate.

    Returns:
        The validated URL.

    Raises:
        ValueError: If the URL format is invalid.

    """
    return validate_url(url)


SafeUrl = Annotated[
    str,
    AfterValidator(_validate_safe_url_format),
    AfterValidator(_validate_safe_url),
]
"""A URL validated for correct format and safe from SSRF attacks."""

SafePath = Annotated[str, AfterValidator(_validate_safe_path)]
"""A filesystem path validated against path-traversal attacks."""

SafeCommand = Annotated[str, AfterValidator(_validate_safe_command)]
"""A command string validated against shell-injection attacks."""

SafeProjectName = Annotated[str, AfterValidator(_validate_safe_project_name)]
"""A project name validated for safe naming conventions."""


_SQL_IDENTIFIER_REGEX = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")


def _sanitize_safe_html(text: str) -> str:
    """Sanitize a string to prevent XSS attacks.

    Args:
        text: The string to sanitize.

    Returns:
        The HTML-escaped string.

    """
    return html.escape(text)


def _validate_safe_sql_identifier(identifier: str) -> str:
    """Validate a string is a safe SQL identifier.

    Args:
        identifier: The SQL identifier to validate.

    Returns:
        The validated SQL identifier.

    Raises:
        ValueError: If the identifier implies SQL injection risk.

    """
    if not _SQL_IDENTIFIER_REGEX.match(identifier):
        raise ValueError(
            f"Invalid SQL identifier: '{identifier}'. "
            "Must match ^[a-zA-Z_][a-zA-Z0-9_]*$"
        )
    return identifier


SafeHtml = Annotated[str, AfterValidator(_sanitize_safe_html)]
"""A string sanitized for safe inclusion in HTML templates."""

SafeSqlIdentifier = Annotated[str, AfterValidator(_validate_safe_sql_identifier)]
"""A string validated as a safe dynamic SQL identifier (e.g., table or column name)."""
