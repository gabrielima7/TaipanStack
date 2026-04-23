"""Secure base models."""

import json
import re
from collections.abc import Callable, Iterator
from typing import Literal, TypeAlias, cast

from pydantic import BaseModel, ConfigDict
from pydantic.main import IncEx
from typing_extensions import TypedDict, Unpack

from taipanstack.utils.logging import REDACTED_VALUE, SENSITIVE_KEY_PATTERNS


class ModelDumpKwargs(TypedDict, total=False):
    """Type definitions for Pydantic model_dump kwargs."""

    mode: Literal["json", "python"] | str
    include: IncEx | None
    exclude: IncEx | None
    context: dict[str, object] | None
    by_alias: bool | None
    exclude_unset: bool
    exclude_defaults: bool
    exclude_none: bool
    exclude_computed_fields: bool
    round_trip: bool
    warnings: bool | Literal["none", "warn", "error"]
    fallback: Callable[[object], object] | None
    serialize_as_any: bool
    polymorphic_serialization: bool | None

class ModelDumpJsonKwargs(TypedDict, total=False):
    """Type definitions for Pydantic model_dump_json kwargs."""

    indent: int | None
    ensure_ascii: bool
    fallback: Callable[[object], object] | None
    polymorphic_serialization: bool | None
    include: IncEx | None
    exclude: IncEx | None
    context: dict[str, object] | None
    by_alias: bool | None
    exclude_unset: bool
    exclude_defaults: bool
    exclude_none: bool
    exclude_computed_fields: bool
    round_trip: bool
    warnings: bool | Literal["none", "warn", "error"]
    serialize_as_any: bool

JSONValue: TypeAlias = (
    dict[str, "JSONValue"] | list["JSONValue"] | str | int | float | bool | None
)

__all__ = ["SecureBaseModel"]

_SENSITIVE_KEY_REGEX = (
    re.compile("|".join(map(re.escape, SENSITIVE_KEY_PATTERNS)), re.IGNORECASE)
    if SENSITIVE_KEY_PATTERNS
    else None
)

_MAX_RECURSION_DEPTH = 100


def _mask_dict(data: dict[str, JSONValue], depth: int) -> dict[str, JSONValue]:
    """Mask sensitive keys in a dictionary."""
    masked: dict[str, JSONValue] = {}
    for k, v in data.items():
        if (
            isinstance(k, str)
            and _SENSITIVE_KEY_REGEX is not None
            and _SENSITIVE_KEY_REGEX.search(k)
        ):
            masked[k] = REDACTED_VALUE
        else:
            masked[k] = _mask_data(v, depth)
    return masked


def _mask_list(data: list[JSONValue], depth: int) -> list[JSONValue]:
    """Mask sensitive keys in a list."""
    return [_mask_data(item, depth) for item in data]


def _mask_data(data: JSONValue, _depth: int = 0) -> JSONValue:
    """Recursively mask sensitive keys in data."""
    if _SENSITIVE_KEY_REGEX is None:
        return data

    # Prevent ReDoS or stack overflow on deeply nested payloads
    if _depth > _MAX_RECURSION_DEPTH:
        return "<MAX_DEPTH_REACHED>"

    match data:
        case dict():
            return _mask_dict(data, _depth + 1)
        case list():
            return _mask_list(data, _depth + 1)
        case _:
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
        **kwargs: Unpack[ModelDumpKwargs],
    ) -> dict[str, object]:
        """Dump the model to a dictionary, redacting sensitive fields.

        Args:
            **kwargs: Arguments to pass to Pydantic's model_dump.

        Returns:
            The redacting dictionary representation of the model.

        """
        data = super().model_dump(**kwargs)
        return cast(dict[str, object], _mask_data(data))

    def model_dump_json(
        self,
        **kwargs: Unpack[ModelDumpJsonKwargs],
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
        dump_kwargs = cast(dict[str, object], kwargs.copy())
        dump_kwargs["mode"] = "json"
        dumped_dict = super().model_dump(**cast(ModelDumpKwargs, dump_kwargs))
        masked_dict = _mask_data(dumped_dict)
        # We need to respect Pydantic's indent/separators if possible,
        # but json.dumps is the safest standard way.
        if indent is not None:
            return json.dumps(masked_dict, indent=cast(int | str, indent))
        return json.dumps(masked_dict)
