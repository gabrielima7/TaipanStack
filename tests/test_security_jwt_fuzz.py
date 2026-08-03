import pytest
from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st

from taipanstack.security.jwt import encode_jwt, decode_jwt
import jwt

@settings(max_examples=100, suppress_health_check=[HealthCheck.filter_too_much])
@given(
    st.text()
)
def test_fuzz_jwt_algorithms(alg: str) -> None:
    """Fuzz encode_jwt and decode_jwt with random algorithm strings.
    Validates that non-ascii strings or massive strings do not crash via compare_digest.
    """
    secret = "super_secret_key_that_is_at_least_32_bytes_long"
    payload = {"sub": "test", "aud": "aud"}

    # Test encoding
    encode_result = encode_jwt(payload, secret, algorithm=alg)
    assert encode_result.is_err() or encode_result.is_ok(), "Should return Result monad"

    # Test decoding
    try:
        token = jwt.encode(payload, secret, algorithm="HS256")
    except Exception:
        token = "invalid.token"

    decode_result = decode_jwt(token, secret, algorithms=[alg], audience="aud")
    assert decode_result.is_err() or decode_result.is_ok(), "Should return Result monad"
