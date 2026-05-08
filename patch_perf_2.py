with open('src/taipanstack/core/result.py', 'r') as f:
    content = f.read()

old_code = """def _collect_list(
    results: list[Result[T, E]] | tuple[Result[T, E], ...],
) -> Result[list[T], E] | None:
    # A list comprehension with a type guard avoids try/except performance hits
    # but still satisfies mypy. We check the first element fast path or just
    # iterate with type checking.

    # Pre-cache ok constructor for speed
    ok_cls = Ok

    # We do a two-pass approach or simple explicit isinstance with list comprehension
    # Mypy is satisfied if we use isinstance in comprehension but it's hard to early return.

    # The absolute fastest way in python is a list comprehension without checks,
    # but we need it to be safe.

    # Let's try an optimized loop:
    values: list[T] = []
    append = values.append
    for r in results:
        if type(r) is ok_cls:
            append(r.ok_value)
        else:
            if isinstance(r, ok_cls):
                append(r.ok_value)
            else:
                return None
    return ok_cls(values)"""

new_code = """def _collect_list(
    results: list[Result[T, E]] | tuple[Result[T, E], ...],
) -> Result[list[T], E] | None:
    try:
        # Note: mypy warns about `ok_value` not existing on Err, which is
        # handled by the AttributeError catch at runtime.
        # We explicitly cast to avoid mypy complaining about the missing attribute.
        return Ok([cast(Ok[T], r).ok_value for r in results])
    except AttributeError:
        return None"""

with open('src/taipanstack/core/result.py', 'w') as f:
    f.write(content.replace(old_code, new_code))
