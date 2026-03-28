import re
from pathlib import Path

def add_wildcard(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    # Search for match result:
    # and then find the last case
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if "match result:" in line or "match validation:" in line or "match hash_result:" in line or "match load_result:" in line or "match guard_ssrf" in line or "match _validate_ssrf_url" in line or "match _check_ip_safety" in line or "match changes:" in line:
            # We want to insert `case _:` block if there isn't one.
            pass
