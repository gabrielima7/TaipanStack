import pathlib

p = pathlib.Path("src/taipanstack/security/sanitizers.py")
lines = p.read_text().splitlines()
out = []
skip = False
added_helpers = False
in_sanitize_string = False

for line in lines:
    if "def sanitize_string(" in line:
        in_sanitize_string = True
        if not added_helpers:
            out.append("def _validate_sanitize_string_input(value: str) -> str:")
            out.append("    if not isinstance(value, str):")
            out.append("        raise TypeError(f\"value must be str, got {type(value).__name__}\")")
            out.append("    return value")
            out.append("")
            out.append("")
            added_helpers = True

    if "    if not isinstance(value, str):" in line and in_sanitize_string:
        skip = True
        out.append("    result = _validate_sanitize_string_input(value)")
        out.append("    if not result:")
        out.append("        return \"\"")
        continue

    if skip and "    if not value:" in line and in_sanitize_string:
        continue

    if skip and "        return \"\"" in line and in_sanitize_string:
        continue

    if skip and "    result = value" in line and in_sanitize_string:
        skip = False
        in_sanitize_string = False
        continue

    if not skip:
        out.append(line)

p.write_text("\n".join(out) + "\n")
