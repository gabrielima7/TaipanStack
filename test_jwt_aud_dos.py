import jwt
from taipanstack.security.jwt import decode_jwt

def gen_aud():
    yield "aud1"

token = jwt.encode({"exp": 9999999999, "aud": "aud1"}, "secret", algorithm="HS256")
res = decode_jwt(token, "secret", ["HS256"], gen_aud())
print(res)
