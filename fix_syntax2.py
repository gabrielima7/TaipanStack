with open("src/taipanstack/security/sanitizers.py", "r") as f:
    lines = f.readlines()

out = []
for line in lines:
    out.append(line.replace(r'\\x00', r'\x00').replace(r'\\n', r'\n').replace(r'\\r', r'\r').replace(r'\\x', r'\x'))

with open("src/taipanstack/security/sanitizers.py", "w") as f:
    f.writelines(out)
