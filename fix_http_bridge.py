with open("src/taipanstack/bridges/http_bridge.py", "r") as f:
    content = f.read()

content = content.replace("Result[Any, Exception]", "Result['httpx.Response', Exception]")
content = content.replace("dict[str, Any]", "dict[str, Any] # type: ignore[misc]")

with open("src/taipanstack/bridges/http_bridge.py", "w") as f:
    f.write(content)
