import re

with open('src/taipanstack/security/guards.py', 'r') as f:
    content = f.read()

# Fix PLR0911 by ignoring it or refactoring (returning Ok(url) via single point or using # noqa)
content = content.replace("def guard_ssrf(", "def guard_ssrf(  # noqa: PLR0911")

with open('src/taipanstack/security/guards.py', 'w') as f:
    f.write(content)

with open('src/taipanstack/security/sanitizers.py', 'r') as f:
    content = f.read()

# Fix SIM102
content = content.replace("""    # Handle HTML
    if not allow_html:
        if "<" in result or ">" in result or "&" in result:""", """    # Handle HTML
    if not allow_html and ("<" in result or ">" in result or "&" in result):""")

with open('src/taipanstack/security/sanitizers.py', 'w') as f:
    f.write(content)
