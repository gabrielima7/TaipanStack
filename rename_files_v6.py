import os
import re

files_to_rename = []
for root, dirs, files in os.walk('tests'):
    for file in sorted(files):
        if file.startswith('test_') and file.endswith('.py') and '_operations' in file:
            filepath = os.path.join(root, file)

            # Simple rename: remove _operations.py
            new_name = file.replace('_operations.py', '.py')
            new_path = os.path.join(root, new_name)
            if filepath != new_path:
                files_to_rename.append((filepath, new_path))

for old, new in files_to_rename:
    os.rename(old, new)
