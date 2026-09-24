"""Tests for the password hashing utilities."""

from pydantic import SecretStr

from taipanstack.core.result import Err
from taipanstack.security.password import hash_password, verify_password


def test_security_password_hash_password() -> None:
    """Test that hashing a password produces a valid-looking hash."""
    password = "secure_password"
    pwd_hash = hash_password(password).unwrap()

    assert pwd_hash.startswith("$argon2")


def test_security_password_hash_password_secret_str() -> None:
    """Test that hashing a SecretStr works correctly."""
    password = SecretStr("secure_password")
    pwd_hash = hash_password(password).unwrap()

    assert pwd_hash.startswith("$argon2")
    assert verify_password(password, pwd_hash).unwrap()


def test_security_password_verify_password_success() -> None:
    """Test that a correct password verifies successfully."""
    password = "my_password"
    pwd_hash = hash_password(password).unwrap()

    assert verify_password(password, pwd_hash).unwrap() is True
    assert verify_password(SecretStr(password), pwd_hash).unwrap() is True


def test_security_password_verify_password_failure() -> None:
    """Test that an incorrect password fails verification."""
    password = "my_password"
    pwd_hash = hash_password(password).unwrap()

    assert verify_password("wrong_password", pwd_hash).unwrap() is False


def test_security_password_verify_password_invalid_hash() -> None:
    """Test that invalid hash formats are handled gracefully."""
    password = "my_password"

    assert verify_password(password, "invalid_hash").unwrap() is False
    assert verify_password(password, "$argon2$invalid$hash").unwrap() is False
    assert (
        verify_password(password, "alg$100$salt$hash").unwrap() is False
    )  # Wrong algorithm
    assert (
        verify_password(password, "pbkdf2_sha256$nan$salt$hash").unwrap() is False
    )  # Invalid iterations
    assert (
        verify_password(password, "pbkdf2_sha256$100$nothex$hash").unwrap() is False
    )  # Invalid salt hex
    assert (
        verify_password(password, "pbkdf2_sha256$100$salt$nothex").unwrap() is False
    )  # Invalid hash hex
    assert (
        verify_password(password, "pbkdf2_sha256$100$salt").unwrap() is False
    )  # Invalid parts length


def test_security_password_verify_legacy_password() -> None:
    """Test that legacy PBKDF2 hashes are still verifiable."""
    password = "my_password"
    # This is a pre-generated PBKDF2 hash of "my_password"
    # Format: pbkdf2_sha256$600000$salt$hash
    # Salt and hash need to be valid hex strings for verify_password.
    # We will compute a valid one manually to verify verification logic.
    import hashlib

    salt = b"1234567890123456"
    iterations = 600000
    hash_bytes = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations,
    )
    pwd_hash = f"pbkdf2_sha256${iterations}${salt.hex()}${hash_bytes.hex()}"

    assert verify_password(password, pwd_hash).unwrap() is True
    assert verify_password("wrong_password", pwd_hash).unwrap() is False


def test_security_password_verify_legacy_password_too_many_iterations() -> None:
    """Test that legacy PBKDF2 hashes with too many iterations are rejected."""
    password = "my_password"
    salt = b"1234567890123456"
    hash_bytes = b"fakehash"
    iterations = 1_000_001
    pwd_hash = f"pbkdf2_sha256${iterations}${salt.hex()}${hash_bytes.hex()}"

    assert verify_password(password, pwd_hash).unwrap() is False


def test_security_password_hash_password_is_random() -> None:
    """Test that hashing the same password twice produces different hashes due to salt."""
    password = "my_password"
    hash1 = hash_password(password).unwrap()
    hash2 = hash_password(password).unwrap()

    assert hash1 != hash2
    assert verify_password(password, hash1).unwrap() is True
    assert verify_password(password, hash2).unwrap() is True


def test_security_password_verify_password_invalid_type_password() -> None:
    """Test that an invalid type for password raises a TypeError."""

    pwd_hash = hash_password("my_password").unwrap()

    res = verify_password(123, pwd_hash)  # type: ignore[arg-type]
    assert isinstance(res, Err)
    assert isinstance(res.err_value, TypeError)
    assert "password must be a string or SecretStr" in str(res.err_value)


def test_security_password_verify_password_invalid_type_hash() -> None:
    """Test that an invalid type for password_hash raises a TypeError."""

    res = verify_password("my_password", 123)  # type: ignore[arg-type]
    assert isinstance(res, Err)
    assert isinstance(res.err_value, TypeError)
    assert "password_hash must be a string" in str(res.err_value)


def test_security_password_verify_password_empty() -> None:
    """Test that verifying an empty password returns False."""
    assert verify_password("", "hash").unwrap() is False
    assert verify_password(SecretStr(""), "hash").unwrap() is False


def test_security_password_verify_password_too_long() -> None:
    """Test that verifying a too long password returns False."""
    assert verify_password("a" * 1025, "hash").unwrap() is False
    assert verify_password(SecretStr("a" * 1025), "hash").unwrap() is False


def test_security_password_hash_password_empty() -> None:
    """Test that hashing an empty password raises ValueError."""

    res = hash_password("")
    assert isinstance(res, Err)
    assert isinstance(res.err_value, ValueError)
    assert "password cannot be empty" in str(res.err_value)


def test_security_password_hash_password_too_long() -> None:
    """Test that hashing a too long password returns Err."""
    res = hash_password("a" * 1025)
    assert isinstance(res, Err)
    assert isinstance(res.err_value, ValueError)
    assert "password length exceeds" in str(res.err_value)
