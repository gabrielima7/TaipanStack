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

from taipanstack.core.result import Err, Ok, Result, safe_from

# Global Argon2 PasswordHasher instance
_ph = argon2.PasswordHasher()

# Legacy PBKDF2 Constants
LEGACY_HASH_ALGORITHM = "sha256"
LEGACY_FORMAT = "pbkdf2_sha256"
MAX_LEGACY_ITERATIONS = 1_000_000


# Constants to prevent DoS via massive processing times
MAX_PASSWORD_LENGTH = 1024


def _get_password_str(password: str | SecretStr) -> Result[str, TypeError]:
    if not isinstance(password, (str, SecretStr)):
        msg = "password must be a string or SecretStr"  # type: ignore[unreachable]
        return Err(TypeError(msg))

    if isinstance(password, SecretStr):
        return Ok(password.get_secret_value())
    return Ok(password)


def hash_password(password: str | SecretStr) -> Result[str, ValueError | TypeError]:
    """
    Hash a password using Argon2id.

    Args:
        password: The plaintext password to hash.

    Returns:
        The hashed password in Argon2 format.

    """
    password_res = _get_password_str(password)
    if isinstance(password_res, Err):
        return password_res

    password_str = password_res.unwrap()

    if not password_str:
        msg = "password cannot be empty"
        return Err(ValueError(msg))

    if len(password_str) > MAX_PASSWORD_LENGTH:
        msg = f"password length exceeds {MAX_PASSWORD_LENGTH} characters"
        return Err(ValueError(msg))

    return Ok(_ph.hash(password_str))


@safe_from(ValueError, TypeError, OverflowError)
def _verify_legacy_pbkdf2_unsafe(password_str: str, password_hash: str) -> bool:
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


def _verify_legacy_pbkdf2(password_str: str, password_hash: str) -> bool:
    result = _verify_legacy_pbkdf2_unsafe(password_str, password_hash)
    if isinstance(result, Err):
        return False
    return result.unwrap()


@safe_from(
    VerifyMismatchError,
    ValueError,
    TypeError,
    argon2.exceptions.InvalidHashError,
    argon2.exceptions.VerificationError,
)
def _verify_argon2_unsafe(password_str: str, password_hash: str) -> bool:
    return _ph.verify(password_hash, password_str)


def _verify_argon2(password_str: str, password_hash: str) -> bool:
    result = _verify_argon2_unsafe(password_str, password_hash)
    if isinstance(result, Err):
        return False
    return result.unwrap()


def _is_valid_password_string(password_str: str) -> bool:
    """Validate a password string for emptiness and maximum length."""
    if not password_str:
        return False
    return len(password_str) <= MAX_PASSWORD_LENGTH


def verify_password(
    password: str | SecretStr, password_hash: str
) -> Result[bool, TypeError]:
    """
    Verify a password against an Argon2 or legacy PBKDF2-HMAC-SHA256 hash.

    Args:
        password: The plaintext password to verify.
        password_hash: The stored password hash.

    Returns:
        Ok(True) if the password matches the hash, Ok(False) otherwise.

    """
    password_res = _get_password_str(password)
    if isinstance(password_res, Err):
        return password_res

    password_str = password_res.unwrap()

    if not isinstance(password_hash, str):
        msg = "password_hash must be a string"  # type: ignore[unreachable]
        return Err(TypeError(msg))

    if not _is_valid_password_string(password_str):
        return Ok(False)

    if password_hash.startswith(LEGACY_FORMAT + "$"):
        return Ok(_verify_legacy_pbkdf2(password_str, password_hash))

    return Ok(_verify_argon2(password_str, password_hash))
