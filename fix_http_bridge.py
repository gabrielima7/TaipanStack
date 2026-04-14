import re

file_path = "src/taipanstack/bridges/http_bridge.py"
with open(file_path, "r") as f:
    content = f.read()

content = content.replace("class RequestKwargs(typing.TypedDict, total=False):", 'class RequestKwargs(typing.TypedDict, total=False):\n        """Type hints for HTTP request keyword arguments."""')
content = content.replace("class ClientKwargs(typing.TypedDict, total=False):", 'class ClientKwargs(typing.TypedDict, total=False):\n        """Type hints for HTTP client keyword arguments."""')

with open(file_path, "w") as f:
    f.write(content)
