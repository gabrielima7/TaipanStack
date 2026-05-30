"""Secure base models."""

import json
import re
from collections.abc import Callable, Iterator
from typing import TYPE_CHECKING, Literal, TypeAlias, cast

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from pydantic.main import IncEx
else:
    IncEx: TypeAlias = set[int] | set[str] | dict[int, object] | dict[str, object]

from taipanstack.utils.logging import REDACTED_VALUE, SENSITIVE_KEY_PATTERNS

__all__ = ["SecureBaseModel"]

_SENSITIVE_KEY_REGEX = (
    re.compile("|".join(map(re.escape, SENSITIVE_KEY_PATTERNS)), re.IGNORECASE)
    if SENSITIVE_KEY_PATTERNS
    else None
)

_MAX_RECURSION_DEPTH = 100


def _mask_dict(data: dict[str, object], depth: int) -> dict[str, object]:
    """Mask sensitive keys in a dictionary."""
    masked: dict[str, object] = {}
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


def _mask_list(data: list[object], depth: int) -> list[object]:
    """Mask sensitive keys in a list."""
    return [_mask_data(item, depth) for item in data]


def _mask_tuple(data: tuple[object, ...], depth: int) -> tuple[object, ...]:
    """Mask sensitive keys in a tuple."""
    return tuple(_mask_data(item, depth) for item in data)


def _mask_set(data: set[object], depth: int) -> set[object]:
    """Mask sensitive keys in a set."""
    return {_mask_data(item, depth) for item in data}


def _mask_data(data: object, _depth: int = 0) -> object:  # noqa: PLR0911
    """Recursively mask sensitive keys in data."""
    if _SENSITIVE_KEY_REGEX is None:
        return data

    # Prevent ReDoS or stack overflow on deeply nested payloads
    if _depth > _MAX_RECURSION_DEPTH:
        return "<MAX_DEPTH_REACHED>"

    if isinstance(data, dict):
        # The cast ensures that we type check against the dictionary types,
        # but technically we only mask string keys in dicts in Pydantic.
        # We can safely cast it because Pydantic mostly yields dict[str, object].
        return _mask_dict(cast(dict[str, object], data), _depth + 1)
    if isinstance(data, list):
        return _mask_list(cast(list[object], data), _depth + 1)
    if isinstance(data, tuple):
        return _mask_tuple(cast(tuple[object, ...], data), _depth + 1)
    if isinstance(data, set):
        return _mask_set(cast(set[object], data), _depth + 1)
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

    def model_dump(  # noqa: PLR0913
        self,
        *,
        mode: Literal["json", "python"] | str = "python",
        include: IncEx | None = None,
        exclude: IncEx | None = None,
        context: dict[str, object] | None = None,
        by_alias: bool | None = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        exclude_computed_fields: bool = False,
        round_trip: bool = False,
        warnings: bool | Literal["none", "warn", "error"] = True,
        fallback: Callable[[object], object] | None = None,
        serialize_as_any: bool = False,
        **kwargs: object,
    ) -> dict[str, object]:
        """Dump the model to a dictionary, redacting sensitive fields.

        Returns:
            The redacting dictionary representation of the model.

        """
        data = super().model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            exclude_computed_fields=exclude_computed_fields,
            round_trip=round_trip,
            warnings=warnings,
            fallback=fallback,
            serialize_as_any=serialize_as_any,
            **kwargs,  # type: ignore[arg-type]
        )
        return cast(dict[str, object], _mask_data(data))

    def model_dump_json(  # noqa: PLR0913
        self,
        *,
        indent: int | None = None,
        ensure_ascii: bool = False,
        include: IncEx | None = None,
        exclude: IncEx | None = None,
        context: dict[str, object] | None = None,
        by_alias: bool | None = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        exclude_computed_fields: bool = False,
        round_trip: bool = False,
        warnings: bool | Literal["none", "warn", "error"] = True,
        fallback: Callable[[object], object] | None = None,
        serialize_as_any: bool = False,
        **kwargs: object,
    ) -> str:
        """Dump the model to a JSON string, redacting sensitive fields.

        Returns:
            The redacted JSON string representation of the model.

        """
        # Extract indent if any, as model_dump does not accept it

        # Dump to JSON-compatible dict, mask, then serialize
        dumped_dict = super().model_dump(
            mode="json",
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            exclude_computed_fields=exclude_computed_fields,
            round_trip=round_trip,
            warnings=warnings,
            fallback=fallback,
            serialize_as_any=serialize_as_any,
            **kwargs,  # type: ignore[arg-type]
        )
        masked_dict = _mask_data(dumped_dict)
        # We need to respect Pydantic's indent/separators if possible,
        # but json.dumps is the safest standard way.
        if indent is not None:
            return json.dumps(masked_dict, indent=indent, ensure_ascii=ensure_ascii)
        return json.dumps(masked_dict, ensure_ascii=ensure_ascii)
