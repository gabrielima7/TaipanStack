from taipanstack.core.result import Err
from taipanstack.security.jwt import encode_jwt


def test_encode_jwt_weak_key():
    payload = {"sub": "123"}
    secret = "weak"
    # encode_jwt returns a Result because it is decorated with @safe_from
    result = encode_jwt(payload, secret, algorithm="HS256")
    assert isinstance(result, Err)
    assert isinstance(result.err_value, ValueError)
    assert "at least 32 bytes" in str(result.err_value)
