import re

with open("src/taipanstack/core/result.py", "r") as f:
    content = f.read()

old_code = """    # Fast path: homogeneous exact types
    if type(first) is Ok:
        try:
            return Ok([r.ok_value for r in results])  # type: ignore
        except AttributeError:
            pass"""

new_code = """    # Fast path: homogeneous exact types
    if type(first) is Ok:
        try:
            return Ok([r.ok_value for r in results])  # type: ignore[union-attr,misc]
        except AttributeError:
            pass"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open("src/taipanstack/core/result.py", "w") as f:
        f.write(content)
    print("Patched successfully")
else:
    print("Could not find code to patch")
