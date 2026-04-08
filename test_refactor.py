import os
import subprocess

def run_radon():
    result = subprocess.run(["poetry", "run", "radon", "cc", "src/taipanstack/security/sanitizers.py", "-s", "-a"], capture_output=True, text=True)
    print(result.stdout)

run_radon()
