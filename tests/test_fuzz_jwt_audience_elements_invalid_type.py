"""Property-based fuzzing tests for JWT audience element type in decode_jwt."""

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.jwt import decode_jwt


@given(
    audience=st.lists(
        st.one_of(st.integers(), st.floats(), st.booleans(), st.none()),
        min_size=1,
        max_size=10,
    )
)
@settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
def test_fuzz_jwt_audience_decode_jwt_invalid_type_elements(
    audience,
) -> None:
    """Bombard decode_jwt with iterables containing invalid type audience elements."""
    result = decode_jwt("token", "secret", algorithms=["HS256"], audience=audience)
    assert result.is_err()
    assert isinstance(result.err_value, TypeError)
    assert "Audience items must be strings" in str(result.err_value)
