"""
Ledger integrity verification for Invario.

Walks the hash chain and verifies the integrity of every entry.
Detects tampering, missing entries, or broken chain links.
"""

from __future__ import annotations

from dataclasses import dataclass

from taipanstack.core.result import Err, Ok, Result

from invario.domain.ledger_entry import LedgerEntry


GENESIS_HASH = "0" * 64


@dataclass(frozen=True)
class IntegrityError:
    """Detail of an integrity violation found in the ledger.

    Attributes:
        sequence_number: Entry where the violation was detected.
        expected_hash: What the hash should be.
        actual_hash: What the hash actually is.
        violation_type: Type of violation detected.

    """

    sequence_number: int
    expected_hash: str
    actual_hash: str
    violation_type: str


def verify_entry_hash(entry: LedgerEntry) -> Result[bool, IntegrityError]:
    """Verify that an entry's stored hash matches its computed hash.

    Args:
        entry: The ledger entry to verify.

    Returns:
        Ok(True) if hash is valid, Err(IntegrityError) if tampered.

    """
    computed = entry.compute_hash()

    if entry.entry_hash != computed:
        return Err(IntegrityError(
            sequence_number=entry.sequence_number,
            expected_hash=computed,
            actual_hash=entry.entry_hash,
            violation_type="entry_hash_mismatch",
        ))

    return Ok(True)


def verify_chain_link(
    current: LedgerEntry,
    previous: LedgerEntry | None,
) -> Result[bool, IntegrityError]:
    """Verify that the chain link between two consecutive entries is valid.

    Args:
        current: The current entry.
        previous: The previous entry (None for first entry).

    Returns:
        Ok(True) if chain link is valid, Err(IntegrityError) if broken.

    """
    expected_previous_hash = (
        previous.entry_hash if previous is not None else GENESIS_HASH
    )

    if current.previous_hash != expected_previous_hash:
        return Err(IntegrityError(
            sequence_number=current.sequence_number,
            expected_hash=expected_previous_hash,
            actual_hash=current.previous_hash,
            violation_type="chain_link_broken",
        ))

    return Ok(True)


def verify_chain(
    entries: tuple[LedgerEntry, ...] | list[LedgerEntry],
) -> Result[bool, IntegrityError]:
    """Verify the integrity of an entire ledger chain.

    Walks every entry from genesis to tip, verifying:
    1. Each entry's hash matches its content
    2. Each entry's previous_hash matches the preceding entry

    Args:
        entries: Ordered sequence of ledger entries.

    Returns:
        Ok(True) if entire chain is valid.
        Err(IntegrityError) on first violation detected.

    """
    if not entries:
        return Ok(True)  # Empty chain is trivially valid

    # Verify sequence numbers are monotonic
    for i, entry in enumerate(entries):
        if entry.sequence_number != i:
            return Err(IntegrityError(
                sequence_number=i,
                expected_hash=str(i),
                actual_hash=str(entry.sequence_number),
                violation_type="sequence_gap",
            ))

    # Walk the chain
    for i, entry in enumerate(entries):
        # Verify entry hash
        hash_result = verify_entry_hash(entry)
        match hash_result:
            case Err() as err:
                return err
            case Ok():
                pass

        # Verify chain link
        previous = entries[i - 1] if i > 0 else None
        link_result = verify_chain_link(entry, previous)
        match link_result:
            case Err() as err:
                return err
            case Ok():
                pass

    return Ok(True)
