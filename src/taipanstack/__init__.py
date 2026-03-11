"""
TaipanStack - Python Security & Quality Bootstrapper.

A modular, secure, and scalable Python stack for robust development.
Supports Python 3.11+ with version-aware optimizations for 3.13/3.14.
"""

__version__ = "0.3.9"

from taipanstack.config.version_config import (
    VersionRecommendations,
    get_version_recommendations,
)
from taipanstack.core.compat import (
    PY312,
    PY313,
    PY314,
    PY_VERSION,
    get_features,
    get_python_info,
)
from taipanstack.security.validators import (
    validate_email,
    validate_project_name,
    validate_python_version,
)

__all__ = [
    "PY312",
    "PY313",
    "PY314",
    "PY_VERSION",
    "VersionRecommendations",
    "get_features",
    "get_python_info",
    "get_version_recommendations",
    "validate_email",
    "validate_project_name",
    "validate_python_version",
]
