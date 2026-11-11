import os
import re

def process_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    new_content = re.sub(r'(.*?)  # type: ignore\[misc\]', r'\1  # type: ignore[misc, no-any-unimported, arg-type]', content)

    with open(filepath, "w") as f:
        f.write(new_content)

for root, _, files in os.walk("src/taipanstack"):
    for file in files:
        if file.endswith(".py"):
            process_file(os.path.join(root, file))
