import ast
import os
import sys

def find_defined_internals(directory):
    internals = set()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    try:
                        tree = ast.parse(f.read())
                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef) and node.name.startswith('_') and not node.name.startswith('__'):
                                internals.add(node.name)
                            elif isinstance(node, ast.ClassDef) and node.name.startswith('_') and not node.name.startswith('__'):
                                internals.add(node.name)
                    except Exception as e:
                        print(f"Error parsing {path}: {e}")
    return internals

def find_used_internals(directory):
    used = set()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    try:
                        tree = ast.parse(f.read())
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Name) and node.id.startswith('_') and not node.id.startswith('__'):
                                used.add(node.id)
                            elif isinstance(node, ast.Attribute) and node.attr.startswith('_') and not node.attr.startswith('__'):
                                used.add(node.attr)
                    except Exception as e:
                        pass
    return used

defined = find_defined_internals('src/taipanstack')
used_in_src = find_used_internals('src/taipanstack')
used_in_tests = find_used_internals('tests')

all_used = used_in_src | used_in_tests

unused = defined - all_used

print("Unused internal functions/classes:")
for item in sorted(unused):
    print(item)
