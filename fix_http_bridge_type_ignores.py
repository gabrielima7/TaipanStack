import re

with open("src/taipanstack/bridges/http_bridge.py", "r") as f:
    content = f.read()

# Remove unused type ignores
content = content.replace("HttpxClientKwargs = dict  # type: ignore[misc, assignment]", "HttpxClientKwargs = dict")
content = content.replace("HttpxRequestKwargs = dict  # type: ignore[misc, assignment]", "HttpxRequestKwargs = dict")
content = content.replace('self._client_kwargs.setdefault("timeout", 10.0)  # type: ignore[misc]', 'self._client_kwargs.setdefault("timeout", 10.0)')
content = content.replace('timeout = self._client_kwargs.pop("timeout", 10.0)  # type: ignore[misc]', 'timeout = self._client_kwargs.pop("timeout", 10.0)')
content = content.replace('self._client = httpx.AsyncClient(timeout=timeout, **self._client_kwargs)  # type: ignore[arg-type, misc]', 'self._client = httpx.AsyncClient(timeout=timeout, **self._client_kwargs)')

with open("src/taipanstack/bridges/http_bridge.py", "w") as f:
    f.write(content)
