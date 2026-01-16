"""Stack Core Module.

Provides core functionality including Result types, version compatibility,
and optimization utilities.
"""

from stack.core.compat import (
    PY311,
    PY312,
    PY313,
    PY314,
    PY_VERSION,
    PythonFeatures,
    VersionTier,
    get_features,
    get_python_info,
    is_experimental_enabled,
)
from stack.core.optimizations import (
    OptimizationProfile,
    OptimizationResult,
    apply_optimizations,
    get_optimization_profile,
    get_recommended_thread_pool_size,
)
from stack.core.result import Err, Ok, Result

__all__ = [
    # Result types
    "Result",
    "Ok",
    "Err",
    # Version detection
    "PY_VERSION",
    "PY311",
    "PY312",
    "PY313",
    "PY314",
    "VersionTier",
    "PythonFeatures",
    "get_features",
    "get_python_info",
    "is_experimental_enabled",
    # Optimizations
    "OptimizationProfile",
    "OptimizationResult",
    "get_optimization_profile",
    "apply_optimizations",
    "get_recommended_thread_pool_size",
]
