"""
Lazy optional import helpers for Taipan Bridges.

Provides a centralised mechanism to handle optional dependencies
that may or may not be installed at runtime.
"""

import importlib
import types

from taipanstack.core.result import Err, Ok, Result


def require_dependency(
    module_name: str,
    *,
    pip_extra: str = "",
) -> Result[types.ModuleType, ImportError]:
    """Attempt to import *module_name* and return a ``Result``.

    Args:
        module_name: Dotted module path (e.g. ``"httpx"``).
        pip_extra: Optional pip extra name for the error message.

    Returns:
        ``Ok(module)`` if available, ``Err(ImportError)`` otherwise.

    Example:
        >>> require_dependency("httpx", pip_extra="bridges-http")
        Ok(<module 'httpx' ...>)

    """
    try:
        mod = importlib.import_module(module_name)  # nosem
        return Ok(mod)
    except ImportError:
        install_hint = (
            f"pip install taipanstack[{pip_extra}]"
            if pip_extra
            else f"pip install {module_name}"
        )
        return Err(
            ImportError(
                f"'{module_name}' is required but not installed. "
                f"Install with: {install_hint}",
            ),
        )


def get_attr_or_err(
    module: types.ModuleType,
    name: str,
) -> Result[object, AttributeError]:
    """Safely access an attribute from a module.

    Args:
        module: The imported module.
        name: Attribute name to retrieve.

    Returns:
        ``Ok(attr)`` if found, ``Err(AttributeError)`` otherwise.

    """
    try:
        return Ok(getattr(module, name))
    except AttributeError as exc:
        return Err(exc)
