import ast
import os
import re

def find_unused_stuff(directory):
    # This script will find any function or class starting with '_'
    # that is NOT referenced anywhere in the entire codebase.

    defined_internals = {} # name -> file path
    all_files = []

    # 1. Find all files
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                all_files.append(os.path.join(root, file))

    # 2. Find all internal definitions
    for path in all_files:
        with open(path, 'r', encoding='utf-8') as f:
            try:
                tree = ast.parse(f.read())
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        name = node.name
                        if name.startswith('_') and not name.startswith('__'):
                            defined_internals[name] = path
            except SyntaxError:
                pass

    # 3. Text search for usage of these internals in ALL files (including tests)
    all_codebase_files = []
    for search_dir in ['.']: # search everywhere
        for root, dirs, files in os.walk(search_dir):
            if '.venv' in dirs: dirs.remove('.venv')
            if '.git' in dirs: dirs.remove('.git')
            if '__pycache__' in dirs: dirs.remove('__pycache__')
            for file in files:
                if file.endswith('.py'):
                    all_codebase_files.append(os.path.join(root, file))

    used_names = set()
    for name in defined_internals:
        # Regex to find word boundaries
        pattern = re.compile(r'\b' + re.escape(name) + r'\b')
        for path in all_codebase_files:
            # Skip the file where it's defined (unless it calls itself, but we want to know if it's used elsewhere)
            # Actually, let's just see if it's used AT ALL outside of its definition line.
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Count occurrences
                matches = pattern.findall(content)
                if path == defined_internals[name]:
                    # Need at least 2 occurrences if used in same file (1 for def, 1+ for usage)
                    if len(matches) > 1:
                        used_names.add(name)
                        break
                else:
                    if len(matches) > 0:
                        used_names.add(name)
                        break

    unused = {name: path for name, path in defined_internals.items() if name not in used_names}
    return unused

unused_items = find_unused_stuff('src/taipanstack')
if unused_items:
    print("Found unused internals:")
    for name, path in unused_items.items():
        print(f"{path}: {name}")
else:
    print("No unused internals found.")
