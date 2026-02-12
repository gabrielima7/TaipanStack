"""
Ledger entry domain model for Invario.

Hash-chained, immutable ledger entry — the fundamental unit
of the append-only financial ledger. Each entry's hash includes
the previous entry's hash, forming an auditable chain.
"""

from __future__ import annotations

import hashlib
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class LedgerEntry(BaseModel):
    """Immutable, hash-chained ledger entry.

    Attributes:
        id: Unique entry identifier.
        transaction_hash: SHA-256 hash of the source Transaction.
        previous_hash: Hash of the previous LedgerEntry (chain link).
        timestamp: When this entry was recorded.
        sequence_number: Monotonically increasing sequence.
        entry_hash: SHA-256 hash of this entry (computed from all fields).

    """

    id: UUID
    transaction_hash: str
    previous_hash: str = Field(
        default="0" * 64,
        description="Genesis block uses 64 zeros",
    )
    timestamp: datetime
    sequence_number: int = Field(ge=0)
    entry_hash: str = ""

    model_config = ConfigDict(frozen=True)

    def compute_hash(self) -> str:
        """Compute SHA-256 hash of this ledger entry.

        The hash covers: id, transaction_hash, previous_hash,
        timestamp, and sequence_number — ensuring tamper detection.

        Returns:
            Hex-encoded SHA-256 hash string.

        """
        content = (
            f"{self.id}|{self.transaction_hash}|{self.previous_hash}|"
            f"{self.timestamp.isoformat()}|{self.sequence_number}"
        )
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    @classmethod
    def create(
        cls,
        *,
        entry_id: UUID,
        transaction_hash: str,
        previous_hash: str,
        timestamp: datetime,
        sequence_number: int,
    ) -> LedgerEntry:
        """Create a new LedgerEntry with its hash pre-computed.

        Args:
            entry_id: Unique entry identifier.
            transaction_hash: Hash of the source transaction.
            previous_hash: Hash of the previous entry.
            timestamp: Recording timestamp.
            sequence_number: Entry sequence number.

        Returns:
            A new LedgerEntry with entry_hash populated.

        """
        # Create without hash first to compute it
        entry_without_hash = cls(
            id=entry_id,
            transaction_hash=transaction_hash,
            previous_hash=previous_hash,
            timestamp=timestamp,
            sequence_number=sequence_number,
            entry_hash="",
        )
        computed_hash = entry_without_hash.compute_hash()

        # Return new frozen instance with hash set
        return cls(
            id=entry_id,
            transaction_hash=transaction_hash,
            previous_hash=previous_hash,
            timestamp=timestamp,
            sequence_number=sequence_number,
            entry_hash=computed_hash,
        )
