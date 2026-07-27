import ast
import os
import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    try:
        tree = ast.parse(content)
    except SyntaxError:
        return False

    file_base = os.path.basename(filepath).replace('.py', '').replace('test_', '')
    if file_base.endswith('_standard_expected'):
        file_base = file_base[:-18]

    replacements = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
            # Check if name contains expected or raises or returns, etc.
            name_rest = node.name[5:]

            # If the rest doesn't start with the module name, prepend it
            if not name_rest.startswith(file_base):
                name_rest = f"{file_base}_{name_rest}"

            # Ensure it ends with an outcome descriptor if it doesn't already
            if not any(x in name_rest for x in ['expected', 'returns', 'raises', 'logged', 'error', 'fails', 'ok', 'success', 'dos']):
                name_rest = f"{name_rest}_expected"

            new_name = f"test_{name_rest}"

            if new_name != node.name:
                replacements.append((node.name, new_name))

    if replacements:
        for old_name, new_name in replacements:
            # Match the function definition directly to avoid messing with other usages
            content = re.sub(rf'def {old_name}\b', f'def {new_name}', content)

            # Also replace any direct calls to this test in the same file if they exist
            # But only whole words and not following def.
            content = re.sub(rf'(?<!def ){old_name}\b', new_name, content)

        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

if __name__ == '__main__':
    for root, dirs, files in os.walk('tests'):
        for file in files:
            if file.endswith('.py') and file.startswith('test_'):
                process_file(os.path.join(root, file))
