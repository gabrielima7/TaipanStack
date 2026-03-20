from vulture import Vulture
v = Vulture()
v.scavenge(['src/taipanstack/'])
for item in v.get_unused_code():
    print(f"{item.filename}:{item.first_lineno}: {item.typ} '{item.name}'")
