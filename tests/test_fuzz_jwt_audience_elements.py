"""Property-based fuzzing tests for JWT audience elements in decode_jwt."""

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.jwt import decode_jwt


@given(
    audience=st.lists(st.text(min_size=1025, max_size=2000), min_size=1, max_size=10)
)
@settings(
    max_examples=50,
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.data_too_large],
)
def test_fuzz_jwt_audience_decode_jwt_massive_elements(
    audience,
) -> None:
    """Bombard decode_jwt with iterables containing massively long audience strings."""
    result = decode_jwt("token", "secret", algorithms=["HS256"], audience=audience)
    assert result.is_err()
    assert isinstance(result.err_value, ValueError)
    assert "Audience string is too long" in str(result.err_value)
