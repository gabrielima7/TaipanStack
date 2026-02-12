"""
Reconciliation Engine for Invario.

The core engine that compares source transactions against a target set
(e.g., from the Ledger), applying a matching strategy to produce a
comprehensive reconciliation report.
"""

from __future__ import annotations

from taipanstack.core.result import Err, Ok, Result

from invario.domain.reconciliation import (
    MatchStatus,
    ReconciliationReport,
    ReconciliationResult,
)
from invario.domain.transaction import Transaction
from invario.reconciliation.report import generate_report
from invario.reconciliation.strategies import ExactMatcher, TransactionMatcher


class ReconciliationError(Exception):
    """Raised when reconciliation process fails fatally."""

    def __init__(self, message: str) -> None:
        super().__init__(f"Reconciliation error: {message}")


class ReconciliationEngine:
    """Core engine for reconciling transaction sets.

    Uses a pluggable matcher strategy to compare source and target records.
    Currently implements a simple One-to-One matching logic based on
    Transaction ID or Idempotency Key lookup, then deep value comparison.
    """

    def __init__(self, matcher: TransactionMatcher | None = None) -> None:
        """Initialize with a matching strategy.

        Args:
            matcher: Strategy to use for comparison. Defaults to ExactMatcher.

        """
        self.matcher = matcher or ExactMatcher()

    def reconcile(
        self,
        source_transactions: list[Transaction],
        target_transactions: list[Transaction],
    ) -> Result[ReconciliationReport, ReconciliationError]:
        """Reconcile source transactions against target transactions.

        Algorithm:
        1. Index target transactions by ID (and/or idempotency key) for O(1) lookup.
        2. Iterate through source transactions.
        3. Try to find a corresponding target transaction.
        4. If found, run the Matcher to check for discrepancies.
        5. If not found, mark as UNMATCHED_SOURCE.
        6. Finally, identify targets that were never touched (UNMATCHED_TARGET).

        Args:
            source_transactions: Incoming batch (e.g., from file).
            target_transactions: Reference set (e.g., from Ledger).

        Returns:
            Ok(ReconciliationReport) on success, Err on fatal error.

        """
        try:
            results: list[ReconciliationResult] = []

            # 1. Index targets
            # We map ID -> Transaction.
            # In a real system we might map (Amount, Date) -> list[Transaction] for fuzzy matching.
            # Here we assume we are reconciling based on known IDs or keys first.
            target_map: dict[str, Transaction] = {
                str(tx.id): tx for tx in target_transactions
            }
            # Track which targets have been matched
            matched_target_ids: set[str] = set()

            # 2. Process sources
            for source in source_transactions:
                source_id = str(source.id)
                target = target_map.get(source_id)

                if target:
                    # Found a candidate, now compare
                    match_result = self.matcher.compare(source, target)
                    results.append(match_result)
                    matched_target_ids.add(source_id)
                else:
                    # No target found with this ID
                    results.append(ReconciliationResult(
                        status=MatchStatus.UNMATCHED_SOURCE,
                        source_hash=source.content_hash(),
                        message="Transaction not found in target set",
                    ))

            # 3. Identify unmatched targets
            for target_id, target in target_map.items():
                if target_id not in matched_target_ids:
                    results.append(ReconciliationResult(
                        status=MatchStatus.UNMATCHED_TARGET,
                        target_hash=target.content_hash(),
                        message="Transaction in target but not in source",
                    ))

            # 4. Generate report
            report = generate_report(results)
            return Ok(report)

        except Exception as e:
            return Err(ReconciliationError(str(e)))
