from taipanstack.security.jwt import decode_jwt

# What if `algorithms` is a generator?
def gen_algos():
    yield "HS256"

print(decode_jwt("token", "secret", gen_algos(), "aud"))
