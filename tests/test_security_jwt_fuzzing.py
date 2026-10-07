from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.jwt import decode_jwt, encode_jwt


@given(st.text(min_size=2000, max_size=10000))
@settings(
    max_examples=50,
    suppress_health_check=[HealthCheck.data_too_large, HealthCheck.too_slow],
)
def test_jwt_encode_algorithm_length_fuzzing(alg):
    res = encode_jwt({"exp": 1}, "secret", algorithm=alg)
    assert res.is_err()
    err_str = str(res.err()).lower()
    assert "long" in err_str or "length" in err_str or "exceed" in err_str


@given(st.lists(st.text(min_size=2000, max_size=10000), min_size=1, max_size=5))
@settings(
    max_examples=50,
    suppress_health_check=[HealthCheck.data_too_large, HealthCheck.too_slow],
)
def test_jwt_decode_algorithms_length_fuzzing(algs):
    res = decode_jwt("token", "secret", algorithms=algs, audience="aud")
    assert res.is_err()
    err_str = str(res.err()).lower()
    assert "long" in err_str or "length" in err_str or "exceed" in err_str


@given(st.lists(st.text(min_size=2000, max_size=10000), min_size=1, max_size=5))
@settings(
    max_examples=50,
    suppress_health_check=[HealthCheck.data_too_large, HealthCheck.too_slow],
)
def test_jwt_decode_audience_list_length_fuzzing(auds):
    res = decode_jwt("token", "secret", algorithms=["HS256"], audience=auds)
    assert res.is_err()
    err_str = str(res.err()).lower()
    assert "long" in err_str or "length" in err_str or "exceed" in err_str
