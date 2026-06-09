from taipanstack.security.guards import guard_ssrf

print(guard_ssrf("http://example.com"))
print(guard_ssrf("http://127.0.0.1"))
