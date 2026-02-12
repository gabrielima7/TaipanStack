"""Tests for Invario domain models."""

from datetime import date, datetime
from decimal import Decimal
from uuid import uuid4

import pytest
from invario.domain.ledger_entry import LedgerEntry
from invario.domain.reconciliation import MatchStatus, ReconciliationResult
from invario.domain.transaction import Transaction, TransactionType


def test_transaction_immutability():
    """Test that Transaction is immutable and hashable."""
    tx = Transaction(
        id=uuid4(),
        type=TransactionType.CREDIT,
        amount=Decimal("100.50"),
        currency="BRL",
        source_account="123",
        target_account="456",
        document="12345678901",
        settlement_date=date(2025, 1, 1),
        description="Test",
        idempotency_key=uuid4(),
        bank_code="001",
    )

    # Attempting to set a field should raise TypeError
    with pytest.raises(Exception):  # Frozen pydantic model raises ValidationError or TypeError depending on version
        tx.amount = Decimal("200.00")

    # Should be hashable (usable in sets/dicts if needed, or at least content_hash works)
    assert tx.content_hash()


def test_transaction_content_hash_consistency():
    """Test that content_hash is consistent for identical transactions."""
    tx_id = uuid4()
    idem_key = uuid4()

    tx1 = Transaction(
        id=tx_id,
        type=TransactionType.CREDIT,
        amount=Decimal("50.00"),
        currency="USD",
        source_account="A",
        target_account="B",
        document="DOC",
        settlement_date=date(2025, 1, 1),
        idempotency_key=idem_key,
        bank_code="001",
    )

    tx2 = Transaction(
        id=tx_id,
        type=TransactionType.CREDIT,
        amount=Decimal("50.00"),
        currency="USD",
        source_account="A",
        target_account="B",
        document="DOC",
        settlement_date=date(2025, 1, 1),
        idempotency_key=idem_key,
        bank_code="001",
        # description and raw_line are excluded from hash
        description="Different description",
        raw_line="Different raw line",
    )

    assert tx1.content_hash() == tx2.content_hash()


def test_ledger_entry_hashing():
    """Test LedgerEntry hash computation including previous hash."""
    tx_hash = "abc123hash"
    prev_hash = "0" * 64

    entry = LedgerEntry.create(
        entry_id=uuid4(),
        transaction_hash=tx_hash,
        previous_hash=prev_hash,
        timestamp=datetime(2025, 1, 1, 12, 0, 0),
        sequence_number=0,
    )

    assert entry.entry_hash
    assert len(entry.entry_hash) == 64
    assert entry.previous_hash == prev_hash

    # Verify hash content
    computed = entry.compute_hash()
    assert entry.entry_hash == computed


def test_reconciliation_result_properties():
    """Test helper properties on ReconciliationResult."""
    matched = ReconciliationResult(
        status=MatchStatus.MATCHED,
        source_hash="abcd",
        target_hash="abcd",
    )
    assert matched.is_matched
    assert not matched.has_discrepancies

    unmatched = ReconciliationResult(
        status=MatchStatus.UNMATCHED_SOURCE,
        source_hash="abcd",
    )
    assert not unmatched.is_matched
