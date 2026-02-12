"""Tests for CSV Ingestion."""

from datetime import date
from decimal import Decimal

from invario.ingestion.parsers.csv_parser import parse_csv_file
from taipanstack.core.result import Err, Ok


def test_parse_csv_success():
    """Test parsing valid CSV."""
    content = """type,amount,currency,source_account,target_account,document,settlement_date,bank_code
credit,100.50,BRL,123,456,12345678901,2025-01-01,001
debit,50.00,USD,123,789,12345678901,02/01/2025,001"""

    result = parse_csv_file(content)
    assert isinstance(result, Ok)
    txs = result.unwrap()

    assert len(txs) == 2
    assert txs[0].amount == Decimal("100.50")
    assert txs[0].settlement_date == date(2025, 1, 1)

    assert txs[1].amount == Decimal("50.00")
    assert txs[1].settlement_date == date(2025, 1, 2)  # DD/MM/YYYY handled


def test_parse_csv_missing_columns():
    """Test failure on missing columns."""
    content = """amount,currency\n100,BRL"""
    result = parse_csv_file(content)
    assert isinstance(result, Err)
    assert "Missing required columns" in str(result.unwrap_err())


def test_parse_csv_invalid_amount():
    """Test failure on invalid amount propagates as Err."""
    content = """type,amount,currency,source_account,target_account,document,settlement_date,bank_code
credit,NOT_A_NUMBER,BRL,123,456,DOC,2025-01-01,001"""

    result = parse_csv_file(content)
    assert isinstance(result, Err)
    assert "Invalid amount" in str(result.unwrap_err())
