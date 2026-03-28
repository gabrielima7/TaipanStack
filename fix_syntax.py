import re

with open("src/taipanstack/security/sanitizers.py", "r") as f:
    content = f.read()

# Replace bare "\n" inside docstrings or any code logic that may have accidentally dropped raw strings if it got un-escaped.
# We don't want to blindly do it, let's fix the invalid escape sequence
# Wait, the error is \x00 in docstrings or normal strings when unescaped incorrectly.
content = content.replace('\\x00', r'\x00')

with open("src/taipanstack/security/sanitizers.py", "w") as f:
    f.write(content)
