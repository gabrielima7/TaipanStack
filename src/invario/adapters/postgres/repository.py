"""
PostgreSQL implementation of LedgerRepository.

Implements strict concurrency control using SELECT FOR UPDATE
on the LedgerHead singleton table to ensure linear hash chain.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError as SqlIntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from invario.adapters.postgres.models import (
    LedgerEntryModel,
    LedgerHeadModel,
    TransactionModel,
)
from invario.domain.ledger_entry import LedgerEntry
from invario.domain.transaction import Transaction
from invario.ledger.repository import LedgerRepository
from invario.ledger.store import LedgerError
from taipanstack.core.result import Err, Ok, Result


class PostgresLedgerRepository(LedgerRepository):
    """PostgreSQL-backed ledger repository with locking."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize with an active async session."""
        self.session = session

    async def _get_or_create_head(self) -> LedgerHeadModel:
        """Get the ledger head, creating it if it doesn't exist.

        MUST be called within a transaction.
        """
        # Try to lock the head row
        result = await self.session.execute(
            select(LedgerHeadModel)
            .where(LedgerHeadModel.id == 1)
            .with_for_update()
        )
        head = result.scalar_one_or_none()

        if head is None:
            # Initialize genesis state
            head = LedgerHeadModel(
                id=1,
                last_sequence_number=-1,
                last_entry_hash="0" * 64,  # Genesis hash
            )
            self.session.add(head)
            await self.session.flush()  # Ensure it exists for locking
            # In a race condition here, the unique constraint (id=1) would fail
            # validation, but with FOR UPDATE on select and a single initializer,
            # this is generally safe for startup. Production might run migrations.

        return head

    async def save_transaction(
        self,
        transaction: Transaction,
    ) -> Result[LedgerEntry, LedgerError]:
        """Save transaction and create ledger entry with locking."""
        try:
            # 1. Lock the Head to ensure sequential access
            head = await self._get_or_create_head()

            # 2. Check for duplicate content hash
            # (We could trust DB constraint, but checking saves a sequence gap if we wanted that)
            # Actually, let's rely on DB constraint for atomicity and catch IntegrityError

            # 3. Create Transaction Model
            tx_model = TransactionModel(
                id=transaction.id,
                type=transaction.type.value,
                amount=transaction.amount,
                currency=transaction.currency,
                source_account=transaction.source_account,
                target_account=transaction.target_account,
                document=transaction.document,
                settlement_date=transaction.settlement_date,
                description=transaction.description,
                idempotency_key=transaction.idempotency_key,
                bank_code=transaction.bank_code,
                raw_line=transaction.raw_line,
                content_hash=transaction.content_hash(),
            )
            self.session.add(tx_model)

            # 4. Create Ledger Entry
            new_seq = head.last_sequence_number + 1
            previous_hash = head.last_entry_hash

            # Create domain object to compute hash
            entry_domain = LedgerEntry.create(
                entry_id=uuid4(),
                transaction_hash=tx_model.content_hash,
                previous_hash=previous_hash,
                timestamp=datetime.now(tz=timezone.utc),
                sequence_number=new_seq,
            )

            entry_model = LedgerEntryModel(
                id=entry_domain.id,
                sequence_number=entry_domain.sequence_number,
                transaction_id=tx_model.id,
                transaction_hash=entry_domain.transaction_hash,
                previous_hash=entry_domain.previous_hash,
                entry_hash=entry_domain.entry_hash,
                timestamp=entry_domain.timestamp.replace(tzinfo=None), # PG stores naive UTC usually
            )
            self.session.add(entry_model)

            # 5. Update Head
            head.last_sequence_number = new_seq
            head.last_entry_hash = entry_domain.entry_hash

            # 6. Commit
            await self.session.commit()

            return Ok(entry_domain)

        except SqlIntegrityError as e:
            await self.session.rollback()
            if "transactions_content_hash_key" in str(e):
                return Err(LedgerError(f"Duplicate transaction: {transaction.content_hash()}"))
            if "transactions_idempotency_key_key" in str(e):
                return Err(LedgerError(f"Duplicate idempotency key: {transaction.idempotency_key}"))
            return Err(LedgerError(f"Database integrity error: {e}"))

        except Exception as e:
            await self.session.rollback()
            return Err(LedgerError(f"Persistence failure: {e}"))

    async def get_entry(
        self,
        sequence_number: int,
    ) -> Result[LedgerEntry, LedgerError]:
        """Retrieve entry by sequence number."""
        try:
            result = await self.session.execute(
                select(LedgerEntryModel).where(
                    LedgerEntryModel.sequence_number == sequence_number
                )
            )
            model = result.scalar_one_or_none()

            if not model:
                return Err(LedgerError(f"Entry {sequence_number} not found"))

            # Convert back to domain
            entry = LedgerEntry(
                id=model.id,
                transaction_hash=model.transaction_hash,
                previous_hash=model.previous_hash,
                timestamp=model.timestamp.replace(tzinfo=timezone.utc),
                sequence_number=model.sequence_number,
                entry_hash=model.entry_hash,
            )
            return Ok(entry)

        except Exception as e:
            return Err(LedgerError(f"Read error: {e}"))

    async def get_all_entries(self) -> tuple[LedgerEntry, ...]:
        """Retrieve all entries ordered by sequence."""
        result = await self.session.execute(
            select(LedgerEntryModel).order_by(LedgerEntryModel.sequence_number)
        )
        models = result.scalars().all()

        return tuple(
            LedgerEntry(
                id=m.id,
                transaction_hash=m.transaction_hash,
                previous_hash=m.previous_hash,
                timestamp=m.timestamp.replace(tzinfo=timezone.utc),
                sequence_number=m.sequence_number,
                entry_hash=m.entry_hash,
            )
            for m in models
        )

    async def contains(self, transaction: Transaction) -> bool:
        """Check if transaction exists by content hash."""
        result = await self.session.execute(
            select(TransactionModel).where(
                TransactionModel.content_hash == transaction.content_hash()
            )
        )
        return result.first() is not None
