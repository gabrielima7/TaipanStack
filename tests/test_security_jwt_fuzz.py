import jwt
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.jwt import decode_jwt, encode_jwt


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

@settings(max_examples=100, suppress_health_check=[HealthCheck.filter_too_much])
@given(
    st.dictionaries(st.text(), st.text() | st.integers() | st.floats() | st.booleans()),
    st.text(min_size=32),
)
def test_fuzz_jwt_encode_decode_payloads(payload: dict[str, object], secret: str) -> None:
    """Fuzz encode_jwt and decode_jwt with random payloads and secrets."""
    # Ensure payload contains expected claims to pass standard decoding
    payload["sub"] = "test"
    payload["aud"] = "aud"

    # Test encoding
    encode_result = encode_jwt(payload, secret)
    assert encode_result.is_err() or encode_result.is_ok(), "Should return Result monad"

    if encode_result.is_ok():
        token = str(encode_result.unwrap())
        decode_result = decode_jwt(token, secret, algorithms=["HS256"], audience="aud")
        assert decode_result.is_err() or decode_result.is_ok(), "Should return Result monad"

@settings(max_examples=100, suppress_health_check=[HealthCheck.filter_too_much])
@given(
    st.text(),
    st.text(min_size=32),
    st.text(),
    st.text(),
)
def test_fuzz_jwt_decode_malformed_token(token: str, secret: str, alg: str, aud: str) -> None:
    """Fuzz decode_jwt with malformed tokens."""
    decode_result = decode_jwt(token, secret, algorithms=[alg], audience=aud)
    assert decode_result.is_err() or decode_result.is_ok(), "Should return Result monad"
    if decode_result.is_err():
        assert isinstance(decode_result.err_value, (ValueError, TypeError, jwt.exceptions.PyJWTError, NotImplementedError, KeyError, AttributeError))
