import sys
def replace_in_file(filepath, old, new):
    with open(filepath, "r") as f: content = f.read()
    if old not in content:
        print(f"Error: Could not find target string in {filepath}")
        sys.exit(1)
    with open(filepath, "w") as f: f.write(content.replace(old, new))

# 1. guards.py url chars
old_guard_url = """def _has_invalid_url_chars(url: str) -> bool:
    if any(c <= "\\x20" or c == "\\x7f" for c in url):
        return True
    if "\\x00" in url or not url.isprintable():
        return True
    return False"""
new_guard_url = """def _has_invalid_url_chars(url: str) -> bool:
    if any(c <= "\\x20" or c == "\\x7f" for c in url):
        return True
    return bool("\\x00" in url or not url.isprintable())"""
replace_in_file("src/taipanstack/security/guards.py", old_guard_url, new_guard_url)

# 2. validators.py
old_val = """def _has_invalid_url_chars(url: str) -> bool:
    if any(c <= "\\x20" or c == "\\x7f" for c in url):
        return True
    if "\\x00" in url or not url.isprintable():
        return True
    return False"""
new_val = """def _has_invalid_url_chars(url: str) -> bool:
    if any(c <= "\\x20" or c == "\\x7f" for c in url):
        return True
    return bool("\\x00" in url or not url.isprintable())"""
replace_in_file("src/taipanstack/security/validators.py", old_val, new_val)

# 3. guards.py IP length issue 1
old_guard_ip1 = """def _is_ip_address_unsafe_bounds(addr: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:"""
new_guard_ip1 = """def _is_ip_address_unsafe_bounds(
    addr: ipaddress.IPv4Address | ipaddress.IPv6Address,
) -> bool:"""
replace_in_file("src/taipanstack/security/guards.py", old_guard_ip1, new_guard_ip1)

# 4. guards.py IP length issue 2
old_guard_ip2 = """    return not (getattr(addr, "is_multicast", False) or getattr(addr, "is_unspecified", False))"""
new_guard_ip2 = """    return not (
        getattr(addr, "is_multicast", False) or getattr(addr, "is_unspecified", False)
    )"""
replace_in_file("src/taipanstack/security/guards.py", old_guard_ip2, new_guard_ip2)
