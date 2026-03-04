"""Stack Core Module.

Provides core functionality including Result types, version compatibility,
and optimization utilities.
"""

from taipanstack.core.optimizations import (
    OptimizationProfile,
    OptimizationResult,
    apply_optimizations,
    get_optimization_profile,
    get_recommended_thread_pool_size,
)
from taipanstack.core.result import Err, Ok, Result

__all__ = [
    "Err",
    "Ok",
    "OptimizationProfile",
    "OptimizationResult",
    "Result",
    "apply_optimizations",
    "get_optimization_profile",
    "get_recommended_thread_pool_size",
]
