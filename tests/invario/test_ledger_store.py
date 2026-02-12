"""Tests for Ledger Store."""

from datetime import date
from decimal import Decimal
from uuid import uuid4

import pytest
from invario.domain.transaction import Transaction, TransactionType
from invario.ledger.store import LedgerStore
from taipanstack.core.result import Err, Ok


@pytest.fixture
def sample_tx():
    return Transaction(
        id=uuid4(),
        type=TransactionType.CREDIT,
        amount=Decimal("100.00"),
        currency="BRL",
        source_account="A",
        target_account="B",
        document="DOC",
        settlement_date=date(2025, 1, 1),
        idempotency_key=uuid4(),
        bank_code="001",
    )


def test_ledger_append_success(sample_tx):
    """Test appending to ledger."""
    store = LedgerStore()
    assert store.size == 0
    assert store.last_hash == "0" * 64

    result = store.append(sample_tx)
    assert isinstance(result, Ok)
    entry = result.unwrap()

    assert store.size == 1
    assert entry.sequence_number == 0
    assert entry.previous_hash == "0" * 64
    assert store.last_hash == entry.entry_hash


def test_ledger_chaining(sample_tx):
    """Test that entries are chained correctly."""
    store = LedgerStore()

    # Entry 1
    store.append(sample_tx)
    hash1 = store.last_hash

    # Entry 2 (different ID to avoid deduplication)
    tx2 = sample_tx.model_copy(update={"id": uuid4()})
    result2 = store.append(tx2)
    entry2 = result2.unwrap()

    assert entry2.previous_hash == hash1
    assert entry2.sequence_number == 1


def test_ledger_deduplication(sample_tx):
    """Test that duplicate transactions are rejected."""
    store = LedgerStore()
    store.append(sample_tx)

    # Try appending exact same transaction again
    result = store.append(sample_tx)
    assert isinstance(result, Err)
    assert "Duplicate transaction" in str(result.unwrap_err())
    assert store.size == 1
