"""
Reconciliation domain models for Invario.

Represents the result of comparing source data against the ledger,
with explicit match statuses and detailed discrepancy information.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum


class MatchStatus(str, Enum):
    """Result status of a reconciliation match attempt."""

    MATCHED = "matched"
    UNMATCHED_SOURCE = "unmatched_source"
    UNMATCHED_TARGET = "unmatched_target"
    DISCREPANCY = "discrepancy"


@dataclass(frozen=True)
class Discrepancy:
    """Detail of a specific discrepancy found during reconciliation.

    Attributes:
        field_name: Name of the field with the discrepancy.
        source_value: Value from the source data.
        target_value: Value from the ledger/target.
        difference: Numeric difference (for amount fields).

    """

    field_name: str
    source_value: str
    target_value: str
    difference: Decimal | None = None


@dataclass(frozen=True)
class ReconciliationResult:
    """Result of reconciling a single record.

    Attributes:
        status: Match status of this reconciliation.
        source_hash: Content hash of the source transaction.
        target_hash: Content hash of the matched ledger entry (if any).
        discrepancies: List of field-level discrepancies found.
        message: Human-readable explanation of the result.

    """

    status: MatchStatus
    source_hash: str = ""
    target_hash: str = ""
    discrepancies: tuple[Discrepancy, ...] = field(default_factory=tuple)
    message: str = ""

    @property
    def is_matched(self) -> bool:
        """Check if reconciliation was successful."""
        return self.status == MatchStatus.MATCHED

    @property
    def has_discrepancies(self) -> bool:
        """Check if there are field-level discrepancies."""
        return len(self.discrepancies) > 0


@dataclass(frozen=True)
class ReconciliationReport:
    """Aggregate report from a reconciliation batch.

    Attributes:
        total_records: Total records processed.
        matched: Number of matched records.
        unmatched_source: Records in source but not in target.
        unmatched_target: Records in target but not in source.
        discrepancies: Records with field-level mismatches.
        results: All individual reconciliation results.

    """

    total_records: int
    matched: int
    unmatched_source: int
    unmatched_target: int
    discrepancies: int
    results: tuple[ReconciliationResult, ...] = field(default_factory=tuple)

    @property
    def is_fully_reconciled(self) -> bool:
        """Check if all records matched perfectly."""
        return self.matched == self.total_records
