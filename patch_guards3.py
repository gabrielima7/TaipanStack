import re

with open("src/taipanstack/security/guards.py", "r") as f:
    content = f.read()

content = content.replace(
    """def _check_denied_extension(
    ext: str,
    original_name: str,
    denied_extensions: Sequence[str] | None,
) -> None:
    if denied_extensions is not None:
        denied = frozenset(_normalize_ext(e) for e in denied_extensions if str(e).strip())
    else:
        denied = _DEFAULT_DENIED_EXTENSIONS""",
    """def _check_denied_extension(
    ext: str,
    original_name: str,
    denied_extensions: Sequence[str] | None,
) -> None:
    if denied_extensions is not None:
        denied = frozenset(
            _normalize_ext(e) for e in denied_extensions if str(e).strip()
        )
    else:
        denied = _DEFAULT_DENIED_EXTENSIONS"""
)

with open("src/taipanstack/security/guards.py", "w") as f:
    f.write(content)
