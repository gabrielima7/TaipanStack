import ast
import os

def check_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return

    # find all functions/classes defined at top level
    defined_public = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not node.name.startswith('_'):
                defined_public.add(node.name)

    if not defined_public:
        return

    # Check for __all__
    has_all = False
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == '__all__':
                    has_all = True
                    break

    used_elsewhere = set()
    for d in ['src', 'tests']:
        for root, _, files in os.walk(d):
            for file in files:
                if file.endswith('.py'):
                    p = os.path.join(root, file)
                    if p == filepath:
                        continue
                    with open(p, 'r', encoding='utf-8') as f:
                        try:
                            t = ast.parse(f.read())
                        except SyntaxError:
                            continue
                        for n in ast.walk(t):
                            if isinstance(n, ast.Name):
                                if n.id in defined_public:
                                    used_elsewhere.add(n.id)
                            elif isinstance(n, ast.Attribute):
                                if n.attr in defined_public:
                                    used_elsewhere.add(n.attr)

    unused = defined_public - used_elsewhere

    if unused:
        # Before claiming it's unused, maybe it's exposed in __init__.py?
        # Let's check __init__.py files in parent dirs
        module_name = filepath.replace('/', '.').replace('\\', '.').replace('.py', '')
        if module_name.startswith('src.'):
            module_name = module_name[4:]

        # very simple, we will just print them and manually verify
        print(f"Potentially Unused public in {filepath}: {unused}")


for root, _, files in os.walk('src/taipanstack'):
    for file in files:
        if file.endswith('.py'):
            path = os.path.join(root, file)
            check_file(path)
