"""
Stack - Python Security & Quality Bootstrapper.

A modular, secure, and scalable Python stack for robust development.
Supports Python 3.11+ with version-aware optimizations for 3.13/3.14.
"""

__version__ = "2.1.0"

from stack.config.models import StackConfig
from stack.config.version_config import VersionRecommendations, get_version_recommendations
from stack.core.compat import (
    PY311,
    PY312,
    PY313,
    PY314,
    PY_VERSION,
    get_features,
    get_python_info,
)
from stack.core.optimizations import apply_optimizations, get_optimization_profile
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
    # Config
    "StackConfig",
    "VersionRecommendations",
    "get_version_recommendations",
    # Version detection
    "PY_VERSION",
    "PY311",
    "PY312",
    "PY313",
    "PY314",
    "get_features",
    "get_python_info",
    # Optimizations
    "apply_optimizations",
    "get_optimization_profile",
    # Security
    "guard_command_injection",
    "guard_path_traversal",
    "validate_email",
    "validate_project_name",
    "validate_python_version",
]
