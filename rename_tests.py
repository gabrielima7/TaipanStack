import ast
import os

def rename_functions_in_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    tree = ast.parse(content)

    replacements = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
            parts = node.name.split('_')
            if len(parts) < 4:
                # Need to rename this function.
                # Let's derive module, behavior, expected from the filename and old name.
                filename = os.path.basename(filepath)
                # Assume filename is test_<module>_<something>
                file_parts = filename[:-3].split('_')
                if len(file_parts) >= 2:
                    module = file_parts[1]
                else:
                    module = "unknown"

                behavior = "_".join(parts[1:])
                if not behavior:
                    behavior = "behavior"

                expected = "expected"

                new_name = f"test_{module}_{behavior}_{expected}"
                replacements.append((node.name, new_name))

    if replacements:
        for old, new in replacements:
            content = content.replace(f"def {old}(", f"def {new}(")
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Renamed in {filepath}: {replacements}")

for root, _, files in os.walk('tests'):
    for file in files:
        if file.endswith('.py') and file != '__init__.py':
            filepath = os.path.join(root, file)
            rename_functions_in_file(filepath)
