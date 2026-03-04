import re

with open('src/taipanstack/security/__init__.py', 'r') as f:
    content = f.read()

# Remove the specific guards that are not public API
content = re.sub(r'\s*SecurityError,\n', '\n', content)
content = re.sub(r'\s*guard_env_variable,\n', '\n', content)
content = re.sub(r'\s*guard_file_extension,\n', '\n', content)
content = re.sub(r'\s*guard_ssrf,\n', '\n', content)

# Remove from __all__
content = re.sub(r'\s*"SecurityError",\n', '\n', content)
content = re.sub(r'\s*"guard_env_variable",\n', '\n', content)
content = re.sub(r'\s*"guard_file_extension",\n', '\n', content)
content = re.sub(r'\s*"guard_ssrf",\n', '\n', content)

with open('src/taipanstack/security/__init__.py', 'w') as f:
    f.write(content)
