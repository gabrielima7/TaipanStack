"""Property-based fuzzing tests for JWT secret in decode_jwt."""

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.jwt import decode_jwt

@given(
    secret=st.one_of(
        st.integers(),
        st.floats(),
        st.booleans(),
        st.none(),
        st.dictionaries(st.text(), st.text()),
        st.lists(st.text()),
    )
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
def test_fuzz_jwt_secret_decode_jwt_malformed_secret_standard_expected(
    secret,
) -> None:
    """Bombard decode_jwt with extreme, malformed secret types."""
    result = decode_jwt("token", secret, algorithms=["HS256"], audience="app")
    assert result.is_err()
    assert isinstance(result.err_value, TypeError)
    assert "Secret must be a string" in str(result.err_value)
