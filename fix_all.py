import os
import re

TEST_DIR = "tests"

# It looks like the earlier git restore brought back the original files AND kept the renamed ones.
# We should delete the files that do not end in `_expected.py` (except `__init__.py`).
for file in os.listdir(TEST_DIR):
    if file.startswith("test_") and file.endswith(".py"):
        if not file.endswith("_expected.py"):
            os.remove(os.path.join(TEST_DIR, file))
