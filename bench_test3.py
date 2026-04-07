import time
import re

part = "some_directory-name.txt"

start = time.time()
for _ in range(100000):
    part.replace(".", "").replace("-", "").replace("_", "").isalnum()
print("replace:", time.time() - start)

pattern = re.compile(r"^[a-zA-Z0-9._-]+$")
start = time.time()
for _ in range(100000):
    bool(pattern.match(part))
print("regex:", time.time() - start)

def is_safe_part(part):
    return part.isascii() and all(c.isalnum() or c in "._-" for c in part)

start = time.time()
for _ in range(100000):
    is_safe_part(part)
print("all:", time.time() - start)
