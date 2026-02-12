"""
CSV parser for financial data in Invario.

Parses CSV files with financial transactions using Pydantic
schema validation. Returns Result types for Railway pattern.
"""

from __future__ import annotations

import csv
import io
from datetime import date
from decimal import Decimal, InvalidOperation
from uuid import NAMESPACE_OID, UUID, uuid4, uuid5

from taipanstack.core.result import Err, Ok, Result

from invario.domain.transaction import Transaction, TransactionType


class CsvParseError(Exception):
    """Raised when CSV parsing fails.

    Attributes:
        row_number: Row number in the CSV file.
        reason: Specific reason for the failure.

    """

    def __init__(
        self,
        reason: str,
        *,
        row_number: int = 0,
    ) -> None:
        """Initialize CsvParseError."""
        self.row_number = row_number
        self.reason = reason
        super().__init__(
            f"CSV parse error at row {row_number}: {reason}"
        )


# Required columns in the financial CSV
REQUIRED_COLUMNS: frozenset[str] = frozenset({
    "type",
    "amount",
    "currency",
    "source_account",
    "target_account",
    "document",
    "settlement_date",
    "bank_code",
})

# Map of CSV type values to TransactionType
TYPE_MAP: dict[str, TransactionType] = {
    "credit": TransactionType.CREDIT,
    "debit": TransactionType.DEBIT,
    "transfer": TransactionType.TRANSFER,
    "c": TransactionType.CREDIT,
    "d": TransactionType.DEBIT,
    "t": TransactionType.TRANSFER,
}


def _parse_csv_date(date_str: str) -> date:
    """Parse CSV date in YYYY-MM-DD or DD/MM/YYYY format.

    Args:
        date_str: Date string.

    Returns:
        Parsed date object.

    Raises:
        ValueError: If format is invalid.

    """
    # Try ISO format first (YYYY-MM-DD)
    if "-" in date_str and len(date_str) == 10:
        return date.fromisoformat(date_str)

    # Try Brazilian format (DD/MM/YYYY)
    if "/" in date_str:
        parts = date_str.split("/")
        if len(parts) == 3:
            day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
            return date(year, month, day)

    msg = f"Unknown date format: {date_str!r}. Expected YYYY-MM-DD or DD/MM/YYYY"
    raise ValueError(msg)


def _parse_csv_row(
    row: dict[str, str],
    row_number: int,
) -> Result[Transaction, CsvParseError]:
    """Parse a single CSV row into a Transaction.

    Args:
        row: Dictionary from csv.DictReader.
        row_number: Row number for error reporting.

    Returns:
        Ok(Transaction) on success, Err(CsvParseError) on failure.

    """
    try:
        # Validate required columns
        missing = REQUIRED_COLUMNS - set(row.keys())
        if missing:
            return Err(CsvParseError(
                f"Missing required columns: {', '.join(sorted(missing))}",
                row_number=row_number,
            ))

        # Parse transaction type
        type_str = row["type"].strip().lower()
        if type_str not in TYPE_MAP:
            return Err(CsvParseError(
                f"Invalid transaction type: {type_str!r}. "
                f"Expected: {', '.join(sorted(TYPE_MAP.keys()))}",
                row_number=row_number,
            ))

        # Parse amount
        try:
            amount = Decimal(row["amount"].strip())
        except InvalidOperation:
            return Err(CsvParseError(
                f"Invalid amount: {row['amount']!r}",
                row_number=row_number,
            ))

        if amount <= 0:
            return Err(CsvParseError(
                f"Amount must be positive: {amount}",
                row_number=row_number,
            ))

        # Parse date
        try:
            settlement_date = _parse_csv_date(row["settlement_date"].strip())
        except ValueError as e:
            return Err(CsvParseError(
                str(e),
                row_number=row_number,
            ))

        # Parse optional fields
        description = row.get("description", "").strip()
        idempotency_key_str = row.get("idempotency_key", "").strip()

        if idempotency_key_str:
            try:
                idempotency_key = UUID(idempotency_key_str)
            except ValueError:
                return Err(CsvParseError(
                    f"Invalid idempotency_key UUID: {idempotency_key_str!r}",
                    row_number=row_number,
                ))
        else:
            # Deterministic idempotency key based on content if not provided
            content_str = ",".join(f"{k}:{v}" for k, v in sorted(row.items()))
            idempotency_key = uuid5(NAMESPACE_OID, f"idem:{content_str}")

        # Deterministic Transaction ID based on content
        # Note: If idempotency_key is provided by user, it contributes to uniqueness.
        # If generated, it derives from content.
        # We include everything in the ID generation to ensure content-based deduplication matches.
        full_content_str = ",".join(f"{k}:{v}" for k, v in sorted(row.items()))
        tx_id = uuid5(NAMESPACE_OID, f"tx:{full_content_str}")

        transaction = Transaction(
            id=tx_id,
            type=TYPE_MAP[type_str],
            amount=amount,
            currency=row["currency"].strip().upper(),
            source_account=row["source_account"].strip(),
            target_account=row["target_account"].strip(),
            document=row["document"].strip(),
            settlement_date=settlement_date,
            description=description,
            idempotency_key=idempotency_key,
            bank_code=row["bank_code"].strip(),
            raw_line=str(row),
        )
        return Ok(transaction)

    except Exception as e:
        return Err(CsvParseError(
            f"Unexpected error: {e}",
            row_number=row_number,
        ))


def parse_csv_file(
    content: str,
    *,
    delimiter: str = ",",
) -> Result[list[Transaction], CsvParseError]:
    """Parse a CSV file into a list of transactions.

    Uses all-or-nothing semantics: one invalid row rejects the batch.

    Args:
        content: Full CSV content as string (with header row).
        delimiter: CSV delimiter character (default: comma).

    Returns:
        Ok(list[Transaction]) if all rows valid, Err on first failure.

    """
    if not content.strip():
        return Err(CsvParseError("Empty CSV file", row_number=0))

    reader = csv.DictReader(io.StringIO(content), delimiter=delimiter)

    # Validate header
    if reader.fieldnames is None:
        return Err(CsvParseError("CSV has no header row", row_number=0))

    field_set = frozenset(f.strip().lower() for f in reader.fieldnames)
    missing = REQUIRED_COLUMNS - field_set
    if missing:
        return Err(CsvParseError(
            f"Missing required columns in header: {', '.join(sorted(missing))}",
            row_number=0,
        ))

    transactions: list[Transaction] = []

    for i, row in enumerate(reader, start=2):  # Row 1 is header
        # Normalize keys to lowercase
        normalized = {k.strip().lower(): v for k, v in row.items() if k is not None}
        result = _parse_csv_row(normalized, row_number=i)

        match result:
            case Ok(tx):
                transactions.append(tx)
            case Err() as err:
                return err  # All-or-nothing: first error rejects batch

    if not transactions:
        return Err(CsvParseError("No data rows in CSV file", row_number=0))

    return Ok(transactions)
