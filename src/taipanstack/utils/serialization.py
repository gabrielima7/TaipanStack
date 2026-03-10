"""
Serialization utilities.

Provides an optimized default encoder for use with ``orjson.dumps``.
"""

from typing import Any

from taipanstack.core.result import Err, Ok

__all__ = ["default_encoder"]


def default_encoder(obj: Any) -> dict[str, Any]:
    """Default encoder for orjson.dumps handling Result types.

    Intercepts objects of type ``Ok`` and ``Err``:
      - ``Ok(value)``: Returns ``{"status": "success"}`` merged with ``value`` if
        ``value`` is a dict. Otherwise returns ``{"status": "success", "data": value}``.
      - ``Err(error)``: Returns ``{"status": "error", "message": str(error)}``.

    Args:
        obj: The object to encode.

    Returns:
        A serializable representation of the object.

    Raises:
        TypeError: If the object type is not supported.

    Example:
        >>> import orjson
        >>> orjson.dumps(Ok({"id": 1}), default=default_encoder)
        b'{"status":"success","id":1}'
        >>> orjson.dumps(Err(ValueError("oops")), default=default_encoder)
        b'{"status":"error","message":"oops"}'

    """
    if isinstance(obj, Ok):
        if isinstance(obj.value, dict):
            return {"status": "success", **obj.value}
        return {"status": "success", "data": obj.value}

    if isinstance(obj, Err):
        return {"status": "error", "message": str(obj.value)}

    raise TypeError(f"Type {type(obj).__name__} is not JSON serializable")
