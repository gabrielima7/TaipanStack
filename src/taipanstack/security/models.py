"""Secure base models."""

import json
import re
from typing import Any

from pydantic import BaseModel

from taipanstack.utils.logging import REDACTED_VALUE, SENSITIVE_KEY_PATTERNS

__all__ = ["SecureBaseModel"]

_SENSITIVE_KEY_REGEX = (
    re.compile("|".join(map(re.escape, SENSITIVE_KEY_PATTERNS)), re.IGNORECASE)
    if SENSITIVE_KEY_PATTERNS
    else None
)


def _mask_data(data: Any) -> Any:
    """Recursively mask sensitive keys in data."""
    if _SENSITIVE_KEY_REGEX is None:
        return data

    if isinstance(data, dict):
        masked = {}
        for k, v in data.items():
            if isinstance(k, str) and _SENSITIVE_KEY_REGEX.search(k):
                masked[k] = REDACTED_VALUE
            else:
                masked[k] = _mask_data(v)
        return masked
    elif isinstance(data, list):
        return [_mask_data(item) for item in data]
    return data


class SecureBaseModel(BaseModel):
    """Secure base model that redacts sensitive fields when dumped."""

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
        return _mask_data(data)  # type: ignore[no-any-return]

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
