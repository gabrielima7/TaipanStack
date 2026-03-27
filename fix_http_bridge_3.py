with open("src/taipanstack/bridges/http_bridge.py", "r") as f:
    content = f.read()

content = content.replace("self._client: Any = None", "self._client: 'httpx.AsyncClient | None' = None")

with open("src/taipanstack/bridges/http_bridge.py", "w") as f:
    f.write(content)
