## 2024-06-11 - URL Smuggling Bypass via URL-Encoded Control Characters

**Vulnerability:** The URL validation guard (`_check_url_characters` in `src/taipanstack/security/validators.py`) previously failed to account for URL-encoded control characters (e.g., `%00` or `%20`). By injecting these characters, attackers could bypass the initial check, potentially leading to HTTP Request Smuggling or SSRF if downstream components unquoted the URL before processing.

**Learning:** Simply checking the raw URL string for ASCII control characters (`<= '\x20'` and `'\x7f'`) is insufficient because attackers can obfuscate these characters using URL encoding (`%XX`).

**Prevention:** Always validate both the raw URL string and its `unquote`d variant to ensure no control characters exist in either representation.
