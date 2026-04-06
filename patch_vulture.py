import re

with open('src/taipanstack/security/guards.py', 'r') as f:
    content = f.read()

content = re.sub(r'def _validate_ssrf_url\([\s\S]*?return Ok\(hostname\)\n\n\n', '', content)
content = re.sub(r'def _check_ip_safety\([\s\S]*?return Ok\(None\)\n\n\n', '', content)

with open('src/taipanstack/security/guards.py', 'w') as f:
    f.write(content)
