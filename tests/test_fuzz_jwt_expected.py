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
    def test_fuzz_jwt_fuzz_encode_jwt_malformed_payload_payload_types(
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
    def test_fuzz_jwt_fuzz_decode_jwt_malformed_token_token_types(
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
    def test_fuzz_jwt_fuzz_encode_jwt_malformed_secret_secret_types(
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
    def test_fuzz_jwt_fuzz_encode_jwt_malformed_algorithm_expected(
        self, payload, secret_key, algorithm
    ):
        result = encode_jwt(payload, secret_key, algorithm=algorithm)
        assert result.is_err() or result.is_ok(), (
            "Expected malformed algorithm to result in an Error or OK"
        )

    @given(
        payload=st.dictionaries(st.text(), st.text(), max_size=5),
        secret_key=st.text(min_size=32),
        algorithm=st.text(
            alphabet=st.characters(
                blacklist_characters=["\x00"],
                min_codepoint=0x200B,
                max_codepoint=0x200F,
            ),
        ),
    )
    @settings(
        max_examples=500,
        suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
    )
    def test_fuzz_jwt_fuzz_encode_jwt_non_ascii_algorithm_expected(
        self, payload, secret_key, algorithm
    ):
        result = encode_jwt(payload, secret_key, algorithm=algorithm)
        assert result.is_err() or result.is_ok(), (
            "Expected malformed algorithm to result in an Error or OK"
        )

    @given(
        token=st.text(),
        secret_key=st.text(min_size=32),
        algorithms=st.lists(
            st.text(
                alphabet=st.characters(
                    blacklist_characters=["\x00"],
                    min_codepoint=0x200B,
                    max_codepoint=0x200F,
                ),
            ),
            min_size=1,
        ),
        audience=st.text(),
    )
    @settings(
        max_examples=500,
        suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
    )
    def test_fuzz_jwt_fuzz_decode_jwt_non_ascii_algorithm_expected(
        self, token, secret_key, algorithms, audience
    ):
        result = decode_jwt(token, secret_key, algorithms=algorithms, audience=audience)
        assert result.is_err() or result.is_ok(), (
            "Expected malformed algorithm to result in an Error or OK"
        )

    @given(
        token=st.text(),
        secret_key=st.text(min_size=32),
        algorithms=st.text() | st.integers() | st.floats() | st.booleans() | st.none(),
        audience=st.text(),
    )
    @settings(
        max_examples=500,
        suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
    )
    def test_fuzz_jwt_fuzz_decode_jwt_malformed_algorithms_expected(
        self, token, secret_key, algorithms, audience
    ):
        result = decode_jwt(token, secret_key, algorithms=algorithms, audience=audience)
        assert result.is_err() or result.is_ok(), (
            "Expected malformed algorithm to result in an Error or OK"
        )

    @given(
        payload=st.dictionaries(st.text(), st.text(), max_size=5),
        secret_key=st.text(min_size=32),
        algorithm=st.sampled_from(["none", "None", "nOnE"]),
    )
    @settings(
        max_examples=500,
        suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
    )
    def test_fuzz_jwt_fuzz_encode_jwt_none_algorithm_expected(
        self, payload, secret_key, algorithm
    ):
        result = encode_jwt(payload, secret_key, algorithm=algorithm)
        assert result.is_err(), "Expected none algorithm to result in an Error"

    @given(
        token=st.text(),
        secret_key=st.text(min_size=32),
        algorithms=st.lists(
            st.sampled_from(["none", "None", "nOnE", "HS256"]), min_size=1
        ),
        audience=st.text(),
    )
    @settings(
        max_examples=500,
        suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
    )
    def test_fuzz_jwt_fuzz_decode_jwt_none_algorithm_expected(
        self, token, secret_key, algorithms, audience
    ):
        result = decode_jwt(token, secret_key, algorithms=algorithms, audience=audience)
        assert result.is_err(), "Expected none algorithm to result in an Error"

    @given(
        payload=st.dictionaries(st.text(), st.text(), max_size=5),
        secret_key=st.text(min_size=32),
        algorithm=st.sampled_from(["nOnE😊", "None\x00"]),
    )
    @settings(
        max_examples=500,
        suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
    )
    def test_fuzz_jwt_fuzz_encode_jwt_none_ascii_algorithm_expected(
        self, payload, secret_key, algorithm
    ):
        result = encode_jwt(payload, secret_key, algorithm=algorithm)
        assert result.is_err(), "Expected none algorithm to result in an Error"

    @given(
        token=st.text(),
        secret_key=st.text(min_size=32),
        algorithms=st.lists(st.sampled_from(["nOnE😊", "None\x00"]), min_size=1),
        audience=st.text(),
    )
    @settings(
        max_examples=500,
        suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
    )
    def test_fuzz_jwt_fuzz_decode_jwt_none_ascii_algorithm_expected(
        self, token, secret_key, algorithms, audience
    ):
        result = decode_jwt(token, secret_key, algorithms=algorithms, audience=audience)
        assert result.is_err(), "Expected none algorithm to result in an Error"

    @given(
        payload=st.dictionaries(st.text(), st.text(), max_size=5),
        secret_key=st.text(min_size=32),
        algorithm=st.sampled_from(["HS256"]),
    )
    @settings(
        max_examples=500,
        suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
    )
    def test_fuzz_jwt_fuzz_encode_jwt_valid_algorithm_expected(
        self, payload, secret_key, algorithm
    ):
        result = encode_jwt(payload, secret_key, algorithm=algorithm)
        assert result.is_ok(), "Expected valid algorithm to result in an Ok"

    @given(
        token=st.text(),
        secret_key=st.text(min_size=32),
        algorithms=st.lists(st.sampled_from(["HS256"]), min_size=1),
        audience=st.text(),
    )
    @settings(
        max_examples=500,
        suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
    )
    def test_fuzz_jwt_fuzz_decode_jwt_valid_algorithm_expected(
        self, token, secret_key, algorithms, audience
    ):
        result = decode_jwt(token, secret_key, algorithms=algorithms, audience=audience)
        assert result.is_err(), "Expected malformed token to result in an Error"
