import ast
import re
from pathlib import Path

target_funcs = {"safe_copy", "safe_delete", "get_file_hash", "find_files"}

for path in Path("tests").rglob("*.py"):
    with open(path) as f:
        source = f.read()

    # We will just parse the file and comment out the lines that are part of functions/classes using the target functions
    tree = ast.parse(source)
    ranges = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            uses_target = False
            if any(t in node.name for t in target_funcs):
                uses_target = True
            else:
                for child in ast.walk(node):
                    if isinstance(child, ast.Name) and child.id in target_funcs:
                        uses_target = True
                    elif isinstance(child, ast.ImportFrom):
                        if any(alias.name in target_funcs for alias in child.names):
                            uses_target = True
            if uses_target:
                ranges.append((node.lineno, node.end_lineno))

        elif isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    uses_target = False
                    if any(t in item.name for t in target_funcs):
                        uses_target = True
                    else:
                        for child in ast.walk(item):
                            if isinstance(child, ast.Name) and child.id in target_funcs:
                                uses_target = True
                            elif isinstance(child, ast.ImportFrom):
                                if any(alias.name in target_funcs for alias in child.names):
                                    uses_target = True
                    if uses_target:
                        ranges.append((item.lineno, item.end_lineno))

    if ranges:
        lines = source.splitlines()

        for i in range(len(lines)):
            line_no = i + 1
            if any(start <= line_no <= end for start, end in ranges):
                pass

            # fix imports globally
            # import line
            if "from taipanstack.utils.filesystem import" in lines[i]:
                # replace
                for t in target_funcs:
                    lines[i] = re.sub(rf"{t},?\s*", "", lines[i])

                lines[i] = re.sub(r"from taipanstack\.utils\.filesystem import\s*$", "", lines[i])


        lines_to_keep = []
        for i, line in enumerate(lines, 1):
            if not any(start <= i <= end for start, end in ranges):
                lines_to_keep.append(line)

        new_source = "\n".join(lines_to_keep) + "\n"
        with open(path, "w") as f:
            f.write(new_source)
