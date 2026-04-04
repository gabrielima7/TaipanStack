"""
Password hashing and verification utilities.

This module provides functions for secure password management using Argon2,
with fallback verification support for PBKDF2-HMAC-SHA256.
"""

import hashlib
import secrets

import argon2
from argon2.exceptions import VerifyMismatchError
from pydantic import SecretStr

# Global Argon2 PasswordHasher instance
_ph = argon2.PasswordHasher()

# Legacy PBKDF2 Constants
LEGACY_HASH_ALGORITHM = "sha256"
LEGACY_FORMAT = "pbkdf2_sha256"
MAX_LEGACY_ITERATIONS = 1_000_000


# Constants to prevent DoS via massive processing times
MAX_PASSWORD_LENGTH = 1024


def hash_password(password: str | SecretStr) -> str:
    """
    Hash a password using Argon2id.

    Args:
        password: The plaintext password to hash.

    Returns:
        The hashed password in Argon2 format.

    Raises:
        TypeError: If `password` is not a str or SecretStr.
        ValueError: If `password` length exceeds the maximum allowed or is empty.

    """
    if not isinstance(password, (str, SecretStr)):
        msg = "password must be a string or SecretStr"
        raise TypeError(msg)

    if isinstance(password, SecretStr):
        password_str = password.get_secret_value()
    else:
        password_str = password

    if not password_str:
        msg = "password cannot be empty"
        raise ValueError(msg)

    if len(password_str) > MAX_PASSWORD_LENGTH:
        msg = f"password length exceeds {MAX_PASSWORD_LENGTH} characters"
        raise ValueError(msg)

    return _ph.hash(password_str)


def verify_password(password: str | SecretStr, password_hash: str) -> bool:  # noqa: PLR0911
    """
    Verify a password against an Argon2 or legacy PBKDF2-HMAC-SHA256 hash.

    Args:
        password: The plaintext password to verify.
        password_hash: The stored password hash.

    Returns:
        True if the password matches the hash, False otherwise.

    Raises:
        TypeError: If `password` or `password_hash` are not the correct types.

    """
    if not isinstance(password, (str, SecretStr)):
        msg = "password must be a string or SecretStr"
        raise TypeError(msg)

    if not isinstance(password_hash, str):
        msg = "password_hash must be a string"
        raise TypeError(msg)

    if isinstance(password, SecretStr):
        password_str = password.get_secret_value()
    else:
        password_str = password

    if not password_str:
        return False

    if len(password_str) > MAX_PASSWORD_LENGTH:
        return False

    if password_hash.startswith(LEGACY_FORMAT + "$"):
        # Legacy PBKDF2 verification
        try:
            parts = password_hash.split("$")
            if len(parts) != 4:  # noqa: PLR2004
                return False

            _algorithm, iterations_str, salt_hex, hash_hex = parts

            iterations = int(iterations_str)
            if iterations > MAX_LEGACY_ITERATIONS:
                return False

            salt = bytes.fromhex(salt_hex)
            stored_hash = bytes.fromhex(hash_hex)

            new_hash = hashlib.pbkdf2_hmac(
                LEGACY_HASH_ALGORITHM,
                password_str.encode("utf-8"),
                salt,
                iterations,
            )

            return secrets.compare_digest(new_hash, stored_hash)
        except (ValueError, TypeError, OverflowError):
            return False

    # Argon2 verification
    try:
        return _ph.verify(password_hash, password_str)
    except (
        VerifyMismatchError,
        ValueError,
        TypeError,
        argon2.exceptions.InvalidHashError,
    ):
        return False
