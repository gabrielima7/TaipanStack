"""Tests for the password hashing utilities."""
from pydantic import SecretStr

from taipanstack.security.password import hash_password, verify_password


def test_security_password_hash_password_expected() -> None:
    """Test that hashing a password produces a valid-looking hash."""
    password = "secure_password"
    pwd_hash = hash_password(password)
    assert pwd_hash.startswith("$argon2")

def test_hash_password_secret_str_expected() -> None:
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

def test_verify_password_failure_expected() -> None:
    """Test that an incorrect password fails verification."""
    password = "my_password"
    pwd_hash = hash_password(password)
    assert verify_password("wrong_password", pwd_hash) is False

def test_verify_password_invalid_hash_expected() -> None:
    """Test that invalid hash formats are handled gracefully."""
    password = "my_password"
    assert verify_password(password, "invalid_hash") is False
    assert verify_password(password, "$argon2$invalid$hash") is False
    assert verify_password(password, "alg$100$salt$hash") is False
    assert verify_password(password, "pbkdf2_sha256$nan$salt$hash") is False
    assert verify_password(password, "pbkdf2_sha256$100$nothex$hash") is False
    assert verify_password(password, "pbkdf2_sha256$100$salt$nothex") is False
    assert verify_password(password, "pbkdf2_sha256$100$salt") is False

def test_verify_legacy_password_expected() -> None:
    """Test that legacy PBKDF2 hashes are still verifiable."""
    password = "my_password"
    import hashlib
    salt = b"1234567890123456"
    iterations = 600000
    hash_bytes = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    pwd_hash = f"pbkdf2_sha256${iterations}${salt.hex()}${hash_bytes.hex()}"
    assert verify_password(password, pwd_hash) is True
    assert verify_password("wrong_password", pwd_hash) is False

def test_verify_legacy_password_too_many_iterations_expected() -> None:
    """Test that legacy PBKDF2 hashes with too many iterations are rejected."""
    password = "my_password"
    salt = b"1234567890123456"
    hash_bytes = b"fakehash"
    iterations = 1000001
    pwd_hash = f"pbkdf2_sha256${iterations}${salt.hex()}${hash_bytes.hex()}"
    assert verify_password(password, pwd_hash) is False

def test_hash_password_is_random_expected() -> None:
    """Test that hashing the same password twice produces different hashes due to salt."""
    password = "my_password"
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    assert hash1 != hash2
    assert verify_password(password, hash1) is True
    assert verify_password(password, hash2) is True

def test_verify_password_invalid_type_password_expected() -> None:
    """Test that an invalid type for password raises a TypeError."""
    import pytest
    pwd_hash = hash_password("my_password")
    with pytest.raises(TypeError, match="password must be a string or SecretStr"):
        verify_password(123, pwd_hash)

def test_verify_password_invalid_type_hash_expected() -> None:
    """Test that an invalid type for password_hash raises a TypeError."""
    import pytest
    with pytest.raises(TypeError, match="password_hash must be a string"):
        verify_password("my_password", 123)
