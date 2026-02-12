"""Tests for JSON Ingestion."""

import orjson
from decimal import Decimal
from datetime import date
from invario.ingestion.parsers.json_parser import parse_json_file
from taipanstack.core.result import Ok, Err


def test_parse_json_list_success():
    """Test parsing a JSON array of transactions."""
    data = [
        {
            "type": "credit",
            "amount": "100.50",
            "currency": "BRL",
            "source_account": "123",
            "target_account": "456",
            "document": "DOC",
            "settlement_date": "2025-01-01",
            "bank_code": "001"
        }
    ]
    content = orjson.dumps(data)

    result = parse_json_file(content)
    assert isinstance(result, Ok)
    txs = result.unwrap()
    assert len(txs) == 1
    assert txs[0].amount == Decimal("100.50")


def test_parse_json_object_success():
    """Test parsing a JSON object with 'transactions' key."""
    data = {
        "transactions": [
            {
                "type": "debit",
                "amount": 50,
                "currency": "USD",
                "source_account": "A",
                "target_account": "B",
                "document": "D",
                "settlement_date": "2025-01-02",
                "bank_code": "002"
            }
        ]
    }
    content = orjson.dumps(data)

    result = parse_json_file(content)
    assert isinstance(result, Ok)
    txs = result.unwrap()
    assert txs[0].amount == Decimal("50")


def test_parse_json_invalid_format():
    """Test failure on invalid JSON structure."""
    content = b'{"not": "valid"}'
    result = parse_json_file(content)
    assert isinstance(result, Err)
    assert "Expected a JSON array" in str(result.unwrap_err())
