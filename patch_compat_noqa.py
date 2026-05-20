with open("src/taipanstack/core/compat.py", "r") as f:
    content = f.read()

content = content.replace('        import sysconfig\n', '        import sysconfig  # noqa: PLC0415\n')

with open("src/taipanstack/core/compat.py", "w") as f:
    f.write(content)
