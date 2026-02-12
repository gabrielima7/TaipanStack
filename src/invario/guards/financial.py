"""
Financial security guards for Invario.

Zero-Trust guards for financial data validation. Each guard
raises SecurityError on violation, following TaipanStack's
guard pattern. These are designed for use with @validate_inputs.

All guards follow the contract:
    - Accept a single value
    - Return the validated value (possibly normalized)
    - Raise ValueError on invalid input (caught by @validate_inputs)
"""

from __future__ import annotations

import math
import re
from datetime import date
from decimal import Decimal, DecimalException, InvalidOperation
from uuid import UUID

# ISO 4217 currency codes (most common subset for fintech)
VALID_CURRENCY_CODES: frozenset[str] = frozenset({
    "AED", "ARS", "AUD", "BRL", "CAD", "CHF", "CLP", "CNY",
    "COP", "CZK", "DKK", "EUR", "GBP", "HKD", "HUF", "IDR",
    "ILS", "INR", "JPY", "KRW", "MXN", "MYR", "NOK", "NZD",
    "PEN", "PHP", "PLN", "RON", "RUB", "SAR", "SEK", "SGD",
    "THB", "TRY", "TWD", "UAH", "USD", "UYU", "VND", "ZAR",
})

# CPF: 11 digits, CNPJ: 14 digits
CPF_LENGTH = 11
CNPJ_LENGTH = 14

# COMPE: 3 digits, ISPB: 8 digits
COMPE_LENGTH = 3
ISPB_LENGTH = 8


def guard_positive_amount(amount: Decimal | str | int | float) -> Decimal:
    """Validate that a monetary amount is positive and finite.

    Accepts Decimal, str, int, or float and converts to Decimal.
    Rejects zero, negative, NaN, Infinity, and excessively precise values.

    Args:
        amount: The monetary amount to validate.

    Returns:
        The validated Decimal amount.

    Raises:
        ValueError: If amount is not a valid positive monetary value.

    Example:
        >>> guard_positive_amount(Decimal("150.50"))
        Decimal('150.50')
        >>> guard_positive_amount(-10)
        ValueError: Amount must be positive, got: -10

    """
    try:
        value = Decimal(str(amount))
    except (InvalidOperation, DecimalException, ValueError) as e:
        msg = f"Invalid amount format: {amount!r}"
        raise ValueError(msg) from e

    # Reject special values
    if value.is_nan() or value.is_infinite():
        msg = f"Amount must be finite, got: {amount!r}"
        raise ValueError(msg)

    # Reject non-positive
    if value <= 0:
        msg = f"Amount must be positive, got: {amount}"
        raise ValueError(msg)

    # Reject excessive decimal places (more than 2 for currency)
    _, _, exponent = value.as_tuple()
    if isinstance(exponent, int) and exponent < -2:
        msg = (
            f"Amount has too many decimal places: {amount}. "
            f"Maximum 2 decimal places allowed for currency"
        )
        raise ValueError(msg)

    return value


def guard_currency_code(code: str) -> str:
    """Validate ISO 4217 currency code.

    Args:
        code: Three-letter currency code.

    Returns:
        The validated, uppercased currency code.

    Raises:
        ValueError: If code is not a valid ISO 4217 currency.

    Example:
        >>> guard_currency_code("brl")
        'BRL'
        >>> guard_currency_code("XXX")
        ValueError: Invalid ISO 4217 currency code: XXX

    """
    if not code or not isinstance(code, str):
        msg = "Currency code cannot be empty"
        raise ValueError(msg)

    normalized = code.strip().upper()

    if len(normalized) != 3:
        msg = f"Currency code must be 3 characters, got {len(normalized)}: {code}"
        raise ValueError(msg)

    if not normalized.isalpha():
        msg = f"Currency code must contain only letters: {code}"
        raise ValueError(msg)

    if normalized not in VALID_CURRENCY_CODES:
        msg = f"Invalid ISO 4217 currency code: {normalized}"
        raise ValueError(msg)

    return normalized


def _cpf_check_digits(cpf_digits: list[int]) -> bool:
    """Validate CPF check digits (positions 9 and 10)."""
    # First check digit
    weights_1 = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    total = sum(d * w for d, w in zip(cpf_digits[:9], weights_1))
    remainder = total % 11
    first_check = 0 if remainder < 2 else 11 - remainder

    if cpf_digits[9] != first_check:
        return False

    # Second check digit
    weights_2 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    total = sum(d * w for d, w in zip(cpf_digits[:10], weights_2))
    remainder = total % 11
    second_check = 0 if remainder < 2 else 11 - remainder

    return cpf_digits[10] == second_check


def _cnpj_check_digits(cnpj_digits: list[int]) -> bool:
    """Validate CNPJ check digits (positions 12 and 13)."""
    # First check digit
    weights_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    total = sum(d * w for d, w in zip(cnpj_digits[:12], weights_1))
    remainder = total % 11
    first_check = 0 if remainder < 2 else 11 - remainder

    if cnpj_digits[12] != first_check:
        return False

    # Second check digit
    weights_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    total = sum(d * w for d, w in zip(cnpj_digits[:13], weights_2))
    remainder = total % 11
    second_check = 0 if remainder < 2 else 11 - remainder

    return cnpj_digits[13] == second_check


def guard_cpf_cnpj(document: str) -> str:
    """Validate a CPF or CNPJ document number.

    Accepts formatted (xxx.xxx.xxx-xx) or unformatted (xxxxxxxxxxx) input.
    Validates check digits using the official modulo-11 algorithm.

    Args:
        document: CPF (11 digits) or CNPJ (14 digits) string.

    Returns:
        The validated document with only digits (unformatted).

    Raises:
        ValueError: If document is invalid.

    Example:
        >>> guard_cpf_cnpj("529.982.247-25")
        '52998224725'

    """
    if not document or not isinstance(document, str):
        msg = "Document (CPF/CNPJ) cannot be empty"
        raise ValueError(msg)

    # Remove formatting characters
    digits_only = re.sub(r"[.\-/]", "", document.strip())

    if not digits_only.isdigit():
        msg = f"Document contains non-numeric characters: {document}"
        raise ValueError(msg)

    # Reject sequences of identical digits (e.g., 111.111.111-11)
    if len(set(digits_only)) == 1:
        msg = f"Document cannot be all identical digits: {document}"
        raise ValueError(msg)

    digit_list = [int(d) for d in digits_only]

    if len(digits_only) == CPF_LENGTH:
        if not _cpf_check_digits(digit_list):
            msg = f"Invalid CPF check digits: {document}"
            raise ValueError(msg)
    elif len(digits_only) == CNPJ_LENGTH:
        if not _cnpj_check_digits(digit_list):
            msg = f"Invalid CNPJ check digits: {document}"
            raise ValueError(msg)
    else:
        msg = (
            f"Document must be {CPF_LENGTH} (CPF) or {CNPJ_LENGTH} (CNPJ) digits, "
            f"got {len(digits_only)}: {document}"
        )
        raise ValueError(msg)

    return digits_only


def guard_bank_code(code: str) -> str:
    """Validate a Brazilian bank code (COMPE or ISPB).

    COMPE codes are 3 digits, ISPB codes are 8 digits.

    Args:
        code: Bank code string (3 or 8 digits).

    Returns:
        The validated bank code.

    Raises:
        ValueError: If code is not a valid bank identifier.

    Example:
        >>> guard_bank_code("001")
        '001'
        >>> guard_bank_code("00000000")
        '00000000'

    """
    if not code or not isinstance(code, str):
        msg = "Bank code cannot be empty"
        raise ValueError(msg)

    stripped = code.strip()

    if not stripped.isdigit():
        msg = f"Bank code must contain only digits: {code}"
        raise ValueError(msg)

    if len(stripped) not in (COMPE_LENGTH, ISPB_LENGTH):
        msg = (
            f"Bank code must be {COMPE_LENGTH} (COMPE) or "
            f"{ISPB_LENGTH} (ISPB) digits, got {len(stripped)}: {code}"
        )
        raise ValueError(msg)

    return stripped


def guard_settlement_date(
    settlement_date: date,
    *,
    max_past_days: int = 365,
) -> date:
    """Validate that a settlement date is not in the future.

    Args:
        settlement_date: The date to validate.
        max_past_days: Maximum age in days (default: 1 year).

    Returns:
        The validated settlement date.

    Raises:
        ValueError: If date is future or too far in the past.

    Example:
        >>> from datetime import date
        >>> guard_settlement_date(date.today())
        date(2026, 2, 12)

    """
    if not isinstance(settlement_date, date):
        msg = f"Settlement date must be a date object, got: {type(settlement_date).__name__}"
        raise ValueError(msg)

    today = date.today()

    if settlement_date > today:
        msg = f"Settlement date cannot be in the future: {settlement_date} > {today}"
        raise ValueError(msg)

    days_diff = (today - settlement_date).days
    if days_diff > max_past_days:
        msg = (
            f"Settlement date is too old: {settlement_date} "
            f"({days_diff} days ago, max {max_past_days})"
        )
        raise ValueError(msg)

    return settlement_date


def guard_idempotency_key(key: str) -> str:
    """Validate an idempotency key as a valid UUID v4.

    Args:
        key: String representation of a UUID v4.

    Returns:
        The validated UUID string (lowercase, canonical format).

    Raises:
        ValueError: If key is not a valid UUID.

    Example:
        >>> guard_idempotency_key("550e8400-e29b-41d4-a716-446655440000")
        '550e8400-e29b-41d4-a716-446655440000'

    """
    if not key or not isinstance(key, str):
        msg = "Idempotency key cannot be empty"
        raise ValueError(msg)

    try:
        parsed = UUID(key.strip())
    except ValueError as e:
        msg = f"Invalid UUID format for idempotency key: {key}"
        raise ValueError(msg) from e

    return str(parsed)
