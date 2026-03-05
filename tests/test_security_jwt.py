"""Tests for the secure JWT module."""

import datetime

import jwt

from taipanstack.security.jwt import decode_jwt, encode_jwt


class TestEncodeJWT:
    """Tests for encode_jwt."""

    def test_encode_success(self) -> None:
        """Test successful encoding of a JWT."""
        payload = {"sub": "user_123", "aud": "my_app"}
        secret = "super_secret_key_that_is_at_least_32_bytes_long"  # noqa: S105

        result = encode_jwt(payload, secret)
        assert result.is_ok()
        token = result.unwrap()
        assert isinstance(token, str)
        assert len(token) > 0

    def test_encode_rejects_none_algorithm(self) -> None:
        """Test that encoding explicitly rejects the 'none' algorithm."""
        payload = {"sub": "user_123"}
        secret = "super_secret_key_that_is_at_least_32_bytes_long"  # noqa: S105

        result = encode_jwt(payload, secret, algorithm="none")
        assert result.is_err()
        assert isinstance(result.err(), ValueError)
        assert "explicitly disallowed" in str(result.err())

        result2 = encode_jwt(payload, secret, algorithm="nOnE")
        assert result2.is_err()
        assert isinstance(result2.err(), ValueError)


class TestDecodeJWT:
    """Tests for decode_jwt."""

    def test_decode_success(self) -> None:
        """Test successful decoding of a fully validated JWT."""
        secret = "super_secret_key_that_is_at_least_32_bytes_long"  # noqa: S105
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

    def test_decode_rejects_none_algorithm(self) -> None:
        """Test that mapping 'none' algorithm to decode is blocked."""
        secret = "super_secret_key_that_is_at_least_32_bytes_long"  # noqa: S105
        result = decode_jwt(
            "some.token.str", secret, algorithms=["HS256", "none"], audience="my_app"
        )
        assert result.is_err()
        assert isinstance(result.err(), ValueError)
        assert "explicitly disallowed" in str(result.err())

    def test_decode_requires_exp(self) -> None:
        """Test that decoding strictly requires an 'exp' claim."""
        secret = "super_secret_key_that_is_at_least_32_bytes_long"  # noqa: S105
        # Omit 'exp'
        payload = {"sub": "user_123", "aud": "my_app"}
        token = jwt.encode(payload, secret, algorithm="HS256")

        result = decode_jwt(token, secret, algorithms=["HS256"], audience="my_app")
        assert result.is_err()
        assert isinstance(result.err(), jwt.exceptions.MissingRequiredClaimError)

    def test_decode_requires_aud(self) -> None:
        """Test that decoding strictly requires an 'aud' claim."""
        secret = "super_secret_key_that_is_at_least_32_bytes_long"  # noqa: S105
        exp_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
        # Omit 'aud'
        payload = {"sub": "user_123", "exp": exp_time}
        token = jwt.encode(payload, secret, algorithm="HS256")

        result = decode_jwt(token, secret, algorithms=["HS256"], audience="my_app")
        assert result.is_err()
        assert isinstance(result.err(), jwt.exceptions.MissingRequiredClaimError)

    def test_decode_invalid_signature(self) -> None:
        """Test that decoding fails with wrong secret."""
        secret = "super_secret_key_that_is_at_least_32_bytes_long"  # noqa: S105
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
        assert isinstance(result.err(), jwt.exceptions.InvalidSignatureError)

    def test_decode_expired_token(self) -> None:
        """Test that decoding explicitly fails for expired tokens."""
        secret = "super_secret_key_that_is_at_least_32_bytes_long"  # noqa: S105
        # Expired 1 hour ago
        exp_time = datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=1)
        payload = {"sub": "user_123", "aud": "my_app", "exp": exp_time}
        token = jwt.encode(payload, secret, algorithm="HS256")

        result = decode_jwt(token, secret, algorithms=["HS256"], audience="my_app")
        assert result.is_err()
        assert isinstance(result.err(), jwt.exceptions.ExpiredSignatureError)

    def test_decode_wrong_audience(self) -> None:
        """Test that decoding fails if audience doesn't match."""
        secret = "super_secret_key_that_is_at_least_32_bytes_long"  # noqa: S105
        exp_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
        payload = {"sub": "user_123", "aud": "other_app", "exp": exp_time}
        token = jwt.encode(payload, secret, algorithm="HS256")

        result = decode_jwt(token, secret, algorithms=["HS256"], audience="my_app")
        assert result.is_err()
        assert isinstance(result.err(), jwt.exceptions.InvalidAudienceError)
