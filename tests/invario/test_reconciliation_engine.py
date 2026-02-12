"""Tests for Reconciliation Engine."""

from datetime import date
from decimal import Decimal
from uuid import uuid4

import pytest
from invario.domain.reconciliation import MatchStatus
from invario.domain.transaction import Transaction, TransactionType
from invario.reconciliation.engine import ReconciliationEngine
from taipanstack.core.result import Ok


@pytest.fixture
def make_tx():
    def _make(id_val=None, amount="100.00"):
        return Transaction(
            id=id_val or uuid4(),
            type=TransactionType.CREDIT,
            amount=Decimal(amount),
            currency="BRL",
            source_account="A",
            target_account="B",
            document="DOC",
            settlement_date=date(2025, 1, 1),
            idempotency_key=uuid4(),
            bank_code="001",
        )
    return _make


def test_reconcile_exact_match(make_tx):
    """Test perfect match."""
    tx_id = uuid4()
    source = make_tx(tx_id)
    target = make_tx(tx_id) # Identical copies

    engine = ReconciliationEngine()
    result = engine.reconcile([source], [target])

    assert isinstance(result, Ok)
    report = result.unwrap()

    assert report.total_records == 1
    assert report.matched == 1
    assert report.discrepancies == 0
    assert report.results[0].status == MatchStatus.MATCHED


def test_reconcile_discrepancy(make_tx):
    """Test matching ID but different amount."""
    tx_id = uuid4()
    source = make_tx(tx_id, amount="100.00")
    target = make_tx(tx_id, amount="200.00") # Discrepancy

    engine = ReconciliationEngine()
    result = engine.reconcile([source], [target])

    report = result.unwrap()
    assert report.discrepancies == 1
    assert report.results[0].status == MatchStatus.DISCREPANCY

    disc = report.results[0].discrepancies[0]
    assert disc.field_name == "amount"
    assert disc.difference == Decimal("-100.00")


def test_reconcile_unmatched(make_tx):
    """Test unmatched source and unmatched target."""
    source = make_tx() # Unique ID
    target = make_tx() # Different Unique ID

    engine = ReconciliationEngine()
    result = engine.reconcile([source], [target])

    report = result.unwrap()
    assert report.total_records == 2
    assert report.unmatched_source == 1
    assert report.unmatched_target == 1
