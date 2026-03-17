"""Secure base models."""

import json
import re
from collections.abc import Iterator
from typing import Any, TypeAlias

from pydantic import BaseModel, ConfigDict

from taipanstack.utils.logging import REDACTED_VALUE, SENSITIVE_KEY_PATTERNS

JSONValue: TypeAlias = (
    dict[str, "JSONValue"] | list["JSONValue"] | str | int | float | bool | None
)

__all__ = ["SecureBaseModel"]

_SENSITIVE_KEY_REGEX = (
    re.compile("|".join(map(re.escape, SENSITIVE_KEY_PATTERNS)), re.IGNORECASE)
    if SENSITIVE_KEY_PATTERNS
    else None
)


def _mask_data(data: JSONValue) -> JSONValue:
    """Recursively mask sensitive keys in data."""
    if _SENSITIVE_KEY_REGEX is None:
        return data

    if isinstance(data, dict):
        masked: dict[str, JSONValue] = {}
        for k, v in data.items():
            if isinstance(k, str) and _SENSITIVE_KEY_REGEX.search(k):
                masked[k] = REDACTED_VALUE
            else:
                masked[k] = _mask_data(v)
        return masked
    if isinstance(data, list):
        return [_mask_data(item) for item in data]
    return data


class SecureBaseModel(BaseModel):
    """Secure base model that redacts sensitive fields when dumped."""

    model_config = ConfigDict(frozen=True)

    def __str__(self) -> str:
        """Return a string representation with sensitive fields redacted."""
        return self.__repr__()

    def __repr_args__(self) -> Iterator[tuple[str | None, object]]:
        """Provide arguments for string representation, redacting sensitive fields."""
        for k, v in super().__repr_args__():
            if (
                isinstance(k, str)
                and _SENSITIVE_KEY_REGEX is not None
                and _SENSITIVE_KEY_REGEX.search(k)
            ):
                yield k, REDACTED_VALUE
            else:
                yield k, v

    def model_dump(
        self,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Dump the model to a dictionary, redacting sensitive fields.

        Args:
            **kwargs: Arguments to pass to Pydantic's model_dump.

        Returns:
            The redacting dictionary representation of the model.

        """
        data = super().model_dump(**kwargs)
        return _mask_data(data)  # type: ignore[return-value]

    def model_dump_json(
        self,
        **kwargs: Any,
    ) -> str:
        """Dump the model to a JSON string, redacting sensitive fields.

        Args:
            **kwargs: Arguments to pass to Pydantic's model_dump.

        Returns:
            The redacted JSON string representation of the model.

        """
        # Extract indent if any, as model_dump does not accept it
        indent = kwargs.pop("indent", None)
        # Dump to JSON-compatible dict, mask, then serialize
        dumped_dict = super().model_dump(mode="json", **kwargs)
        masked_dict = _mask_data(dumped_dict)
        # We need to respect Pydantic's indent/separators if possible,
        # but json.dumps is the safest standard way.
        if indent is not None:
            return json.dumps(masked_dict, indent=indent)
        return json.dumps(masked_dict)
