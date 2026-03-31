"""
Password hashing and verification utilities.

This module provides functions for secure password management using Argon2,
with fallback verification support for PBKDF2-HMAC-SHA256.
"""

import functools
import hashlib
import os
import secrets

import argon2
from argon2.exceptions import VerifyMismatchError
from pydantic import SecretStr


@functools.lru_cache(maxsize=1)
def _get_cached_hasher(
    time_cost: int, memory_cost: int, parallelism: int
) -> argon2.PasswordHasher:
    return argon2.PasswordHasher(
        time_cost=time_cost,
        memory_cost=memory_cost,
        parallelism=parallelism,
    )


def get_password_hasher() -> argon2.PasswordHasher:
    """Get a configured Argon2 hasher instance based on environment variables."""
    try:
        time_cost = int(os.getenv("ARGON2_TIME_COST", "3"))
    except ValueError:
        time_cost = 3

    try:
        memory_cost = int(os.getenv("ARGON2_MEMORY_COST", "65536"))
    except ValueError:
        memory_cost = 65536

    try:
        parallelism = int(os.getenv("ARGON2_PARALLELISM", "4"))
    except ValueError:
        parallelism = 4

    return _get_cached_hasher(time_cost, memory_cost, parallelism)


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

    return get_password_hasher().hash(password_str)


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
        except (ValueError, TypeError, OverflowError):
            return False

    # Argon2 verification
    try:
        return get_password_hasher().verify(password_hash, password_str)
    except (
        VerifyMismatchError,
        ValueError,
        TypeError,
        argon2.exceptions.InvalidHashError,
    ):
        return False
