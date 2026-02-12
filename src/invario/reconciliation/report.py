"""
Reconciliation report generator for Invario.

Aggregates individual reconciliation results into a structured
batch report with summary statistics.
"""

from __future__ import annotations

from taipanstack.core.result import Ok

from invario.domain.reconciliation import (
    MatchStatus,
    ReconciliationReport,
    ReconciliationResult,
)


def generate_report(results: list[ReconciliationResult]) -> ReconciliationReport:
    """Generate a comprehensive report from a list of results.

    Calculates totals for matched, unmatched, and discordant records.

    Args:
        results: List of individual reconciliation results.

    Returns:
        Structured ReconciliationReport.

    """
    total = len(results)
    matched = 0
    unmatched_source = 0
    unmatched_target = 0
    discrepancies = 0

    for res in results:
        match res.status:
            case MatchStatus.MATCHED:
                matched += 1
            case MatchStatus.UNMATCHED_SOURCE:
                unmatched_source += 1
            case MatchStatus.UNMATCHED_TARGET:
                unmatched_target += 1
            case MatchStatus.DISCREPANCY:
                discrepancies += 1

    return ReconciliationReport(
        total_records=total,
        matched=matched,
        unmatched_source=unmatched_source,
        unmatched_target=unmatched_target,
        discrepancies=discrepancies,
        results=tuple(results),
    )
