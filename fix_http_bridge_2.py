with open("src/taipanstack/bridges/http_bridge.py", "r") as f:
    content = f.read()

content = content.replace("Any # type: ignore[misc]", "Any")

with open("src/taipanstack/bridges/http_bridge.py", "w") as f:
    f.write(content)
