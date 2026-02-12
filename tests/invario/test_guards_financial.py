"""Tests for Financial Guards."""

from datetime import date, timedelta
from decimal import Decimal

import pytest
from invario.guards.financial import (
    guard_bank_code,
    guard_cpf_cnpj,
    guard_currency_code,
    guard_idempotency_key,
    guard_positive_amount,
    guard_settlement_date,
)


def test_guard_positive_amount():
    """Test amount validation."""
    assert guard_positive_amount(Decimal("10.00")) == Decimal("10.00")
    assert guard_positive_amount("10.50") == Decimal("10.50")
    assert guard_positive_amount(100) == Decimal("100")

    with pytest.raises(ValueError, match="Amount must be positive"):
        guard_positive_amount(0)

    with pytest.raises(ValueError, match="Amount must be positive"):
        guard_positive_amount(-5)

    with pytest.raises(ValueError, match="too many decimal places"):
        guard_positive_amount("10.123")  # Max 2 decimals


def test_guard_currency_code():
    """Test ISO 4217 currency code validation."""
    assert guard_currency_code("BRL") == "BRL"
    assert guard_currency_code("usd ") == "USD"

    with pytest.raises(ValueError, match="Invalid ISO 4217"):
        guard_currency_code("XYZ")

    with pytest.raises(ValueError, match="must be 3 characters"):
        guard_currency_code("BR")


def test_guard_cpf_cnpj():
    """Test CPF/CNPJ validation."""
    # Valid CPF (generated)
    valid_cpf = "52998224725"
    assert guard_cpf_cnpj(valid_cpf) == valid_cpf
    assert guard_cpf_cnpj("529.982.247-25") == valid_cpf

    # Identical digits
    with pytest.raises(ValueError, match="Document cannot be all identical digits"):
        guard_cpf_cnpj("11111111111")

    # Invalid digits (checksum)
    with pytest.raises(ValueError, match="Invalid CPF check digits"):
        guard_cpf_cnpj("12345678900")  # Invalid checksum


def test_guard_bank_code():
    """Test bank code validation (COMPE/ISPB)."""
    assert guard_bank_code("001") == "001"
    assert guard_bank_code("12345678") == "12345678"

    with pytest.raises(ValueError, match="must be 3.*or 8"):
        guard_bank_code("12")

    with pytest.raises(ValueError, match="must be 3.*or 8"):
        guard_bank_code("1234")


def test_guard_settlement_date():
    """Test settlement date validation."""
    today = date.today()
    assert guard_settlement_date(today) == today

    future = today + timedelta(days=1)
    with pytest.raises(ValueError, match="cannot be in the future"):
        guard_settlement_date(future)

    old = today - timedelta(days=400)
    with pytest.raises(ValueError, match="is too old"):
        guard_settlement_date(old)


def test_guard_idempotency_key():
    """Test UUID validation."""
    valid_uuid = "550e8400-e29b-41d4-a716-446655440000"
    assert guard_idempotency_key(valid_uuid) == valid_uuid

    with pytest.raises(ValueError, match="Invalid UUID"):
        guard_idempotency_key("not-a-uuid")
