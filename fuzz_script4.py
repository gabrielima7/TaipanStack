import string
from hypothesis import given, strategies as st
from taipanstack.security.jwt import encode_jwt, decode_jwt

@given(st.text())
def test_fuzz_jwt_algo(alg):
    try:
        encode_jwt({"test": "123"}, "secret", algorithm=alg)
    except (ValueError, TypeError, NotImplementedError, Exception):
        pass

if __name__ == "__main__":
    import pytest
    pytest.main(["-v", "fuzz_script4.py"])
