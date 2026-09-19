from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.jwt import decode_jwt, encode_jwt


@given(
    token=st.one_of(
        st.integers(),
        st.floats(),
        st.lists(st.integers()),
        st.dictionaries(st.text(), st.text()),
    )
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
def test_fuzz_jwt_decode_token_type_expected(token):
    res = decode_jwt(token, "secret", ["HS256"], "app")
    assert res.is_err()
    assert isinstance(res.err_value, TypeError)


@given(
    payload=st.one_of(st.integers(), st.floats(), st.lists(st.integers()), st.text())
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
def test_fuzz_jwt_encode_payload_type_expected(payload):
    res = encode_jwt(payload, "secret", "HS256")
    assert res.is_err()
    assert isinstance(res.err_value, TypeError)
