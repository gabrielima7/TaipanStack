import string
from hypothesis import given, strategies as st
from taipanstack.security.jwt import encode_jwt, decode_jwt

@given(st.text())
def test_fuzz_jwt_decode_algo(alg):
    try:
        decode_jwt("header.payload.signature", "secret", algorithms=[alg], audience="test")
    except (ValueError, TypeError, AttributeError, NotImplementedError, Exception):
        pass

if __name__ == "__main__":
    import pytest
    pytest.main(["-v", "fuzz_script5.py"])
