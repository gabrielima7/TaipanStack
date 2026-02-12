"""Tests for Ledger Integrity."""

from datetime import datetime, timezone
from uuid import uuid4

from invario.domain.ledger_entry import LedgerEntry
from invario.ledger.integrity import verify_chain, IntegrityError
from taipanstack.core.result import Ok, Err


def create_entry(seq, prev_hash, content_hash):
    """Helper to create a raw entry."""
    return LedgerEntry(
        id=uuid4(),
        transaction_hash=content_hash, # Simplified
        previous_hash=prev_hash,
        timestamp=datetime.now(tz=timezone.utc),
        sequence_number=seq,
        entry_hash="", # Computed below
    )


def test_verify_chain_valid():
    """Test verification of a valid chain."""
    # Genesis
    e1_raw = create_entry(0, "0"*64, "tx1")
    e1 = e1_raw.model_copy(update={"entry_hash": e1_raw.compute_hash()})

    # Second
    e2_raw = create_entry(1, e1.entry_hash, "tx2")
    e2 = e2_raw.model_copy(update={"entry_hash": e2_raw.compute_hash()})

    result = verify_chain([e1, e2])
    assert isinstance(result, Ok)
    assert result.unwrap() is True


def test_verify_chain_broken_link():
    """Test detection of broken hash chain."""
    e1_raw = create_entry(0, "0"*64, "tx1")
    e1 = e1_raw.model_copy(update={"entry_hash": e1_raw.compute_hash()})

    # Second entry points to WRONG previous hash
    e2_raw = create_entry(1, "WRONG_HASH", "tx2")
    e2 = e2_raw.model_copy(update={"entry_hash": e2_raw.compute_hash()})

    result = verify_chain([e1, e2])
    assert isinstance(result, Err)
    err = result.unwrap_err()
    assert err.violation_type == "chain_link_broken"
    assert err.sequence_number == 1


def test_verify_chain_tampered_content():
    """Test detection of tampered content."""
    e1_raw = create_entry(0, "0"*64, "tx1")
    # Compute valid hash
    valid_hash = e1_raw.compute_hash()

    # Create entry with valid hash but DIFFERENT content
    # (Simulates modifying DB content without re-hashing)
    tampered = e1_raw.model_copy(update={
        "transaction_hash": "modified_tx",
        "entry_hash": valid_hash
    })

    result = verify_chain([tampered])
    assert isinstance(result, Err)
    err = result.unwrap_err()
    assert err.violation_type == "entry_hash_mismatch"
