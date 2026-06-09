from taipanstack.security.guards import guard_ssrf

print(guard_ssrf("http://exa\x20mple.com"))
print(guard_ssrf("http://example.com/\x7f"))
