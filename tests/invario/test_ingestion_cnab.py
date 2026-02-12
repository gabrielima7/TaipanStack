"""Tests for CNAB Ingestion."""

from datetime import date
from decimal import Decimal

from invario.domain.transaction import TransactionType
from invario.ingestion.parsers.cnab import (
    CNAB240_LINE_LENGTH,
    parse_cnab_file,
    parse_cnab240_detail,
)
from taipanstack.core.result import Err, Ok


def test_parse_cnab240_segment_a_success():
    """Test parsing a valid CNAB 240 Segment A line."""
    # Construct a valid line (240 chars)
    # Bank: 001
    # Type: 3 (Detail)
    # Segment: A (Pos 13)
    # Amount: 10000 (100.00) at 119-134
    # Date: 01012025 at 93-101

    line = list(" " * CNAB240_LINE_LENGTH)
    line[0:3] = list("001")        # Bank
    line[7] = "3"                  # Type 3 (Detail)
    line[13] = "A"                 # Segment A
    # Target Bank 237 at 17:20
    line[17:20] = list("237")
    # Date 01012025 at 93:101
    line[93:101] = list("01012025")
    # Amount 10000 at 119:134
    line[119:134] = list("000000000010000")

    raw_line = "".join(line)

    result = parse_cnab240_detail(raw_line)
    assert isinstance(result, Ok)
    tx = result.unwrap()

    assert tx.amount == Decimal("100.00")
    assert tx.settlement_date == date(2025, 1, 1)
    assert tx.type == TransactionType.TRANSFER
    assert tx.bank_code == "001"


def test_parse_cnab_file_success():
    """Test parsing a full CNAB file with multiple lines."""
    # Create two valid lines
    line1 = list(" " * CNAB240_LINE_LENGTH)
    line1[0:3] = list("001"); line1[7]="3"; line1[13]="A"
    line1[93:101] = list("01012025"); line1[119:134] = list("000000000010000") # 100.00

    line2 = list(" " * CNAB240_LINE_LENGTH)
    line2[0:3] = list("001"); line2[7]="3"; line2[13]="A"
    line2[93:101] = list("02012025"); line2[119:134] = list("000000000020000") # 200.00

    content = "".join(line1) + "\n" + "".join(line2)

    result = parse_cnab_file(content)
    assert isinstance(result, Ok)
    transactions = result.unwrap()

    assert len(transactions) == 2
    assert transactions[0].amount == Decimal("100.00")
    assert transactions[1].amount == Decimal("200.00")


def test_parse_cnab_file_failure_bad_length():
    """Test that implicit all-or-nothing fails on bad line length."""
    line1 = " " * CNAB240_LINE_LENGTH
    line2 = "Short line"

    content = line1 + "\n" + line2

    result = parse_cnab_file(content)
    assert isinstance(result, Err)
    # Should report line 2 failure
    assert "line 2" in str(result.unwrap_err())
