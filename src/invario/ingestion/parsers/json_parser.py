"""
JSON parser for financial data in Invario.

Parses JSON transaction files using orjson for high-performance
deserialization. Returns Result types for Railway pattern.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any
from uuid import UUID, uuid4

import orjson

from taipanstack.core.result import Err, Ok, Result

from invario.domain.transaction import Transaction, TransactionType


class JsonParseError(Exception):
    """Raised when JSON parsing fails.

    Attributes:
        reason: Specific reason for the failure.
        index: Index of the transaction in the array (if applicable).

    """

    def __init__(
        self,
        reason: str,
        *,
        index: int = -1,
    ) -> None:
        """Initialize JsonParseError."""
        self.reason = reason
        self.index = index
        ctx = f" at index {index}" if index >= 0 else ""
        super().__init__(f"JSON parse error{ctx}: {reason}")


# Map of JSON type values to TransactionType
_TYPE_MAP: dict[str, TransactionType] = {
    "credit": TransactionType.CREDIT,
    "debit": TransactionType.DEBIT,
    "transfer": TransactionType.TRANSFER,
}


def _parse_json_transaction(
    data: dict[str, Any],
    index: int,
) -> Result[Transaction, JsonParseError]:
    """Parse a single JSON object into a Transaction.

    Args:
        data: Dictionary from JSON parsing.
        index: Index for error reporting.

    Returns:
        Ok(Transaction) on success, Err(JsonParseError) on failure.

    """
    required_fields = {
        "type", "amount", "currency", "source_account",
        "target_account", "document", "settlement_date", "bank_code",
    }

    missing = required_fields - set(data.keys())
    if missing:
        return Err(JsonParseError(
            f"Missing required fields: {', '.join(sorted(missing))}",
            index=index,
        ))

    try:
        # Parse type
        type_str = str(data["type"]).lower()
        if type_str not in _TYPE_MAP:
            return Err(JsonParseError(
                f"Invalid transaction type: {type_str!r}",
                index=index,
            ))

        # Parse amount
        try:
            amount = Decimal(str(data["amount"]))
        except InvalidOperation:
            return Err(JsonParseError(
                f"Invalid amount: {data['amount']!r}",
                index=index,
            ))

        if amount <= 0:
            return Err(JsonParseError(
                f"Amount must be positive: {amount}",
                index=index,
            ))

        # Parse date
        try:
            settlement_date = date.fromisoformat(str(data["settlement_date"]))
        except ValueError:
            return Err(JsonParseError(
                f"Invalid date format: {data['settlement_date']!r}. Expected YYYY-MM-DD",
                index=index,
            ))

        # Optional fields
        description = str(data.get("description", ""))
        id_key = data.get("idempotency_key", "")
        tx_id_str = data.get("id", "")

        if id_key:
            try:
                idempotency_key = UUID(str(id_key))
            except ValueError:
                return Err(JsonParseError(
                    f"Invalid idempotency_key UUID: {id_key!r}",
                    index=index,
                ))
        else:
            idempotency_key = uuid4()

        if tx_id_str:
            try:
                tx_id = UUID(str(tx_id_str))
            except ValueError:
                tx_id = uuid4()
        else:
            tx_id = uuid4()

        transaction = Transaction(
            id=tx_id,
            type=_TYPE_MAP[type_str],
            amount=amount,
            currency=str(data["currency"]).upper(),
            source_account=str(data["source_account"]),
            target_account=str(data["target_account"]),
            document=str(data["document"]),
            settlement_date=settlement_date,
            description=description,
            idempotency_key=idempotency_key,
            bank_code=str(data["bank_code"]),
            raw_line=orjson.dumps(data).decode("utf-8"),
        )
        return Ok(transaction)

    except Exception as e:
        return Err(JsonParseError(
            f"Unexpected error: {e}",
            index=index,
        ))


def parse_json_file(
    content: str | bytes,
) -> Result[list[Transaction], JsonParseError]:
    """Parse a JSON file into a list of transactions.

    Accepts either a JSON array of transaction objects or a single
    object with a "transactions" key. Uses orjson for performance.
    All-or-nothing batch semantics.

    Args:
        content: JSON content as string or bytes.

    Returns:
        Ok(list[Transaction]) if all valid, Err on first failure.

    """
    if not content:
        return Err(JsonParseError("Empty JSON content"))

    try:
        raw = content.encode("utf-8") if isinstance(content, str) else content
        parsed = orjson.loads(raw)
    except orjson.JSONDecodeError as e:
        return Err(JsonParseError(f"Invalid JSON: {e}"))

    # Handle both formats: [] or {"transactions": []}
    if isinstance(parsed, list):
        items = parsed
    elif isinstance(parsed, dict) and "transactions" in parsed:
        items = parsed["transactions"]
        if not isinstance(items, list):
            return Err(JsonParseError(
                "'transactions' field must be an array"
            ))
    else:
        return Err(JsonParseError(
            "Expected a JSON array or object with 'transactions' key"
        ))

    if not items:
        return Err(JsonParseError("No transactions in JSON data"))

    transactions: list[Transaction] = []

    for i, item in enumerate(items):
        if not isinstance(item, dict):
            return Err(JsonParseError(
                f"Transaction must be a JSON object, got {type(item).__name__}",
                index=i,
            ))

        result = _parse_json_transaction(item, index=i)

        match result:
            case Ok(tx):
                transactions.append(tx)
            case Err() as err:
                return err  # All-or-nothing

    return Ok(transactions)
