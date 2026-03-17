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
LEGACY_ITERATIONS = 600_000
LEGACY_SALT_SIZE = 16
LEGACY_HASH_ALGORITHM = "sha256"
LEGACY_FORMAT = "pbkdf2_sha256"


def hash_password(password: str | SecretStr) -> str:
    """
    Hash a password using Argon2id.

    Args:
        password: The plaintext password to hash.

    Returns:
        The hashed password in Argon2 format.

    """
    if isinstance(password, SecretStr):
        password_str = password.get_secret_value()
    else:
        password_str = password

    return _ph.hash(password_str)


def verify_password(password: str | SecretStr, password_hash: str) -> bool:
    """
    Verify a password against an Argon2 or legacy PBKDF2-HMAC-SHA256 hash.

    Args:
        password: The plaintext password to verify.
        password_hash: The stored password hash.

    Returns:
        True if the password matches the hash, False otherwise.

    """
    if isinstance(password, SecretStr):
        password_str = password.get_secret_value()
    else:
        password_str = password

    if password_hash.startswith(LEGACY_FORMAT + "$"):
        # Legacy PBKDF2 verification
        try:
            parts = password_hash.split("$")
            if len(parts) != 4:  # noqa: PLR2004
                return False

            _algorithm, iterations_str, salt_hex, hash_hex = parts

            iterations = int(iterations_str)
            salt = bytes.fromhex(salt_hex)
            stored_hash = bytes.fromhex(hash_hex)

            new_hash = hashlib.pbkdf2_hmac(
                LEGACY_HASH_ALGORITHM,
                password_str.encode("utf-8"),
                salt,
                iterations,
            )

            return secrets.compare_digest(new_hash, stored_hash)
        except (ValueError, TypeError):
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
