from taipanstack.security.jwt import decode_jwt
import jwt

# Generate a JWT with a massive header to cause ReDoS or memory issues? No, pyjwt handles that usually.

# What about the audience parameter in decode_jwt?
# `audience: str | Iterable[str]`
# If I pass a generator to `audience`, does `pyjwt` evaluate it multiple times?
def gen_aud():
    yield "aud1"
    yield "aud2"

token = jwt.encode({"exp": 9999999999, "aud": "aud2"}, "secret", algorithm="HS256")
res = decode_jwt(token, "secret", ["HS256"], gen_aud())
print("Result with generator:", res)

# If it's exhausted, does it fail next time? Wait, pyjwt `decode` takes audience. If pyjwt iterates over it multiple times, it will fail if it's a generator. Let's see what pyjwt does internally.
