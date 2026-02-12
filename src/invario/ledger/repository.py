"""
Ledger repository abstraction for Invario.

Provides an abstract base and in-memory implementation
for ledger data access, following TaipanStack's repository pattern.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from taipanstack.core.result import Err, Ok, Result

from invario.domain.ledger_entry import LedgerEntry
from invario.domain.transaction import Transaction
from invario.ledger.store import LedgerError, LedgerStore


class LedgerRepository(ABC):
    """Abstract base class for ledger data access."""

    @abstractmethod
    async def save_transaction(
        self,
        transaction: Transaction,
    ) -> Result[LedgerEntry, LedgerError]:
        """Save a validated transaction to the ledger.

        Args:
            transaction: The transaction to record.

        Returns:
            Ok(LedgerEntry) on success, Err(LedgerError) on failure.

        """

    @abstractmethod
    async def get_entry(
        self,
        sequence_number: int,
    ) -> Result[LedgerEntry, LedgerError]:
        """Retrieve a ledger entry by sequence number.

        Args:
            sequence_number: Zero-based sequence number.

        Returns:
            Ok(LedgerEntry) if found, Err(LedgerError) if not.

        """

    @abstractmethod
    async def get_all_entries(self) -> tuple[LedgerEntry, ...]:
        """Retrieve all ledger entries in order.

        Returns:
            Tuple of all entries, ordered by sequence number.

        """

    @abstractmethod
    async def contains(self, transaction: Transaction) -> bool:
        """Check if a transaction already exists in the ledger.

        Args:
            transaction: Transaction to search for.

        Returns:
            True if transaction's content hash is found.

        """


class InMemoryLedgerRepository(LedgerRepository):
    """In-memory ledger repository backed by LedgerStore.

    Suitable for testing and development. For production,
    implement a persistent LedgerRepository with database backing.

    """

    def __init__(self) -> None:
        """Initialize with an empty LedgerStore."""
        self._store = LedgerStore()

    async def save_transaction(
        self,
        transaction: Transaction,
    ) -> Result[LedgerEntry, LedgerError]:
        """Save a transaction to the in-memory ledger."""
        return self._store.append(transaction)

    async def get_entry(
        self,
        sequence_number: int,
    ) -> Result[LedgerEntry, LedgerError]:
        """Retrieve an entry from the in-memory ledger."""
        return self._store.get_entry(sequence_number)

    async def get_all_entries(self) -> tuple[LedgerEntry, ...]:
        """Retrieve all entries from the in-memory ledger."""
        return self._store.entries

    async def contains(self, transaction: Transaction) -> bool:
        """Check if a transaction exists in the in-memory ledger."""
        return self._store.contains_transaction(transaction)
