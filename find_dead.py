import ast
import os

def check_for_dead_code(directory):
    # Dictionary to hold the definition filepath for each function/class name
    defined = {}

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    try:
                        tree = ast.parse(f.read())
                        for node in tree.body:
                            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                                name = node.name
                                # Skip main and __init__
                                if name not in ('main', '__init__', '__main__'):
                                    defined[name] = filepath
                    except SyntaxError:
                        pass

    # Now check if they are exported in __init__.py files
    exported = set()
    for root, _, files in os.walk(directory):
        for file in files:
            if file == '__init__.py':
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    try:
                        tree = ast.parse(content)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Assign):
                                for target in node.targets:
                                    if isinstance(target, ast.Name) and target.id == '__all__':
                                        if isinstance(node.value, (ast.List, ast.Tuple)):
                                            for elt in node.value.elts:
                                                if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                                                    exported.add(elt.value)
                    except SyntaxError:
                        pass

    # Now let's see which defined things are never called anywhere in src OR tests
    used = set()
    for d in ['src', 'tests']:
        for root, _, files in os.walk(d):
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        try:
                            tree = ast.parse(content)
                            for node in ast.walk(tree):
                                if isinstance(node, ast.Name):
                                    used.add(node.id)
                                elif isinstance(node, ast.Attribute):
                                    used.add(node.attr)
                        except SyntaxError:
                            pass

    for name, filepath in defined.items():
        if name not in used and name not in exported:
            print(f"Dead code found: {name} in {filepath}")

check_for_dead_code('src/taipanstack')
