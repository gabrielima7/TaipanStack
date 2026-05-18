"""Tests for the secure JWT module."""

import datetime

import jwt

from taipanstack.security.jwt import decode_jwt, encode_jwt


class TestEncodeJWT:
    """Tests for encode_jwt."""

    def test_security_jwt_encode_success(self) -> None:
        """Test successful encoding of a JWT."""
        payload = {"sub": "user_123", "aud": "my_app"}
        secret = "super_secret_key_that_is_at_least_32_bytes_long"

        result = encode_jwt(payload, secret)
        assert result.is_ok()
        token = result.unwrap()
        assert isinstance(token, str)
        assert len(token) > 0

    def test_security_jwt_encode_rejects_none_algorithm(self) -> None:
        """Test that encoding explicitly rejects the 'none' algorithm."""
        payload = {"sub": "user_123"}
        secret = "super_secret_key_that_is_at_least_32_bytes_long"

        result = encode_jwt(payload, secret, algorithm="none")
        assert result.is_err()
        assert isinstance(result.err_value, ValueError)
        assert "explicitly disallowed" in str(result.err_value)

        result2 = encode_jwt(payload, secret, algorithm="nOnE")
        assert result2.is_err()
        assert isinstance(result2.err_value, ValueError)


class TestDecodeJWT:
    """Tests for decode_jwt."""

    def test_security_jwt_decode_success(self) -> None:
        """Test successful decoding of a fully validated JWT."""
        secret = "super_secret_key_that_is_at_least_32_bytes_long"
        # Calculate Future expiration time manually since PyJWT uses naive UTC heavily
        exp_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
        payload = {"sub": "user_123", "aud": "my_app", "exp": exp_time}

        # We know encode works from encode_success
        token = jwt.encode(payload, secret, algorithm="HS256")

        result = decode_jwt(token, secret, algorithms=["HS256"], audience="my_app")
        assert result.is_ok()
        decoded = result.unwrap()
        assert decoded["sub"] == "user_123"
        assert decoded["aud"] == "my_app"

    def test_security_jwt_decode_rejects_none_algorithm(self) -> None:
        """Test that mapping 'none' algorithm to decode is blocked."""
        secret = "super_secret_key_that_is_at_least_32_bytes_long"
        result = decode_jwt(
            "some.token.str", secret, algorithms=["HS256", "none"], audience="my_app"
        )
        assert result.is_err()
        assert isinstance(result.err_value, ValueError)
        assert "explicitly disallowed" in str(result.err_value)

    def test_security_jwt_decode_requires_exp(self) -> None:
        """Test that decoding strictly requires an 'exp' claim."""
        secret = "super_secret_key_that_is_at_least_32_bytes_long"
        # Omit 'exp'
        payload = {"sub": "user_123", "aud": "my_app"}
        token = jwt.encode(payload, secret, algorithm="HS256")

        result = decode_jwt(token, secret, algorithms=["HS256"], audience="my_app")
        assert result.is_err()
        assert isinstance(result.err_value, jwt.exceptions.MissingRequiredClaimError)

    def test_security_jwt_decode_requires_aud(self) -> None:
        """Test that decoding strictly requires an 'aud' claim."""
        secret = "super_secret_key_that_is_at_least_32_bytes_long"
        exp_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
        # Omit 'aud'
        payload = {"sub": "user_123", "exp": exp_time}
        token = jwt.encode(payload, secret, algorithm="HS256")

        result = decode_jwt(token, secret, algorithms=["HS256"], audience="my_app")
        assert result.is_err()
        assert isinstance(result.err_value, jwt.exceptions.MissingRequiredClaimError)

    def test_security_jwt_decode_invalid_signature(self) -> None:
        """Test that decoding fails with wrong secret."""
        secret = "super_secret_key_that_is_at_least_32_bytes_long"
        exp_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
        payload = {"sub": "user_123", "aud": "my_app", "exp": exp_time}
        token = jwt.encode(payload, secret, algorithm="HS256")

        result = decode_jwt(
            token,
            "wrong_secret_that_is_at_least_32_bytes_long",
            algorithms=["HS256"],
            audience="my_app",
        )
        assert result.is_err()
        assert isinstance(result.err_value, jwt.exceptions.InvalidSignatureError)

    def test_security_jwt_decode_expired_token(self) -> None:
        """Test that decoding explicitly fails for expired tokens."""
        secret = "super_secret_key_that_is_at_least_32_bytes_long"
        # Expired 1 hour ago
        exp_time = datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=1)
        payload = {"sub": "user_123", "aud": "my_app", "exp": exp_time}
        token = jwt.encode(payload, secret, algorithm="HS256")

        result = decode_jwt(token, secret, algorithms=["HS256"], audience="my_app")
        assert result.is_err()
        assert isinstance(result.err_value, jwt.exceptions.ExpiredSignatureError)

    def test_security_jwt_decode_wrong_audience(self) -> None:
        """Test that decoding fails if audience doesn't match."""
        secret = "super_secret_key_that_is_at_least_32_bytes_long"
        exp_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
        payload = {"sub": "user_123", "aud": "other_app", "exp": exp_time}
        token = jwt.encode(payload, secret, algorithm="HS256")

        result = decode_jwt(token, secret, algorithms=["HS256"], audience="my_app")
        assert result.is_err()
        assert isinstance(result.err_value, jwt.exceptions.InvalidAudienceError)


# Migrated from tests/test_fuzz_jwt_operations.py
"""Property-based fuzzing tests for the secure JWT module."""

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

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
