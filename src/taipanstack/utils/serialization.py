"""
Serialization utilities.

Provides an optimized default encoder for use with ``orjson.dumps``.
"""

from taipanstack.core.result import Err, Ok

__all__ = ["default_encoder"]


def default_encoder(obj: object) -> dict[str, object]:
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
    match obj:
        case Ok(ok_value) if isinstance(ok_value, dict):
            return {"status": "success", **ok_value}
        case Ok(ok_value):
            return {"status": "success", "data": ok_value}
        case Err(err_value):
            return {"status": "error", "message": str(err_value)}
        case _:
            raise TypeError(f"Type {type(obj).__name__} is not JSON serializable")
