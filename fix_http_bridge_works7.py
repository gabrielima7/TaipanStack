import re

with open("src/taipanstack/bridges/http_bridge.py", "r") as f:
    content = f.read()

# Fix the final error: "AsyncClient" gets multiple values for keyword argument "timeout"
content = content.replace(
    'timeout = self._client_kwargs.pop("timeout", 10.0)  # type: ignore[misc]\n        self._client = httpx.AsyncClient(timeout=timeout, **self._client_kwargs)  # type: ignore[arg-type]',
    'timeout = self._client_kwargs.pop("timeout", 10.0)  # type: ignore[misc]\n        self._client = httpx.AsyncClient(timeout=timeout, **self._client_kwargs)  # type: ignore[arg-type, misc]'
)

with open("src/taipanstack/bridges/http_bridge.py", "w") as f:
    f.write(content)
