import re

with open("src/taipanstack/bridges/http_bridge.py", "r") as f:
    content = f.read()

content = content.replace("dict[str, Any] # type: ignore[misc]", "dict[str, Any]")

# The kwargs are Any.
content = re.sub(r"\*\*kwargs: Any", r"**kwargs: Any  # type: ignore[misc]", content)
content = re.sub(r"\*\*kw: Any", r"**kw: Any  # type: ignore[misc]", content)
content = re.sub(r"\*\*client_kwargs: Any", r"**client_kwargs: Any  # type: ignore[misc]", content)

with open("src/taipanstack/bridges/http_bridge.py", "w") as f:
    f.write(content)
