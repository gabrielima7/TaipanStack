import ast

with open('src/taipanstack/security/__init__.py', 'r') as f:
    tree = ast.parse(f.read())

imports = []
all_list = []

for node in tree.body:
    if isinstance(node, ast.ImportFrom):
        for alias in node.names:
            imports.append(alias.name)
    elif isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == '__all__':
                if isinstance(node.value, ast.List):
                    for elt in node.value.elts:
                        if isinstance(elt, ast.Constant):
                            all_list.append(elt.value)

print("Imports:", imports)
print("__all__:", all_list)

unused = set(imports) - set(all_list)
print("Unused:", unused)

not_imported = set(all_list) - set(imports)
print("Not imported:", not_imported)
