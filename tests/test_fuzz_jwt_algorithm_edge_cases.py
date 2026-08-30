from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.jwt import decode_jwt


@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
@given(
    algorithms=st.lists(
        st.one_of(
            st.integers(),
            st.floats(),
            st.booleans(),
            st.none(),
            st.dictionaries(st.text(), st.text()),
            st.lists(st.text()),
        ),
        min_size=1,
    )
)
def test_fuzz_jwt_algorithm_decode_jwt_malformed_algorithms_in_list(algorithms) -> None:
    """Bombard decode_jwt with list of extreme, malformed algorithm types."""
    result = decode_jwt("token", "secret", algorithms=algorithms, audience="app")
    assert result.is_err()
    assert isinstance(result.err_value, TypeError)
    assert "Algorithm must be a string" in str(result.err_value)
