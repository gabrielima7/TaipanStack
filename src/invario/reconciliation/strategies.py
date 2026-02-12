"""
Reconciliation matching strategies for Invario.

Defines protocols and implementations for matching source transactions
against ledger entries (One-to-One, One-to-Many, Tolerance-based).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import timedelta
from decimal import Decimal
from typing import Protocol

from invario.domain.ledger_entry import LedgerEntry
from invario.domain.reconciliation import Discrepancy, MatchStatus, ReconciliationResult
from invario.domain.transaction import Transaction


class MatchingStrategy(Protocol):
    """Protocol for reconciliation matching strategies."""

    def match(
        self,
        source: Transaction,
        candidates: list[LedgerEntry],
    ) -> ReconciliationResult:
        """Attempt to match a source transaction against candidates.

        Args:
            source: The source transaction to match.
            candidates: Potential ledger entries to match against.

        Returns:
            ReconciliationResult with status and discrepancy details.

        """


class ExactMatchStrategy:
    """Strategy that requires exact matching of all key fields.

    Matches if:
    - Amounts are identical
    - Currencies are identical
    - Dates are identical
    - Documents match (if present)
    """

    def match(
        self,
        source: Transaction,
        candidates: list[LedgerEntry],
        # In a real system, we'd need to fetch the Transaction from the LedgerEntry
        # For this prototype, we'll assume candidates have access to their transaction details
        # via a repository lookup or similar.
        # To keep it simple and strictly typed, we'll assume we have a map or lookup function.
    ) -> ReconciliationResult:
        # NOTE: This signature needs to change because LedgerEntry only has hashes.
        # We need the full Transaction object for the candidate to compare fields.
        # This implies the Engine must look up the transactions *before* calling the strategy
        # OR the strategy receives (Transaction, Transaction) pairs.
        pass


# Redefining the protocol to be more practical for value comparison
class TransactionMatcher(ABC):
    """Abstract base for matching source transaction against target transaction."""

    @abstractmethod
    def compare(
        self,
        source: Transaction,
        target: Transaction,
    ) -> ReconciliationResult:
        """Compare two transactions and return a reconciliation result.

        Args:
            source: Source transaction (e.g., from CNAB).
            target: Target transaction (e.g., from Ledger).

        Returns:
            ReconciliationResult with detailed status.

        """


class ExactMatcher(TransactionMatcher):
    """Matcher requiring exact equality on amount, date, and document."""

    def compare(
        self,
        source: Transaction,
        target: Transaction,
    ) -> ReconciliationResult:
        discrepancies: list[Discrepancy] = []

        # Check Currency (Hard fail if different)
        if source.currency != target.currency:
            discrepancies.append(Discrepancy(
                field_name="currency",
                source_value=source.currency,
                target_value=target.currency,
            ))

        # Check Amount
        if source.amount != target.amount:
            discrepancies.append(Discrepancy(
                field_name="amount",
                source_value=str(source.amount),
                target_value=str(target.amount),
                difference=source.amount - target.amount,
            ))

        # Check Date
        if source.settlement_date != target.settlement_date:
            discrepancies.append(Discrepancy(
                field_name="settlement_date",
                source_value=source.settlement_date.isoformat(),
                target_value=target.settlement_date.isoformat(),
            ))

        # Check Document (if present on both)
        if source.document and target.document and source.document != target.document:
             discrepancies.append(Discrepancy(
                field_name="document",
                source_value=source.document,
                target_value=target.document,
            ))

        if not discrepancies:
            return ReconciliationResult(
                status=MatchStatus.MATCHED,
                source_hash=source.content_hash(),
                target_hash=target.content_hash(),
                message="Exact match confirmed",
            )

        return ReconciliationResult(
            status=MatchStatus.DISCREPANCY,
            source_hash=source.content_hash(),
            target_hash=target.content_hash(),
            discrepancies=tuple(discrepancies),
            message=f"Found {len(discrepancies)} discrepancies during exact match",
        )


class DateToleranceMatcher(TransactionMatcher):
    """Matcher that allows a tolerance window for settlement dates."""

    def __init__(self, tolerance_days: int = 1) -> None:
        self.tolerance = timedelta(days=tolerance_days)
        self.exact_matcher = ExactMatcher()

    def compare(
        self,
        source: Transaction,
        target: Transaction,
    ) -> ReconciliationResult:
        # Delegate to exact match for other fields first
        base_result = self.exact_matcher.compare(source, target)

        # If it matched or failed on non-date fields, return as is (but we need to check date specifically)
        # Actually, simpler: check amount/currency exactly, then check date with tolerance.

        discrepancies: list[Discrepancy] = []

         # Check Currency
        if source.currency != target.currency:
            discrepancies.append(Discrepancy("currency", source.currency, target.currency))

        # Check Amount
        if source.amount != target.amount:
            discrepancies.append(Discrepancy("amount", str(source.amount), str(target.amount), source.amount - target.amount))

        # Check Date with Tolerance
        diff = abs(source.settlement_date - target.settlement_date)
        if diff > self.tolerance:
             discrepancies.append(Discrepancy(
                field_name="settlement_date",
                source_value=source.settlement_date.isoformat(),
                target_value=target.settlement_date.isoformat(),
                difference=None, # Timedelta not supported by Decimal difference type in Discrepancy
            ))

        if not discrepancies:
             return ReconciliationResult(
                status=MatchStatus.MATCHED,
                source_hash=source.content_hash(),
                target_hash=target.content_hash(),
                message=f"Matched with date tolerance (diff: {diff})",
            )

        return ReconciliationResult(
            status=MatchStatus.DISCREPANCY,
            source_hash=source.content_hash(),
            target_hash=target.content_hash(),
            discrepancies=tuple(discrepancies),
            message="Discrepancies found in tolerance match",
        )
