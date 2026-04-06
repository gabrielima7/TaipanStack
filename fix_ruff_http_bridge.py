import re

with open("src/taipanstack/bridges/http_bridge.py", "r") as f:
    content = f.read()

# Fix docstrings
content = content.replace("class HttpxClientKwargs(TypedDict, total=False):", "class HttpxClientKwargs(TypedDict, total=False):\n        \"\"\"Type hints for httpx.AsyncClient initialization.\"\"\"")
content = content.replace("class HttpxRequestKwargs(TypedDict, total=False):", "class HttpxRequestKwargs(TypedDict, total=False):\n        \"\"\"Type hints for httpx request methods.\"\"\"")

# Fix line length (using line continuation for method signatures)
content = re.sub(
    r"async def (get|post|put|delete|patch)\(self, url: str, \*\*kw: Unpack\[HttpxRequestKwargs\]\) -> Result\[httpx.Response, Exception\]:",
    r"async def \1(\n        self, url: str, **kw: Unpack[HttpxRequestKwargs]\n    ) -> Result[httpx.Response, Exception]:",
    content
)

with open("src/taipanstack/bridges/http_bridge.py", "w") as f:
    f.write(content)
