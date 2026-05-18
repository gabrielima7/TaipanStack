import ast
import os
import glob

def find_bad_names():
    for f_name in glob.glob("tests/**/test_*.py", recursive=True):
        with open(f_name, "r") as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                parts = node.name.split("_")
                if len(parts) < 4:
                    print(f"Bad name: {node.name} in {f_name}")

find_bad_names()
