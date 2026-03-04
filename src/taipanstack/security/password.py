"""
Password hashing and verification utilities.

This module provides functions for secure password management using
PBKDF2-HMAC-SHA256.
"""

import hashlib
import secrets

from pydantic import SecretStr

# Constants for PBKDF2
ITERATIONS = 600_000
SALT_SIZE = 16
HASH_ALGORITHM = "sha256"
FORMAT = "pbkdf2_sha256"


def hash_password(password: str | SecretStr) -> str:
    """
    Hash a password using PBKDF2-HMAC-SHA256.

    Args:
        password: The plaintext password to hash.

    Returns:
        The hashed password in the format:
        pbkdf2_sha256$<iterations>$<salt_hex>$<hash_hex>

    """
    if isinstance(password, SecretStr):
        password_str = password.get_secret_value()
    else:
        password_str = password

    salt = secrets.token_bytes(SALT_SIZE)
    hash_bytes = hashlib.pbkdf2_hmac(
        HASH_ALGORITHM,
        password_str.encode("utf-8"),
        salt,
        ITERATIONS,
    )

    return f"{FORMAT}${ITERATIONS}${salt.hex()}${hash_bytes.hex()}"


def verify_password(password: str | SecretStr, password_hash: str) -> bool:
    """
    Verify a password against a PBKDF2-HMAC-SHA256 hash.

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

    try:
        parts = password_hash.split("$")
        if len(parts) != 4:  # noqa: PLR2004
            return False

        algorithm, iterations_str, salt_hex, hash_hex = parts
        if algorithm != FORMAT:
            return False

        iterations = int(iterations_str)
        salt = bytes.fromhex(salt_hex)
        stored_hash = bytes.fromhex(hash_hex)

        new_hash = hashlib.pbkdf2_hmac(
            HASH_ALGORITHM,
            password_str.encode("utf-8"),
            salt,
            iterations,
        )

        return secrets.compare_digest(new_hash, stored_hash)
    except (ValueError, TypeError):
        return False
