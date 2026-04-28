import time
from taipanstack.security.sanitizers import sanitize_sql_identifier
import string

massive_str = "!" * 5_000_000 + "A"
start = time.time()
try:
    res = sanitize_sql_identifier(massive_str)
    print("Length:", len(res))
except Exception as e:
    print("Error:", e)
end = time.time()
print(f"Time: {end - start:.4f}s")
