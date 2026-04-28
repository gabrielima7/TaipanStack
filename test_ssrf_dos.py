from taipanstack.security.guards import guard_ssrf

# Test URL parsing edge cases
print(guard_ssrf("http://0177.0.0.1/"))
print(guard_ssrf("http://0x7f000001/"))
print(guard_ssrf("http://127.1/"))
print(guard_ssrf("http://[::1]/"))
print(guard_ssrf("http://localhost/"))
