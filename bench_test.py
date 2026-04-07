from result import Ok
from taipanstack.core.result import collect_results
import time

results = [Ok(i) for i in range(100)]
start = time.time()
for _ in range(1000):
    collect_results(results)
print("collect_results:", time.time() - start)

from taipanstack.security.guards import guard_ssrf
import socket
from unittest.mock import patch

public_ip = [(socket.AF_INET, socket.SOCK_STREAM, 0, "", ("93.184.216.34", 80))]
with patch("taipanstack.security.guards.socket.getaddrinfo", return_value=public_ip):
    start = time.time()
    for _ in range(1000):
        guard_ssrf("https://example.com")
print("guard_ssrf:", time.time() - start)
