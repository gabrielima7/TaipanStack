"""Property-based fuzzing tests for the secure JWT module."""

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.jwt import decode_jwt, encode_jwt

# Strategy for completely malformed, extreme payload types
malformed_payload_strategy = st.recursive(
    st.one_of(
        st.integers(),
        st.floats(allow_nan=True, allow_infinity=True),
        st.booleans(),
        st.none(),
        st.text(),
        st.binary(),
        st.datetimes(),
        st.complex_numbers(),
    ),
    lambda children: st.one_of(
        st.lists(children, max_size=10),
        st.dictionaries(st.text(), children, max_size=10),
    ),
    max_leaves=15,
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
        payload=st.one_of(
            st.integers(),
            st.floats(),
            st.booleans(),
            st.none(),
            st.lists(st.text()),
            st.text(),
        ),
        secret=st.text(min_size=1, max_size=100),
        algorithm=st.sampled_from(["HS256", "HS384", "HS512"]),
    )
    @settings(max_examples=500, suppress_health_check=[HealthCheck.too_slow])
    def test_fuzz_jwt_fuzz_encode_jwt_malformed_payload(
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
    def test_fuzz_jwt_fuzz_decode_jwt_malformed_token(
        self, token, secret, algorithms, audience
    ) -> None:
        """Bombard decode_jwt with extreme, malformed token types."""
        result = decode_jwt(token, secret, algorithms=algorithms, audience=audience)
        # Should cleanly return an Err result, not raise an unhandled TypeError or AttributeError
        assert result.is_err(), "Expected malformed token to result in an Error"

    @given(
        token=st.text(min_size=10),
        secret=malformed_secret_strategy,
        algorithms=st.lists(st.sampled_from(["HS256", "HS384", "HS512"]), min_size=1),
        audience=st.one_of(st.text(), st.lists(st.text())),
    )
    @settings(max_examples=500, suppress_health_check=[HealthCheck.too_slow])
    def test_fuzz_jwt_fuzz_decode_jwt_malformed_secret(
        self, token, secret, algorithms, audience
    ) -> None:
        """Bombard decode_jwt with extreme, malformed secret types."""
        result = decode_jwt(token, secret, algorithms=algorithms, audience=audience)
        assert result.is_err(), "Expected malformed secret to result in an Error"

    @given(
        token=st.text(min_size=10),
        secret=st.text(min_size=1, max_size=100),
        algorithms=malformed_payload_strategy,
        audience=st.one_of(st.text(), st.lists(st.text())),
    )
    @settings(max_examples=500, suppress_health_check=[HealthCheck.too_slow])
    def test_fuzz_jwt_fuzz_decode_jwt_malformed_algorithms(
        self, token, secret, algorithms, audience
    ) -> None:
        """Bombard decode_jwt with extreme, malformed algorithms types."""
        result = decode_jwt(token, secret, algorithms=algorithms, audience=audience)
        assert result.is_err(), "Expected malformed algorithms to result in an Error"

    def test_fuzz_jwt_fuzz_decode_jwt_algorithms_compare_typeerror(self) -> None:
        """Test decode_jwt handles compare_digest type error securely."""

        # A list that passes the initial typecheck but causes TypeError in compare_digest if it isn't properly strings
        class BadStr(str):
            def strip(self):
                return self

            def lower(self):
                raise TypeError("Mocked type error")

        result = decode_jwt("some.token", "secret", [BadStr("HS256")], "audience")
        assert result.is_err()
        assert isinstance(result.err_value, TypeError)

    @given(
        token=st.text(min_size=10),
        secret=st.text(min_size=1, max_size=100),
        algorithms=st.lists(st.sampled_from(["HS256", "HS384", "HS512"]), min_size=1),
        audience=malformed_secret_strategy,
    )
    @settings(max_examples=500, suppress_health_check=[HealthCheck.too_slow])
    def test_fuzz_jwt_fuzz_decode_jwt_malformed_audience(
        self, token, secret, algorithms, audience
    ) -> None:
        """Bombard decode_jwt with extreme, malformed audience types."""
        result = decode_jwt(token, secret, algorithms=algorithms, audience=audience)
        assert result.is_err(), "Expected malformed audience to result in an Error"

    @given(
        payload=st.dictionaries(st.text(), st.text()),
        secret=malformed_secret_strategy,
        algorithm=st.sampled_from(["HS256"]),
    )
    @settings(max_examples=500, suppress_health_check=[HealthCheck.too_slow])
    def test_fuzz_jwt_fuzz_encode_jwt_malformed_secret(
        self, payload, secret, algorithm
    ) -> None:
        """Bombard encode_jwt with extreme, malformed secret types."""
        result = encode_jwt(payload, secret, algorithm=algorithm)
        assert result.is_err(), "Expected malformed secret to result in an Error"

    @given(
        payload=st.dictionaries(st.text(), st.text(), max_size=5),
        secret_key=st.text(),
        algorithm=st.one_of(
            st.integers(), st.floats(), st.booleans(), st.none(), st.lists(st.text())
        ),
    )
    @settings(max_examples=500, suppress_health_check=[HealthCheck.too_slow])
    def test_fuzz_jwt_fuzz_encode_jwt_malformed_algorithm(
        self, payload, secret_key, algorithm
    ):
        result = encode_jwt(payload, secret_key, algorithm=algorithm)
        assert result.is_err(), "Expected malformed algorithm to result in an Error"

    def test_fuzz_jwt_fuzz_encode_jwt_unserializable_payload(self) -> None:
        """Test encode_jwt handles entirely un-serializable objects cleanly."""

        class Unserializable:
            pass

        payload = {"bad": Unserializable()}
        result = encode_jwt(payload, "secret", algorithm="HS256")
        assert result.is_err(), "Expected unserializable payload to result in an Error"
