import re

with open("src/taipanstack/security/sanitizers.py") as f:
    data = f.read()

SEARCH = """
    # Remove path separators that might have snuck through
    safe_stem = safe_stem.replace("/", replacement)
    safe_stem = safe_stem.replace("\\\\", replacement)

    # Collapse multiple replacement chars
    if replacement:
        double_replacement = replacement + replacement
        while double_replacement in safe_stem:
            safe_stem = safe_stem.replace(double_replacement, replacement)
        safe_stem = safe_stem.strip(replacement)
    else:  # pragma: no cover
        # If replacement is empty (""), this branch is hit, but safe_stem may still have leading/trailing dots/spaces
        pass
"""

REPLACE = """
    # Remove path separators that might have snuck through
    safe_stem = safe_stem.replace("/", replacement)
    safe_stem = safe_stem.replace("\\\\", replacement)

    # Collapse multiple replacement chars
    if replacement:
        double_replacement = replacement + replacement
        while double_replacement in safe_stem:
            safe_stem = safe_stem.replace(double_replacement, replacement)
        safe_stem = safe_stem.strip(replacement)
"""

if SEARCH[1:] in data:
    data = data.replace(SEARCH[1:], REPLACE[1:])

with open("src/taipanstack/security/sanitizers.py", "w") as f:
    f.write(data)
