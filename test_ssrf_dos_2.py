from taipanstack.security.guards import guard_ssrf

url = "http://127.0.0.1/"
print(guard_ssrf(url))

url2 = "http://0.0.0.0/"
print(guard_ssrf(url2))

url3 = "http://[::]/"
print(guard_ssrf(url3))
