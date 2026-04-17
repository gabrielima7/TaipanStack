import pathlib
p = pathlib.Path("src/taipanstack/security/sanitizers.py")
t = p.read_text()
t = t.replace("'", '"')
p.write_text(t)
