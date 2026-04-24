import re

with open("src/taipanstack/security/guards.py", "r") as f:
    content = f.read()

new_content = content

print("Length of content:", len(new_content))
