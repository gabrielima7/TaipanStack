import re

with open("src/taipanstack/security/sanitizers.py", "r") as f:
    content = f.read()

search = '''def sanitize_sql_identifier(identifier: str) -> str:
    """Sanitize a SQL identifier (table/column name).

    Note: This is NOT for SQL values - use parameterized queries for those!

    Args:
        identifier: The identifier to sanitize.

    Returns:
        The sanitized identifier.

    Raises:
        TypeError: If identifier is not a string.
        ValueError: If identifier is empty or too long.

    """
    if type(identifier) is str:
        if (
            len(identifier) <= 128  # noqa: PLR2004
            and identifier.isascii()
            and identifier.isidentifier()
        ):
            return identifier

        if not identifier:
            msg = "SQL identifier cannot be empty"
            raise ValueError(msg)

        return _sanitize_sql_identifier_slow_path(identifier)

    raise TypeError(f"identifier must be str, got {type(identifier).__name__}")'''

replace = '''def sanitize_sql_identifier(identifier: str) -> str:
    """Sanitize a SQL identifier (table/column name).

    Note: This is NOT for SQL values - use parameterized queries for those!

    Args:
        identifier: The identifier to sanitize.

    Returns:
        The sanitized identifier.

    Raises:
        TypeError: If identifier is not a string.
        ValueError: If identifier is empty or too long.

    """
    if type(identifier) is str:
        if (
            len(identifier) <= 128  # noqa: PLR2004
            and identifier.isascii()
            and identifier.isidentifier()
        ):
            return identifier

        if not identifier:
            msg = "SQL identifier cannot be empty"
            raise ValueError(msg)

        return _sanitize_sql_identifier_slow_path(identifier)

    raise TypeError(f"identifier must be str, got {type(identifier).__name__}")'''

if search in content:
    content = content.replace(search, replace)
    with open("src/taipanstack/security/sanitizers.py", "w") as f:
        f.write(content)
    print("Success")
else:
    print("Search string not found")
