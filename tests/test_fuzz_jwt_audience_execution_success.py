"""Property-based fuzzing tests for JWT audience in decode_jwt."""

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.jwt import decode_jwt


@given(
    audience=st.one_of(
        st.integers(),
        st.floats(),
        st.booleans(),
        st.none(),
        st.dictionaries(st.text(), st.text()),
    )
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
def test_fuzz_jwt_audience_decode_jwt_malformed_audience_execution_success(
    audience,
) -> None:
    """Bombard decode_jwt with extreme, malformed audience types."""
    result = decode_jwt("token", "secret", algorithms=["HS256"], audience=audience)
    assert result.is_err()
    assert isinstance(result.err_value, TypeError)
    assert "Audience must be a string or iterable of strings" in str(result.err_value)
