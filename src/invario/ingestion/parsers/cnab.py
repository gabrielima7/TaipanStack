"""
CNAB file parser for Invario.

Parses CNAB 240 and CNAB 400 banking file formats into
Transaction domain models using Railway Oriented Programming.
Every parsing operation returns Result[T, Exception].
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from taipanstack.core.result import Err, Ok, Result, safe

from invario.domain.transaction import Transaction, TransactionType


class CnabParseError(Exception):
    """Raised when CNAB line parsing fails.

    Attributes:
        line_number: Line number in the file.
        raw_line: The original line content.
        reason: Specific reason for the failure.

    """

    def __init__(
        self,
        reason: str,
        *,
        line_number: int = 0,
        raw_line: str = "",
    ) -> None:
        """Initialize CnabParseError."""
        self.line_number = line_number
        self.raw_line = raw_line[:100]  # Truncate for safety
        self.reason = reason
        super().__init__(
            f"CNAB parse error at line {line_number}: {reason}"
        )


# CNAB 240 segment positions (0-indexed)
CNAB240_LINE_LENGTH = 240
CNAB240_SEGMENT_TYPE_POS = 13
CNAB240_RECORD_TYPE_POS = 7
CNAB240_BANK_CODE_START = 0
CNAB240_BANK_CODE_END = 3

# CNAB 400 segment positions
CNAB400_LINE_LENGTH = 400
CNAB400_RECORD_TYPE_POS = 0


def _parse_cnab_date(date_str: str) -> date:
    """Parse CNAB date format (DDMMYYYY) to date object.

    Args:
        date_str: Date string in DDMMYYYY format.

    Returns:
        Parsed date object.

    Raises:
        ValueError: If date format is invalid.

    """
    if len(date_str) != 8 or not date_str.isdigit():
        msg = f"Invalid CNAB date format: {date_str!r}. Expected DDMMYYYY"
        raise ValueError(msg)

    day = int(date_str[0:2])
    month = int(date_str[2:4])
    year = int(date_str[4:8])

    return date(year, month, day)


def _parse_cnab_amount(amount_str: str) -> Decimal:
    """Parse CNAB amount (last 2 digits are cents).

    Args:
        amount_str: Amount string with implicit 2 decimal places.

    Returns:
        Parsed Decimal amount.

    Raises:
        ValueError: If amount format is invalid.

    """
    if not amount_str.isdigit():
        msg = f"Invalid CNAB amount format: {amount_str!r}"
        raise ValueError(msg)

    cents = int(amount_str)
    return Decimal(cents) / Decimal(100)


def parse_cnab240_detail(
    line: str,
    *,
    line_number: int = 0,
) -> Result[Transaction, CnabParseError]:
    """Parse a single CNAB 240 detail segment (segment 'A' or 'J').

    Args:
        line: Raw CNAB 240 line (240 characters).
        line_number: Line number for error reporting.

    Returns:
        Ok(Transaction) on success, Err(CnabParseError) on failure.

    """
    if len(line) != CNAB240_LINE_LENGTH:
        return Err(CnabParseError(
            f"Line length must be {CNAB240_LINE_LENGTH}, got {len(line)}",
            line_number=line_number,
            raw_line=line,
        ))

    try:
        record_type = line[CNAB240_RECORD_TYPE_POS]

        # Only process detail records (type '3')
        if record_type != "3":
            return Err(CnabParseError(
                f"Not a detail record (type {record_type!r}), skipping",
                line_number=line_number,
                raw_line=line,
            ))

        bank_code = line[CNAB240_BANK_CODE_START:CNAB240_BANK_CODE_END]
        segment_type = line[CNAB240_SEGMENT_TYPE_POS]

        # Parse Segment A (payment details)
        if segment_type == "A":
            return _parse_segment_a(line, bank_code=bank_code, line_number=line_number)

        # Parse Segment J (boleto details)
        if segment_type == "J":
            return _parse_segment_j(line, bank_code=bank_code, line_number=line_number)

        return Err(CnabParseError(
            f"Unsupported segment type: {segment_type!r}",
            line_number=line_number,
            raw_line=line,
        ))

    except (ValueError, IndexError) as e:
        return Err(CnabParseError(
            str(e),
            line_number=line_number,
            raw_line=line,
        ))


def _parse_segment_a(
    line: str,
    *,
    bank_code: str,
    line_number: int,
) -> Result[Transaction, CnabParseError]:
    """Parse CNAB 240 Segment A (credit/payment transfer)."""
    try:
        # Segment A field positions (FEBRABAN standard)
        target_bank = line[17:20]
        target_account = line[20:33].strip()
        source_account = line[58:71].strip()
        settlement_date = _parse_cnab_date(line[93:101])
        amount = _parse_cnab_amount(line[119:134].strip())
        document = line[134:148].strip()
        description = line[177:217].strip()

        # Determine transaction type
        tx_type = TransactionType.TRANSFER

        transaction = Transaction(
            id=uuid4(),
            type=tx_type,
            amount=amount,
            currency="BRL",
            source_account=source_account,
            target_account=f"{target_bank}-{target_account}",
            document=document if document else "00000000000",
            settlement_date=settlement_date,
            description=description,
            idempotency_key=uuid4(),
            bank_code=bank_code,
            raw_line=line,
        )
        return Ok(transaction)

    except (ValueError, IndexError) as e:
        return Err(CnabParseError(
            f"Segment A parse error: {e}",
            line_number=line_number,
            raw_line=line,
        ))


def _parse_segment_j(
    line: str,
    *,
    bank_code: str,
    line_number: int,
) -> Result[Transaction, CnabParseError]:
    """Parse CNAB 240 Segment J (boleto/payment slip)."""
    try:
        # Segment J field positions
        barcode = line[17:61].strip()
        target_account = barcode[:10] if barcode else "0000000000"
        settlement_date = _parse_cnab_date(line[91:99])
        amount = _parse_cnab_amount(line[99:114].strip())
        document = line[114:128].strip()
        description = line[140:180].strip()

        transaction = Transaction(
            id=uuid4(),
            type=TransactionType.DEBIT,
            amount=amount,
            currency="BRL",
            source_account="boleto",
            target_account=target_account,
            document=document if document else "00000000000",
            settlement_date=settlement_date,
            description=description,
            idempotency_key=uuid4(),
            bank_code=bank_code,
            raw_line=line,
        )
        return Ok(transaction)

    except (ValueError, IndexError) as e:
        return Err(CnabParseError(
            f"Segment J parse error: {e}",
            line_number=line_number,
            raw_line=line,
        ))


def parse_cnab_file(
    content: str,
) -> Result[list[Transaction], CnabParseError]:
    """Parse an entire CNAB file into a list of transactions.

    Determines format (240 or 400) from line length and parses
    all detail records. Uses all-or-nothing semantics: if any
    line fails, the entire batch is rejected.

    Args:
        content: Full file content as string.

    Returns:
        Ok(list[Transaction]) if all lines valid, Err on first failure.

    """
    lines = content.splitlines()

    if not lines:
        return Err(CnabParseError("Empty CNAB file", line_number=0))

    # Determine format from first line length
    first_line_len = len(lines[0])
    transactions: list[Transaction] = []

    for i, line in enumerate(lines, start=1):
        stripped = line.rstrip("\n\r")
        if not stripped:
            continue

        if first_line_len == CNAB240_LINE_LENGTH or len(stripped) == CNAB240_LINE_LENGTH:
            result = parse_cnab240_detail(stripped, line_number=i)
        else:
            # CNAB 400 not fully implemented yet — reject gracefully
            return Err(CnabParseError(
                f"CNAB 400 format not yet supported (line length: {len(stripped)})",
                line_number=i,
                raw_line=stripped,
            ))

        match result:
            case Ok(tx):
                transactions.append(tx)
            case Err(error):
                # Non-detail lines produce non-fatal errors; skip them
                if "Not a detail record" in str(error):
                    continue
                # Real parse errors are fatal
                return Err(error)

    if not transactions:
        return Err(CnabParseError(
            "No valid transactions found in CNAB file",
            line_number=0,
        ))

    return Ok(transactions)
