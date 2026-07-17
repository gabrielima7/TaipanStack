import re

with open("src/taipanstack/resilience/retry.py", "r") as f:
    content = f.read()

content = content.replace("last_exception: Exception | None = None", "last_exception: BaseException | None = None")

with open("src/taipanstack/resilience/retry.py", "w") as f:
    f.write(content)
