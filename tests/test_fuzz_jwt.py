"""Property-based fuzzing tests for the secure JWT module."""

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.jwt import decode_jwt, encode_jwt

# Strategy for completely malformed, extreme payload types
malformed_payload_strategy = st.one_of(
    st.integers(),
    st.floats(),
    st.booleans(),
    st.none(),
    st.lists(st.text()),
    st.text(),
)

# Strategy for malformed secrets (not strings)
malformed_secret_strategy = st.one_of(
    st.integers(),
    st.floats(),
    st.booleans(),
    st.none(),
    st.lists(st.text()),
)


class TestFuzzJWT:
    """Fuzz testing for JWT encoding and decoding."""

    @given(
        payload=malformed_payload_strategy,
        secret=st.text(min_size=1, max_size=100),
        algorithm=st.sampled_from(["HS256", "HS384", "HS512"]),
    )
    @settings(max_examples=500, suppress_health_check=[HealthCheck.too_slow])
    def test_fuzz_encode_jwt_malformed_payload(
        self, payload, secret, algorithm
    ) -> None:
        """Bombard encode_jwt with extreme, malformed payload types."""
        result = encode_jwt(payload, secret, algorithm=algorithm)
        # Should cleanly return an Err result, not raise an unhandled TypeError
        assert result.is_err(), "Expected malformed payload to result in an Error"

    @given(
        token=malformed_payload_strategy,
        secret=st.text(min_size=1, max_size=100),
        algorithms=st.lists(st.sampled_from(["HS256", "HS384", "HS512"]), min_size=1),
        audience=st.one_of(st.text(), st.lists(st.text())),
    )
    @settings(max_examples=500, suppress_health_check=[HealthCheck.too_slow])
    def test_fuzz_decode_jwt_malformed_token(
        self, token, secret, algorithms, audience
    ) -> None:
        """Bombard decode_jwt with extreme, malformed token types."""
        result = decode_jwt(token, secret, algorithms=algorithms, audience=audience)
        # Should cleanly return an Err result, not raise an unhandled TypeError or AttributeError
        assert result.is_err(), "Expected malformed token to result in an Error"

    @given(
        payload=st.dictionaries(st.text(), st.text()),
        secret=malformed_secret_strategy,
        algorithm=st.sampled_from(["HS256"]),
    )
    @settings(max_examples=500, suppress_health_check=[HealthCheck.too_slow])
    def test_fuzz_encode_jwt_malformed_secret(self, payload, secret, algorithm) -> None:
        """Bombard encode_jwt with extreme, malformed secret types."""
        result = encode_jwt(payload, secret, algorithm=algorithm)
        assert result.is_err(), "Expected malformed secret to result in an Error"
