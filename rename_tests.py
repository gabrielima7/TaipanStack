import os
import re

TEST_DIR = "tests"

def rename_file_and_functions(filepath):
    # Rename test functions inside the file
    with open(filepath, "r") as f:
        content = f.read()

    # Extract module name from file name
    filename = os.path.basename(filepath)
    module_name = filename.replace('test_', '').replace('.py', '')

    new_content = []
    for line in content.split('\n'):
        match = re.match(r'^(\s*)def (test_[a-zA-Z0-9_]+)\((.*)$', line)
        if match:
            indent = match.group(1)
            func_name = match.group(2)
            rest = match.group(3)

            base_name = func_name[5:]
            if base_name.endswith('_expected') or base_name.endswith('_returns_err'):
                pass

            new_func_name = f"test_{module_name}_{base_name}_expected"
            new_func_name = new_func_name.replace(f"{module_name}_{module_name}", f"{module_name}")

            new_content.append(f"{indent}def {new_func_name}({rest}")
        else:
            new_content.append(line)

    with open(filepath, "w") as f:
        f.write('\n'.join(new_content))

    new_filename = f"test_{module_name}_operations_expected.py"
    new_filepath = os.path.join(os.path.dirname(filepath), new_filename)

    if filepath != new_filepath:
        os.rename(filepath, new_filepath)

for root, _, files in os.walk(TEST_DIR):
    for file in files:
        if file.startswith("test_") and file.endswith(".py") and not file.endswith("_expected.py"):
            rename_file_and_functions(os.path.join(root, file))
