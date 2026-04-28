import time
from taipanstack.security.sanitizers import sanitize_env_value

massive = "A" * 50_000_000
start = time.time()
sanitize_env_value(massive)
end = time.time()
print(f"Time taken: {end - start:.4f}s")
