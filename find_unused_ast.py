import ast
import os
import re

def find_unused_in_file(filepath):
    """Find internal classes and functions not used ANYWHERE."""
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()

    tree = ast.parse(source)

    defined = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name.startswith('_') and not node.name.startswith('__'):
                defined.add(node.name)

    used_elsewhere = set()

    # Check entire src and tests for usage
    for d in ['src', 'tests']:
        for root, _, files in os.walk(d):
            for file in files:
                if file.endswith('.py'):
                    p = os.path.join(root, file)
                    with open(p, 'r', encoding='utf-8') as f:
                        content = f.read()

                    for name in defined:
                        # use regex word boundary to find exact usage
                        matches = len(re.findall(r'\b' + re.escape(name) + r'\b', content))
                        # definition in this file counts as 1. If matches > 1 in this file it's used
                        if p == filepath:
                             if matches > 1:
                                  used_elsewhere.add(name)
                        else:
                             if matches > 0:
                                  used_elsewhere.add(name)

    unused = defined - used_elsewhere
    if unused:
         print(f"{filepath}: {unused}")

for root, _, files in os.walk('src/taipanstack'):
    for file in files:
        if file.endswith('.py'):
            path = os.path.join(root, file)
            find_unused_in_file(path)
