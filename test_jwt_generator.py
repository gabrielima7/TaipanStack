from taipanstack.security.jwt import decode_jwt
import jwt

def gen_algos():
    yield "HS256"

# Encode
token = jwt.encode({"exp": 9999999999, "aud": "my-aud"}, "secret", algorithm="HS256")

# Decode using a generator for algorithms.
# The code:
# if any(secrets.compare_digest(str(alg).strip().lower(), "none") for alg in algorithms):
#     raise ValueError(...)
# return jwt.decode(token, secret_key, algorithms=algorithms, ...)

# Since `any` will iterate over the generator to check for "none", by the time it reaches `jwt.decode`, `algorithms` is exhausted!
res = decode_jwt(token, "secret", algorithms=gen_algos(), audience="my-aud")
print("Algorithms as generator:", res)

# Same for audience if it is an Iterable. Wait, the code doesn't iterate over audience, it just passes it to `jwt.decode`. `pyjwt` might iterate over it or expect it to be a list. Let's test that too.
def gen_aud():
    yield "my-aud"

res2 = decode_jwt(token, "secret", algorithms=["HS256"], audience=gen_aud())
print("Audience as generator:", res2)
