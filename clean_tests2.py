import re
from pathlib import Path

target_funcs = {"safe_copy", "safe_delete", "get_file_hash", "find_files"}

for path in ["tests/test_filesystem_traversal_extended.py", "tests/test_utils_filesystem.py"]:
    with open(path) as f:
        source = f.read()

    lines = source.splitlines()
    for i in range(len(lines)):
        if "find_files," in lines[i]:
            lines[i] = ""
        if "get_file_hash," in lines[i]:
            lines[i] = ""
        if "safe_copy," in lines[i]:
            lines[i] = ""
        if "safe_delete," in lines[i]:
            lines[i] = ""

    new_source = "\n".join(lines) + "\n"
    with open(path, "w") as f:
        f.write(new_source)
