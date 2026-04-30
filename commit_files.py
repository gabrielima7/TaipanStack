import subprocess
import os

files_to_commit = [
    "tests/test_config_generators_operations_expected.py",
    "tests/test_config_models_operations_expected.py",
    "tests/test_result_module_operations_expected.py"
]

for file in files_to_commit:
    subprocess.run(["git", "add", file])

subprocess.run(["git", "commit", "-m", "fix: address linting and code quality failures on test files"])
