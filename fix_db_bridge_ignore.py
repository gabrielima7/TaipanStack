import re

with open("src/taipanstack/bridges/db_bridge.py", "r") as f:
    content = f.read()

# Make the unfollowed import types explicit Any, or change no-any-unimported
# Wait, it might be easier to use `Any` from typing and use `type: ignore[no-any-unimported]`

def replace_ignore_misc(m):
    return m.group(1) + "  # type: ignore[misc, no-any-unimported]"

new_content = re.sub(r'(.*?)  # type: ignore\[misc\]', replace_ignore_misc, content)

with open("src/taipanstack/bridges/db_bridge.py", "w") as f:
    f.write(new_content)
