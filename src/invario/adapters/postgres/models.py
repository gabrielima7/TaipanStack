"""
SQLAlchemy models for Invario persistence.

Defines the schema for Transactions, LedgerEntries, and the LedgerHead
singleton used for concurrency control.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    Uuid,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""


class TransactionModel(Base):
    """Persistence model for Financial Transactions.

    Stores the immutable transaction data.
    ID is the primary key.
    Content hash is indexed for preventing duplicates.
    """

    __tablename__ = "transactions"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    source_account: Mapped[str] = mapped_column(String(50), nullable=False)
    target_account: Mapped[str] = mapped_column(String(50), nullable=False)
    document: Mapped[str] = mapped_column(String(20), nullable=False)
    settlement_date: Mapped[date] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    idempotency_key: Mapped[UUID] = mapped_column(Uuid, unique=True, nullable=False)
    bank_code: Mapped[str] = mapped_column(String(10), nullable=False)
    raw_line: Mapped[str] = mapped_column(Text, default="", nullable=False)

    # SHA-256 content hash for deduplication
    content_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)

    # Relationship to ledger entry (one-to-one)
    ledger_entry: Mapped[LedgerEntryModel | None] = relationship(
        "LedgerEntryModel", back_populates="transaction"
    )

    __table_args__ = (
        Index("ix_transactions_content_hash", "content_hash"),
    )


class LedgerEntryModel(Base):
    """Persistence model for Ledger Entries.

    Represents the hash-chained append-only log.
    sequence_number is the primary key (monotonic).
    """

    __tablename__ = "ledger_entries"

    id: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    sequence_number: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    transaction_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("transactions.id"), nullable=False, unique=True
    )

    transaction_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    previous_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    entry_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    timestamp: Mapped[datetime] = mapped_column(nullable=False)

    # Relationships
    transaction: Mapped[TransactionModel] = relationship(
        "TransactionModel", back_populates="ledger_entry"
    )

    __table_args__ = (
        Index("ix_ledger_entries_previous_hash", "previous_hash"),
    )


class LedgerHeadModel(Base):
    """Singleton table to track the tip of the ledger.

    Used for strict concurrency control (locking).
    Only one row should ever exist (id=1).
    """

    __tablename__ = "ledger_head"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    last_sequence_number: Mapped[int] = mapped_column(BigInteger, nullable=False)
    last_entry_hash: Mapped[str] = mapped_column(String(64), nullable=False)


class ApiKeyModel(Base):
    """Persistence model for API Keys.

    Stores the SHA-256 hash of the key, never the key itself.
    """

    __tablename__ = "api_keys"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    key_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    owner: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    scopes: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    webhook_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    gpg_public_key: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("ix_api_keys_key_hash", "key_hash"),
    )
