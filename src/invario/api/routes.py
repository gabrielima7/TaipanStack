"""
FastAPI routes for Invario.
"""

import os
import shutil
import uuid
import base64
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile, status, Depends, Request, Header
from taipanstack.core.result import Err, Ok

from invario import __version__
from invario.api.dependencies import LedgerRepoDep
from invario.api.schemas import AuditResponse, HealthCheckResponse, IngestResponse
from invario.api.telemetry import (
    LEDGER_INTEGRITY_GAUGE,
)
from invario.ledger.integrity import verify_chain
from invario.api.security import get_api_key
from invario.api.security_gpg import verify_signature
from invario.adapters.postgres.models import ApiKeyModel
import structlog

# Initialize Router
router = APIRouter()
logger = structlog.get_logger()

# Uploads directory
UPLOAD_DIR = Path("/tmp/invario_uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/health", response_model=HealthCheckResponse)
async def health_check(
    repo: LedgerRepoDep,
) -> HealthCheckResponse:
    """Deep health check endpoint."""
    try:
        entries = await repo.get_all_entries()
        if entries:
             result = verify_chain(entries)
             if isinstance(result, Err):
                 LEDGER_INTEGRITY_GAUGE.set(0)
                 raise HTTPException(
                     status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                     detail=f"Ledger corrupted: {result.err().reason}",
                 )
        LEDGER_INTEGRITY_GAUGE.set(1)
        return HealthCheckResponse(status="ok", version=__version__)
    except Exception as e:
        LEDGER_INTEGRITY_GAUGE.set(0)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"System unhealthy: {e}",
        )


@router.post("/v1/ingest", status_code=status.HTTP_202_ACCEPTED)
async def ingest_transactions(
    request: Request,
    file: UploadFile,
    x_signature: str = Header(..., alias="X-Signature"),
    api_key: ApiKeyModel = Depends(get_api_key),
) -> dict:
    """Async Ingestion Queue.

    1. Validates GPG Signature (X-Signature).
    2. Buffers file to disk.
    3. Enqueues processing job.
    4. Returns Job ID immediately.
    """
    log = logger.bind(owner=api_key.owner)

    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename missing")

    # 1. Non-Repudiation: Verify Signature
    if not api_key.gpg_public_key:
        # For now, require GPG key to be set up.
        # Or allow bypass if specific scope? Strict mode: Require it.
        # Let's enforce it for "Scale & Non-Repudiation" phase.
        raise HTTPException(
            status_code=400,
            detail="Client GPG Public Key not configured. Contact support."
        )

    # We need to read content to verify signature AND save to disk.
    # For very large files, this memory read might be heavy, but signature verification
    # typically requires full content anyway unless we stream-update hash.
    # python-gnupg verify needs data or file.

    try:
        content_bytes = await file.read()
        content_str = content_bytes.decode("utf-8")

        # Decode Header
        # Client sends Base64(ASCII Armor)
        decoded_sig_bytes = base64.b64decode(x_signature)
        decoded_sig = decoded_sig_bytes.decode("utf-8")

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Request parsing error: {e}")

    # Verify Sig
    sig_result = verify_signature(content_str, decoded_sig, api_key.gpg_public_key)
    match sig_result:
        case Ok(True):
            pass # Valid
        case Err(reason):
            log.warning("signature_rejected", reason=reason)
            raise HTTPException(status_code=400, detail=f"Invalid Signature: {reason}")

    # 2. Buffer to Disk
    # Generate correlation ID and unique filename
    correlation_id = str(uuid.uuid4())
    safe_filename = f"{correlation_id}_{file.filename}"
    file_path = UPLOAD_DIR / safe_filename

    try:
        # Write bytes effectively
        with open(file_path, "wb") as f:
            f.write(content_bytes)
    except Exception as e:
        log.error("upload_write_failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to buffer upload")

    # 3. Enqueue Job
    try:
        job = await request.app.state.arq_pool.enqueue_job(
            "process_ingestion_job",
            file_path=str(file_path),
            api_key_hash=api_key.key_hash,
            webhook_url=api_key.webhook_url,
            correlation_id=correlation_id
        )
        if not job:
             raise Exception("Job enqueue rejected")

        log.info("job_enqueued", job_id=job.job_id)

        return {
            "job_id": job.job_id,
            "status": "queued",
            "correlation_id": correlation_id,
            "message": "File accepted for processing."
        }

    except Exception as e:
        log.error("enqueue_failed", error=str(e))
        # Cleanup
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail="Queue unavailable")


@router.get("/v1/jobs/{job_id}")
async def get_job_status(
    request: Request,
    job_id: str,
    api_key: ApiKeyModel = Depends(get_api_key),
) -> dict:
    """Check status of background job."""
    from arq.jobs import Job
    pool = request.app.state.arq_pool
    job = Job(job_id, pool)

    try:
        status = await job.status()
        info = await job.info()
        result = await job.result(timeout=0.1) if status == "complete" else None
    except TimeoutError:
        result = None
    except Exception:
         # Job might not exist
         status = "unknown"
         result = None

    return {
        "job_id": job_id,
        "status": str(status),
        "result": result
    }


@router.get("/v1/ledger/audit", response_model=AuditResponse)
async def audit_ledger(
    repo: LedgerRepoDep,
    api_key: ApiKeyModel = Depends(get_api_key),
) -> AuditResponse:
    """Verify integrity of the entire ledger hash chain."""
    entries = await repo.get_all_entries()
    result = verify_chain(entries)

    last_seq = -1
    last_hash = "0" * 64
    if entries:
        last_entry = entries[-1]
        last_seq = last_entry.sequence_number
        last_hash = last_entry.entry_hash

    match result:
        case Ok(True):
            return AuditResponse(
                status="healthy",
                total_entries=len(entries),
                last_sequence=last_seq,
                last_hash=last_hash,
                integrity_valid=True,
                checked_at=datetime.now(tz=timezone.utc),
            )
        case Err(error):
            return AuditResponse(
                status="corrupted",
                total_entries=len(entries),
                last_sequence=last_seq,
                last_hash=last_hash,
                integrity_valid=False,
                violation={
                    "type": error.violation_type,
                    "sequence": error.sequence_number,
                    "expected": error.expected_hash,
                    "actual": error.actual_hash,
                },
                checked_at=datetime.now(tz=timezone.utc),
            )
        case _:
             raise HTTPException(status_code=500, detail="Unknown integity result")
