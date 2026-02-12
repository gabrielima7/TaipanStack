"""
Ingestion pipeline orchestrator for Invario.

Detects file format, dispatches to the correct parser,
applies financial guards, and returns validated transactions.
Uses collect_results for all-or-nothing batch semantics.
"""

from __future__ import annotations

from pathlib import Path

from taipanstack.core.result import Err, Ok, Result, collect_results
from taipanstack.security.guards import guard_file_extension

from invario.domain.transaction import Transaction
from invario.guards.financial import (
    guard_bank_code,
    guard_currency_code,
    guard_positive_amount,
)
from invario.ingestion.parsers.cnab import CnabParseError, parse_cnab_file
from invario.ingestion.parsers.csv_parser import CsvParseError, parse_csv_file
from invario.ingestion.parsers.json_parser import JsonParseError, parse_json_file


class IngestionError(Exception):
    """Raised when the ingestion pipeline fails.

    Attributes:
        reason: Specific reason for the failure.
        filename: Name of the file that caused the error.

    """

    def __init__(
        self,
        reason: str,
        *,
        filename: str = "",
    ) -> None:
        """Initialize IngestionError."""
        self.reason = reason
        self.filename = filename
        ctx = f" ({filename})" if filename else ""
        super().__init__(f"Ingestion error{ctx}: {reason}")


# Supported file extensions
ALLOWED_EXTENSIONS: list[str] = ["cnab", "rem", "ret", "csv", "json"]


def _detect_format(filename: str, content: str) -> str:
    """Detect file format from extension or content.

    Args:
        filename: Name of the file.
        content: File content for heuristic detection.

    Returns:
        Detected format string: 'cnab', 'csv', or 'json'.

    Raises:
        ValueError: If format cannot be determined.

    """
    ext = Path(filename).suffix.lower().lstrip(".")

    if ext in ("cnab", "rem", "ret"):
        return "cnab"
    if ext == "csv":
        return "csv"
    if ext == "json":
        return "json"

    # Content-based heuristic
    stripped = content.strip()
    if stripped.startswith(("{", "[")):
        return "json"

    # Check if first line is at least 240 chars (CNAB)
    first_line = stripped.split("\n", maxsplit=1)[0]
    if len(first_line) >= 240:
        return "cnab"

    # Default to CSV as most permissive
    if "," in first_line or ";" in first_line:
        return "csv"

    msg = f"Cannot determine file format for: {filename}"
    raise ValueError(msg)


def _validate_transaction(
    tx: Transaction,
) -> Result[Transaction, Exception]:
    """Apply financial guards to a parsed transaction.

    Args:
        tx: Transaction to validate.

    Returns:
        Ok(Transaction) if all guards pass, Err on first failure.

    """
    try:
        guard_positive_amount(tx.amount)
        guard_currency_code(tx.currency)
        guard_bank_code(tx.bank_code)
        return Ok(tx)
    except ValueError as e:
        return Err(e)


def ingest_file(
    filename: str,
    content: str,
) -> Result[list[Transaction], IngestionError]:
    """Ingest a financial file through the full pipeline.

    Pipeline stages:
    1. Validate file extension
    2. Detect format (CNAB/CSV/JSON)
    3. Parse with format-specific parser
    4. Apply financial guards to each transaction
    5. Return validated batch (all-or-nothing)

    Args:
        filename: Name of the file being ingested.
        content: Full file content as string.

    Returns:
        Ok(list[Transaction]) if entire batch is valid.
        Err(IngestionError) on any failure.

    """
    # Stage 1: Validate extension
    try:
        guard_file_extension(
            filename,
            allowed_extensions=ALLOWED_EXTENSIONS,
        )
    except Exception as e:
        return Err(IngestionError(str(e), filename=filename))

    # Stage 2: Detect format
    try:
        file_format = _detect_format(filename, content)
    except ValueError as e:
        return Err(IngestionError(str(e), filename=filename))

    # Stage 3: Parse
    parse_result: Result[list[Transaction], Exception]

    if file_format == "cnab":
        parse_result = parse_cnab_file(content)
    elif file_format == "csv":
        parse_result = parse_csv_file(content)
    elif file_format == "json":
        parse_result = parse_json_file(content)
    else:
        return Err(IngestionError(
            f"Unsupported format: {file_format}",
            filename=filename,
        ))

    # Unwrap parse result
    match parse_result:
        case Err(error):
            return Err(IngestionError(str(error), filename=filename))
        case Ok(transactions):
            pass

    # Stage 4: Apply financial guards to each transaction
    validated_results = [_validate_transaction(tx) for tx in transactions]
    validated_batch = collect_results(validated_results)

    match validated_batch:
        case Err(error):
            return Err(IngestionError(
                f"Validation failed: {error}",
                filename=filename,
            ))
        case Ok(valid_transactions):
            return Ok(valid_transactions)
