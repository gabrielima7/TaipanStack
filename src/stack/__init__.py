"""
Stack - Python Security & Quality Bootstrapper.

A modular, secure, and scalable Python stack for robust development.
"""

__version__ = "2.0.0"

from stack.config.models import StackConfig
from stack.security.guards import (
    guard_command_injection,
    guard_path_traversal,
)
from stack.security.validators import (
    validate_email,
    validate_project_name,
    validate_python_version,
)

__all__ = [
    "StackConfig",
    "guard_command_injection",
    "guard_path_traversal",
    "validate_email",
    "validate_project_name",
    "validate_python_version",
]
