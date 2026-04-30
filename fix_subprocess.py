def fix_subprocess():
    with open('src/taipanstack/utils/subprocess.py', 'r') as f:
        content = f.read()

    new_validate_timeout = """def _validate_timeout(timeout: float | None) -> None:
    \"\"\"Validate timeout value.\"\"\"
    if timeout is not None and not (math.isfinite(timeout) and timeout >= 0):
        raise ValueError("timeout must be a finite non-negative number")"""

    start_idx = content.find("def _validate_timeout(")
    end_idx = content.find("def _resolve_cwd(", start_idx)

    if start_idx == -1 or end_idx == -1:
        print("Could not find _validate_timeout method boundaries")
        return

    new_content = content[:start_idx] + new_validate_timeout + "\n\n" + content[end_idx:]

    with open('src/taipanstack/utils/subprocess.py', 'w') as f:
        f.write(new_content)

    print("Successfully fixed subprocess timeout type hint")

if __name__ == "__main__":
    fix_subprocess()
