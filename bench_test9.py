from taipanstack.security.sanitizers import sanitize_string
import time

payload = "Héllo Wörld こんにちは 🌍 café résumé naïve" * 5

start = time.time()
for _ in range(10000):
    sanitize_string(payload)
print("sanitize_string unicode:", time.time() - start)

payload = "<script>alert('xss')</script><img onerror=alert(1) src=x>"

start = time.time()
for _ in range(10000):
    sanitize_string(payload)
print("sanitize_string xss:", time.time() - start)
