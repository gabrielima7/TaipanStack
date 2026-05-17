import string
from hypothesis import given, strategies as st
from taipanstack.security.jwt import encode_jwt, decode_jwt

@given(st.text(), st.text(), st.text())
def test_fuzz_jwt(payload_key, secret_key, alg):
    payload = {payload_key: "value"}
    try:
        encode_jwt(payload, secret_key, algorithm=alg)
    except Exception:
        pass

if __name__ == "__main__":
    import pytest
    pytest.main(["-v", "fuzz_script3.py"])
