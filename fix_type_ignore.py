import os
import re
import subprocess

def process_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    # Find all type: ignore[misc] occurrences
    new_content = content.replace("  # type: ignore[misc]", "")
    new_content = new_content.replace("  # type: ignore[unreachable]", "")

    with open(filepath, "w") as f:
        f.write(new_content)

for root, _, files in os.walk("src/taipanstack"):
    for file in files:
        if file.endswith(".py"):
            process_file(os.path.join(root, file))
