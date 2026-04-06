import re

with open("src/taipanstack/bridges/http_bridge.py", "r") as f:
    content = f.read()

# Only keep the required ignore:
content = content.replace('self._client = httpx.AsyncClient(timeout=timeout, **self._client_kwargs)', 'self._client = httpx.AsyncClient(timeout=timeout, **self._client_kwargs)  # type: ignore[misc]')

with open("src/taipanstack/bridges/http_bridge.py", "w") as f:
    f.write(content)
