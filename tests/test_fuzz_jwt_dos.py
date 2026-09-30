from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.jwt import decode_jwt


@settings(
    max_examples=10,
    suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.large_base_example,
        HealthCheck.data_too_large,
    ],
)
@given(
    algorithms=st.lists(st.text(min_size=1, max_size=10), min_size=11, max_size=1000)
)
def test_fuzz_jwt_decode_algorithms_dos(algorithms: list[str]) -> None:
    """Fuzz decode_jwt with massive lists of algorithms to ensure DoS protection limits are active."""
    res = decode_jwt(
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.e30.signature",
        "secret",
        algorithms,
        "aud",
    )
    assert res.is_err()
    assert "Too many algorithms provided" in str(res.unwrap_err())


@settings(
    max_examples=10,
    suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.large_base_example,
        HealthCheck.data_too_large,
    ],
)
@given(audience=st.lists(st.text(min_size=1, max_size=10), min_size=11, max_size=1000))
def test_fuzz_jwt_decode_audience_list_dos(audience: list[str]) -> None:
    """Fuzz decode_jwt with massive lists of audiences to ensure DoS protection limits are active."""
    res = decode_jwt(
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.e30.signature",
        "secret",
        ["HS256"],
        audience,
    )
    assert res.is_err()
    assert "Too many audience items provided" in str(res.unwrap_err())


@settings(
    max_examples=10,
    suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.large_base_example,
        HealthCheck.data_too_large,
    ],
)
@given(audience=st.text(min_size=1025, max_size=5000))
def test_fuzz_jwt_decode_audience_string_dos(audience: str) -> None:
    """Fuzz decode_jwt with massive strings for audience to ensure DoS protection limits are active."""
    res = decode_jwt(
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.e30.signature",
        "secret",
        ["HS256"],
        audience,
    )
    assert res.is_err()
    assert "Audience string is too long" in str(res.unwrap_err())
