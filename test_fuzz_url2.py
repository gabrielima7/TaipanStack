from urllib.parse import urlparse

url = "http://user:pass@example.com"
parsed = urlparse(url)
print(f"hostname: {parsed.hostname}")

url2 = "http://example.com:80"
parsed2 = urlparse(url2)
print(f"hostname: {parsed2.hostname}")
