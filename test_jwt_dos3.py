from taipanstack.security.jwt import decode_jwt

def gen_algos():
    yield "HS256"
    yield "HS384"

# algorithms generator gets exhausted in the `any(...)` check
try:
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.t-IDcSemACt8x4iTMCda8Yhe3iZaWbvV5XKSTbuAn0M"
    # We pass it to decode_jwt. The `any(secrets.compare_digest(...) for alg in algorithms)` exhausts the generator!
    print("Executing decode_jwt...")
    res = decode_jwt(token, "secret", gen_algos(), "aud")
    print(res)
except Exception as e:
    print(e)
