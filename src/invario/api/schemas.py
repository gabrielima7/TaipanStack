"""
Pydantic schemas for the Invario API.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    """API health status."""

    status: str
    version: str


class IngestResponse(BaseModel):
    """Response for file ingestion."""

    filename: str
    transactions_processed: int
    status: str = "success"


class AuditResponse(BaseModel):
    """Response for ledger integrity audit."""

    status: str
    total_entries: int
    last_sequence: int
    last_hash: str
    integrity_valid: bool
    violation: dict[str, str | int] | None = None
    checked_at: datetime
