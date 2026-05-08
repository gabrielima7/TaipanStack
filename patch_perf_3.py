with open('src/taipanstack/core/result.py', 'r') as f:
    content = f.read()

old_code = """def _collect_list(
    results: list[Result[T, E]] | tuple[Result[T, E], ...],
) -> Result[list[T], E] | None:
    try:
        # Note: mypy warns about `ok_value` not existing on Err, which is
        # handled by the AttributeError catch at runtime.
        # We explicitly cast to avoid mypy complaining about the missing attribute.
        return Ok([cast(Ok[T], r).ok_value for r in results])
    except AttributeError:
        return None"""

new_code = """def _collect_list(
    results: list[Result[T, E]] | tuple[Result[T, E], ...],
) -> Result[list[T], E] | None:
    try:
        # We use a runtime # type: ignore to bypass mypy's strict check
        # on the AttributeError strategy for extreme performance on the hot path
        return Ok([r.ok_value for r in results])  # type: ignore[union-attr]
    except AttributeError:
        return None"""

with open('src/taipanstack/core/result.py', 'w') as f:
    f.write(content.replace(old_code, new_code))
