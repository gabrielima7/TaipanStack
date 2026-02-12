"""
Immutable, hash-chained ledger store for Invario.

An append-only data structure where each entry's hash includes
the previous entry's hash, forming an auditable chain.
Every mutation returns Result — never crashes.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from taipanstack.core.result import Err, Ok, Result

from invario.domain.ledger_entry import LedgerEntry
from invario.domain.transaction import Transaction


class LedgerError(Exception):
    """Raised when a ledger operation fails.

    Attributes:
        reason: Specific reason for the failure.

    """

    def __init__(self, reason: str) -> None:
        """Initialize LedgerError."""
        self.reason = reason
        super().__init__(f"Ledger error: {reason}")


class LedgerStore:
    """Append-only, hash-chained financial ledger.

    Each entry's hash includes the previous entry's hash,
    creating a tamper-evident audit trail. Similar to a
    simplified blockchain without consensus.

    Example:
        >>> store = LedgerStore()
        >>> result = store.append(transaction)
        >>> match result:
        ...     case Ok(entry):
        ...         print(f"Entry #{entry.sequence_number}")
        ...     case Err(error):
        ...         print(f"Failed: {error}")

    """

    def __init__(self) -> None:
        """Initialize an empty ledger store."""
        self._entries: list[LedgerEntry] = []
        self._transaction_hashes: set[str] = set()

    @property
    def entries(self) -> tuple[LedgerEntry, ...]:
        """Return all entries as an immutable tuple."""
        return tuple(self._entries)

    @property
    def size(self) -> int:
        """Return the number of entries in the ledger."""
        return len(self._entries)

    @property
    def last_hash(self) -> str:
        """Return the hash of the last entry, or genesis hash."""
        if self._entries:
            return self._entries[-1].entry_hash
        return "0" * 64  # Genesis hash

    def append(
        self,
        transaction: Transaction,
    ) -> Result[LedgerEntry, LedgerError]:
        """Append a transaction to the ledger.

        Creates a new hash-chained LedgerEntry from the transaction.
        Rejects duplicate transactions (by content hash).

        Args:
            transaction: Validated transaction to record.

        Returns:
            Ok(LedgerEntry) on success, Err(LedgerError) on failure.

        """
        tx_hash = transaction.content_hash()

        # Guard against duplicates (idempotency)
        if tx_hash in self._transaction_hashes:
            return Err(LedgerError(
                f"Duplicate transaction detected: hash={tx_hash[:16]}..."
            ))

        try:
            entry = LedgerEntry.create(
                entry_id=uuid4(),
                transaction_hash=tx_hash,
                previous_hash=self.last_hash,
                timestamp=datetime.now(tz=timezone.utc),
                sequence_number=self.size,
            )

            self._entries.append(entry)
            self._transaction_hashes.add(tx_hash)
            return Ok(entry)

        except Exception as e:
            return Err(LedgerError(f"Failed to create entry: {e}"))

    def get_entry(
        self,
        sequence_number: int,
    ) -> Result[LedgerEntry, LedgerError]:
        """Retrieve an entry by sequence number.

        Args:
            sequence_number: Zero-based sequence number.

        Returns:
            Ok(LedgerEntry) if found, Err(LedgerError) if not.

        """
        if sequence_number < 0 or sequence_number >= self.size:
            return Err(LedgerError(
                f"Sequence number {sequence_number} out of range "
                f"(ledger size: {self.size})"
            ))

        return Ok(self._entries[sequence_number])

    def contains_transaction(self, transaction: Transaction) -> bool:
        """Check if a transaction is already in the ledger.

        Args:
            transaction: Transaction to check.

        Returns:
            True if the transaction's content hash exists in the ledger.

        """
        return transaction.content_hash() in self._transaction_hashes
