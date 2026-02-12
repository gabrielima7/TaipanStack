"""Tests for Ingestion Pipeline."""

from unittest.mock import patch, MagicMock
from decimal import Decimal
from invario.ingestion.pipeline import ingest_file, IngestionError
from invario.domain.transaction import Transaction, TransactionType
from taipanstack.core.result import Ok, Err


def test_ingest_pipeline_success():
    """Test full pipeline success."""
    # Mock the parser to return a valid transaction
    tx = MagicMock(spec=Transaction)
    tx.amount = Decimal("100")
    tx.currency = "BRL"
    tx.bank_code = "001"
    # Needs to pass guards

    with patch("invario.ingestion.pipeline.parse_csv_file") as mock_parse:
        mock_parse.return_value = Ok([tx])

        result = ingest_file("test.csv", "content")

        assert isinstance(result, Ok)
        assert len(result.unwrap()) == 1


def test_ingest_pipeline_guard_failure():
    """Test that financial guard failure rejects the batch."""
    # Transaction with invalid currency
    tx = MagicMock(spec=Transaction)
    tx.amount = Decimal("100")
    tx.currency = "INVALID" # Guard should catch this
    tx.bank_code = "001"

    with patch("invario.ingestion.pipeline.parse_csv_file") as mock_parse:
        mock_parse.return_value = Ok([tx])

        result = ingest_file("test.csv", "content")

        assert isinstance(result, Err)
        assert "Validation failed" in str(result.unwrap_err())


def test_ingest_pipeline_extension_failure():
    """Test that invalid extension is rejected early."""
    result = ingest_file("test.exe", "content")
    assert isinstance(result, Err)
    assert "SecurityError" in str(result.unwrap_err()) or "extension" in str(result.unwrap_err())
