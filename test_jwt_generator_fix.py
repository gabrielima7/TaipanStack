from taipanstack.security.jwt import decode_jwt
import jwt
import sys

def gen_algos():
    yield "HS256"

def test_gen_algos():
    token = jwt.encode({"exp": 9999999999, "aud": "aud"}, "secret", algorithm="HS256")
    try:
        res = decode_jwt(token, "secret", algorithms=gen_algos(), audience="aud")
        print("Success!", res)
    except Exception as e:
        print("Failed!", type(e), e)

test_gen_algos()
