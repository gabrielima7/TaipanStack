"""
Secure JWT Utility module.

Provides explicitly secure wrappers around PyJWT encoding and decoding,
enforcing strict validation of algorithms, expiration, and audience claims.
All operations return ``Result`` types.
"""

from collections.abc import Iterable
from typing import TypeAlias

import jwt
from jwt.exceptions import PyJWTError

from taipanstack.core.result import safe_from

__all__ = ["decode_jwt", "encode_jwt"]

JWTPayload: TypeAlias = dict[str, object]


@safe_from(PyJWTError, ValueError, TypeError)
def encode_jwt(
    payload: JWTPayload,
    secret_key: str,
    algorithm: str = "HS256",
) -> str:
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
    if str(algorithm).strip().lower() == "none":
        raise ValueError('Algorithm "none" is explicitly disallowed.')

    return jwt.encode(payload, secret_key, algorithm=algorithm)


@safe_from(PyJWTError, ValueError, TypeError, AttributeError)
def decode_jwt(
    token: str,
    secret_key: str,
    algorithms: list[str],
    audience: str | Iterable[str],
) -> JWTPayload:
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
    if any(str(alg).strip().lower() == "none" for alg in algorithms):
        raise ValueError('Algorithm "none" is explicitly disallowed for decoding.')

    # We enforce 'exp' and 'aud' through PyJWT's options parameter
    options = {
        "require": ["exp", "aud"],
        "verify_signature": True,
        "verify_exp": True,
        "verify_aud": True,
    }

    return jwt.decode(
        token,
        secret_key,
        algorithms=algorithms,
        audience=audience,
        options=options,  # type: ignore[arg-type]
    )
