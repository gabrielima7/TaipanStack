"""
Transaction domain model for Invario.

Immutable, hashable representation of a financial transaction.
All monetary values use Decimal for precision — never float.
"""

from __future__ import annotations

import hashlib
from datetime import date
from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TransactionType(str, Enum):
    """Types of financial transactions."""

    CREDIT = "credit"
    DEBIT = "debit"
    TRANSFER = "transfer"


class Transaction(BaseModel):
    """Immutable financial transaction.

    Attributes:
        id: Unique transaction identifier.
        type: Transaction type (credit, debit, transfer).
        amount: Monetary value (must be > 0, validated by guards).
        currency: ISO 4217 currency code (e.g., BRL, USD).
        source_account: Source account identifier.
        target_account: Target account identifier.
        document: CPF or CNPJ of the involved party.
        settlement_date: Date of settlement.
        description: Human-readable description.
        idempotency_key: UUID to prevent duplicate processing.
        bank_code: COMPE (3 digits) or ISPB (8 digits) code.
        raw_line: Original raw data line (for audit trail).

    """

    id: UUID
    type: TransactionType
    amount: Decimal = Field(gt=0, decimal_places=2)
    currency: str = Field(min_length=3, max_length=3)
    source_account: str
    target_account: str
    document: str
    settlement_date: date
    description: str = ""
    idempotency_key: UUID
    bank_code: str
    raw_line: str = ""

    model_config = ConfigDict(frozen=True)

    def content_hash(self) -> str:
        """Generate SHA-256 hash of transaction content.

        Used for integrity verification and deduplication.
        Excludes raw_line and description (metadata only).

        Returns:
            Hex-encoded SHA-256 hash string.

        """
        content = (
            f"{self.id}|{self.type.value}|{self.amount}|{self.currency}|"
            f"{self.source_account}|{self.target_account}|{self.document}|"
            f"{self.settlement_date.isoformat()}|{self.idempotency_key}|"
            f"{self.bank_code}"
        )
        return hashlib.sha256(content.encode("utf-8")).hexdigest()
