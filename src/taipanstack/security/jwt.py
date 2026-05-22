"""
Secure JWT Utility module.

Provides explicitly secure wrappers around PyJWT encoding and decoding,
enforcing strict validation of algorithms, expiration, and audience claims.
All operations return ``Result`` types.
"""

import secrets
from collections.abc import Iterable
from typing import TYPE_CHECKING, TypeAlias

if TYPE_CHECKING:
    import jwt

import jwt

from taipanstack.core.result import Err, Ok, Result

__all__ = ["decode_jwt", "encode_jwt"]

JWTPayload: TypeAlias = dict[str, object]


def encode_jwt(
    payload: JWTPayload,
    secret_key: str,
    algorithm: str = "HS256",
) -> Result[str, Exception]:
    """Encode a payload into a JWT securely.

    Explicitly rejects the "none" algorithm to prevent bypass vulnerabilities.

    Args:
        payload: Dictionary containing the JWT claims.
        secret_key: The secret key for signing the token.
        algorithm: The signing algorithm (default "HS256").

    Returns:
        The encoded JWT string.

    Raises:
        ValueError: If the "none" algorithm is specified.
        PyJWTError: If encoding fails.

    """
    if not isinstance(payload, dict):
        return Err(TypeError("Payload must be a dictionary"))
    if not isinstance(secret_key, str):
        return Err(TypeError("Secret key must be a string"))
    if not isinstance(algorithm, str):
        return Err(TypeError("Algorithm must be a string"))

    if secrets.compare_digest(algorithm.strip().lower(), "none"):
        return Err(ValueError('Algorithm "none" is explicitly disallowed.'))

    try:
        return Ok(jwt.encode(payload, secret_key, algorithm=algorithm))  # nosem
    except Exception as e:
        return Err(e)


def decode_jwt(
    token: str,
    secret_key: str,
    algorithms: list[str],
    audience: str | Iterable[str],
) -> Result[JWTPayload, Exception]:
    """Decode a JWT securely with strict claim validation.

    Enforces that 'exp' (expiration) and 'aud' (audience) claims are present
    and validated. Explicitly rejects the "none" algorithm.

    Args:
        token: The encoded JWT string.
        secret_key: The secret key for verifying the signature.
        algorithms: List of exactly accepted algorithms.
        audience: The expected audience(s).

    Returns:
        The decoded payload dictionary.

    Raises:
        ValueError: If the "none" algorithm is present in the `algorithms` list.
        PyJWTError: If the token is invalid, expired, or has incorrect claims.

    """
    if (
        not isinstance(token, str)
        or not isinstance(secret_key, str)
        or not isinstance(algorithms, list)
        or not all(isinstance(alg, str) for alg in algorithms)
        or not isinstance(audience, (str, Iterable))
    ):
        return Err(TypeError("Invalid parameter types for decoding"))

    try:
        if any(
            secrets.compare_digest(alg.strip().lower(), "none") for alg in algorithms
        ):
            return Err(ValueError('Algorithm "none" is explicitly disallowed.'))
    except TypeError:
        return Err(TypeError("Algorithms must be a list of strings"))

    try:
        return Ok(
            jwt.decode(
                token,
                secret_key,
                algorithms=algorithms,
                audience=audience,
                options={
                    "require": ["exp", "aud"],
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_aud": True,
                },
            )
        )
    except Exception as e:
        return Err(e)
