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
from jwt.exceptions import PyJWTError

from taipanstack.core.result import safe_from

__all__ = ["decode_jwt", "encode_jwt"]

JWTPayload: TypeAlias = dict[str, object]


@safe_from(
    PyJWTError,
    ValueError,
    TypeError,
    NotImplementedError,
    KeyError,
    AttributeError,
    Exception,
)
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
    if not isinstance(algorithm, str):
        raise TypeError("Algorithm must be a string")

    if secrets.compare_digest(algorithm.strip().lower(), "none"):
        raise ValueError('Algorithm "none" is explicitly disallowed.')

    return jwt.encode(payload, secret_key, algorithm=algorithm)  # nosem


def _validate_jwt_algorithms(algorithms: list[str]) -> None:
    if not isinstance(algorithms, list):
        raise TypeError("Algorithms must be a list of strings")

    for alg in algorithms:
        if isinstance(alg, str) and secrets.compare_digest(alg.strip().lower(), "none"):
            raise ValueError('Algorithm "none" is explicitly disallowed for decoding.')


def _validate_jwt_audience(audience: str | Iterable[str]) -> None:
    if not isinstance(audience, (str, list, tuple, set)):
        raise TypeError("Audience must be a string or iterable of strings")


@safe_from(
    PyJWTError,
    ValueError,
    TypeError,
    AttributeError,
    NotImplementedError,
    KeyError,
    Exception,
)
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
    _validate_jwt_algorithms(algorithms)
    _validate_jwt_audience(audience)

    return jwt.decode(
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
