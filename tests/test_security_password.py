"""Tests for the password hashing utilities."""

from pydantic import SecretStr

from taipanstack.security.password import hash_password, verify_password


def test_hash_password() -> None:
    """Test that hashing a password produces a valid-looking hash."""
    password = "secure_password"
    pwd_hash = hash_password(password)

    assert pwd_hash.startswith("$argon2")


def test_hash_password_secret_str() -> None:
    """Test that hashing a SecretStr works correctly."""
    password = SecretStr("secure_password")
    pwd_hash = hash_password(password)

    assert pwd_hash.startswith("$argon2")
    assert verify_password(password, pwd_hash)


def test_verify_password_success() -> None:
    """Test that a correct password verifies successfully."""
    password = "my_password"
    pwd_hash = hash_password(password)

    assert verify_password(password, pwd_hash) is True
    assert verify_password(SecretStr(password), pwd_hash) is True


def test_verify_password_failure() -> None:
    """Test that an incorrect password fails verification."""
    password = "my_password"
    pwd_hash = hash_password(password)

    assert verify_password("wrong_password", pwd_hash) is False


def test_verify_password_invalid_hash() -> None:
    """Test that invalid hash formats are handled gracefully."""
    password = "my_password"

    assert verify_password(password, "invalid_hash") is False
    assert verify_password(password, "$argon2$invalid$hash") is False
    assert verify_password(password, "alg$100$salt$hash") is False  # Wrong algorithm
    assert (
        verify_password(password, "pbkdf2_sha256$nan$salt$hash") is False
    )  # Invalid iterations
    assert (
        verify_password(password, "pbkdf2_sha256$100$nothex$hash") is False
    )  # Invalid salt hex
    assert (
        verify_password(password, "pbkdf2_sha256$100$salt$nothex") is False
    )  # Invalid hash hex
    assert (
        verify_password(password, "pbkdf2_sha256$100$salt") is False
    )  # Invalid parts length


def test_verify_legacy_password() -> None:
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

    assert verify_password(password, pwd_hash) is True
    assert verify_password("wrong_password", pwd_hash) is False


def test_hash_password_is_random() -> None:
    """Test that hashing the same password twice produces different hashes due to salt."""
    password = "my_password"
    hash1 = hash_password(password)
    hash2 = hash_password(password)

    assert hash1 != hash2
    assert verify_password(password, hash1) is True
    assert verify_password(password, hash2) is True
