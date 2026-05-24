"""Property-based fuzzing tests for JWT algorithms in decode_jwt."""

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.jwt import decode_jwt


@given(
    algorithms=st.one_of(
        st.integers(),
        st.floats(),
        st.booleans(),
        st.none(),
        st.dictionaries(st.text(), st.text()),
        st.text(),  # string is also invalid according to pyjwt, it expects a list
    )
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
def test_fuzz_jwt_algorithm_decode_jwt_malformed_algorithms(algorithms) -> None:
    """Bombard decode_jwt with extreme, malformed algorithm types."""
    result = decode_jwt("token", "secret", algorithms=algorithms, audience="app")
    assert result.is_err()
    assert isinstance(result.err_value, TypeError)
    assert "Algorithms must be a list" in str(result.err_value)
