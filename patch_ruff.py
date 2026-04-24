import os

filepath = "src/taipanstack/security/models.py"
with open(filepath, "r") as f:
    content = f.read()

content = content.replace("ensure_ascii: bool = False,", "")

with open(filepath, "w") as f:
    f.write(content)
