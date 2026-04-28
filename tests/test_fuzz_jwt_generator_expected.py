import pytest
import jwt
from hypothesis import given, settings, HealthCheck, strategies as st
from taipanstack.security.jwt import decode_jwt, PyJWTError

def test_decode_jwt_generator_algorithms():
    def gen_algos():
        yield "HS256"

    token = jwt.encode({"exp": 9999999999, "aud": "my-aud"}, "secret", algorithm="HS256")

    # It should succeed, not fail due to algorithm exhaustion
    res = decode_jwt(token, "secret", algorithms=gen_algos(), audience="my-aud")
    assert res.is_ok()
