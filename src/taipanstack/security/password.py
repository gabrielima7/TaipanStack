"""
Password hashing utilities using PBKDF2.
"""

import hashlib
import secrets

# OWASP recommended iterations for PBKDF2-HMAC-SHA256
DEFAULT_ITERATIONS = 600_000
SALT_SIZE = 16
HASH_ALGORITHM = "sha256"


def hash_password(password: str, iterations: int = DEFAULT_ITERATIONS) -> str:
    """
    Hash a password using PBKDF2-HMAC-SHA256.

    Args:
        password: The cleartext password to hash.
        iterations: The number of iterations to use.

    Returns:
        A string in the format: pbkdf2_sha256$iterations$salt$hash
    """
    salt = secrets.token_bytes(SALT_SIZE)
    hash_bytes = hashlib.pbkdf2_hmac(
        HASH_ALGORITHM,
        password.encode("utf-8"),
        salt,
        iterations,
    )
    return f"pbkdf2_{HASH_ALGORITHM}${iterations}${salt.hex()}${hash_bytes.hex()}"


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify a password against a hash.

    Args:
        password: The cleartext password to verify.
        hashed: The hashed password to verify against.

    Returns:
        True if the password matches, False otherwise.
    """
    try:
        algorithm, iterations_str, salt_hex, hash_hex = hashed.split("$")
        if algorithm != f"pbkdf2_{HASH_ALGORITHM}":
            return False
        iterations = int(iterations_str)
        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(hash_hex)

        actual_hash = hashlib.pbkdf2_hmac(
            HASH_ALGORITHM,
            password.encode("utf-8"),
            salt,
            iterations,
        )
        return secrets.compare_digest(actual_hash, expected_hash)
    except (ValueError, TypeError):
        return False
