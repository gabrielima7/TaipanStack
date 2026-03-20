import ast
import os

def find_defined_functions_and_classes(directory):
    defined = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    try:
                        tree = ast.parse(f.read())
                        for node in ast.walk(tree):
                            if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and not node.name.startswith('__'):
                                defined[node.name] = path
                    except Exception:
                        pass
    return defined

def find_used_names(directories):
    used = set()
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    path = os.path.join(root, file)
                    with open(path, 'r', encoding='utf-8') as f:
                        try:
                            tree = ast.parse(f.read())
                            for node in ast.walk(tree):
                                if isinstance(node, ast.Name):
                                    used.add(node.id)
                                elif isinstance(node, ast.Attribute):
                                    used.add(node.attr)
                        except Exception:
                            pass
    return used

defined = find_defined_functions_and_classes('src/taipanstack')
all_used = find_used_names(['src/taipanstack', 'tests'])

unused = {name: path for name, path in defined.items() if name not in all_used}

print("Potentially Unused functions/classes (including public ones not used in tests):")
for name, path in unused.items():
    print(f"{path}: {name}")
