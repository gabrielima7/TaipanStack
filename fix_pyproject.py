import re

with open("pyproject.toml", "r") as f:
    content = f.read()

# I also need to exclude abstractmethod bodies since they are just ... or pass
# Actually, the user asked me to keep `if TYPE_CHECKING:` and `@overload`.
# Wait, they originally had `exclude_lines = ["pragma: no cover", "if TYPE_CHECKING:", "@overload"]`
# But if we removed `@abstractmethod` from exclude_lines, then abstract method bodies will show as missing.
# Let's restore `@abstractmethod` to exclude_lines as well.
# Also the `def __call__` one is for Protocol.

new_exclude = """exclude_lines = [
    "if TYPE_CHECKING:",
    "@overload",
    "@abstractmethod",
    'def __call__\\\\(.*\\\\) -> .*:\\\\s*(?:\\"\\"\\".*?\\"\\"\\"\\\\s*)?\\\\.\\\\.\\\\.',
]"""

content = re.sub(r'exclude_lines = \[\n.*?\]', new_exclude, content, flags=re.DOTALL)

with open("pyproject.toml", "w") as f:
    f.write(content)
