from taipanstack.security.sanitizers import sanitize_path
import time

start = time.time()
for _ in range(100000):
    sanitize_path("safe/../../still/../ok/file.txt", max_depth=None)
print("sanitize_path traversal:", time.time() - start)

start = time.time()
for _ in range(100000):
    sanitize_path("a/b/c/d/e/f/g/h/file.txt", max_depth=10)
print("sanitize_path nested:", time.time() - start)
