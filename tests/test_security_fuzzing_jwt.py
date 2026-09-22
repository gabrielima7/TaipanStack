import hypothesis.strategies as st
from hypothesis import given, settings

from taipanstack.security.jwt import decode_jwt, encode_jwt


@settings(max_examples=100)
@given(st.dictionaries(st.text(), st.text()), st.text(), st.text())
def test_fuzz_jwt_encode(payload, secret, alg):
    result = encode_jwt(payload, secret, algorithm=alg)
    if result.is_err():
        assert isinstance(result.err_value, (ValueError, TypeError, Exception))
    else:
        assert isinstance(result.unwrap(), str)


@settings(max_examples=100)
@given(st.text(), st.text(), st.lists(st.text()), st.text())
def test_fuzz_jwt_decode(token, secret, algs, aud):
    result = decode_jwt(token, secret, algorithms=algs, audience=aud)
    if result.is_err():
        pass
    else:
        assert isinstance(result.unwrap(), dict)
