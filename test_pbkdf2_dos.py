import hashlib

try:
    hashlib.pbkdf2_hmac("sha256", b"test", b"salt", -10)
    print("No error")
except Exception as e:
    print(e)
