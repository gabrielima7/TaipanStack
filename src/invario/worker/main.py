import os
import structlog
from arq import create_pool
from arq.connections import RedisSettings
from taipanstack.core.result import Err, Ok

from invario.ingestion.pipeline import ingest_file
from invario.worker.webhooks import send_webhook
from invario.adapters.postgres.database import db
from invario.adapters.postgres.repository import PostgresLedgerRepository

logger = structlog.get_logger()

async def startup(ctx):
    logger.info("worker_starting")
    # Initialize DB connection (handled by global engine but good to warm up)
    pass

async def shutdown(ctx):
    logger.info("worker_shutting_down")
    await db.close()

async def process_ingestion_job(ctx, file_path: str, api_key_hash: str, webhook_url: str | None, correlation_id: str):
    """
    Job to process an uploaded file.

    1. Read file from disk.
    2. Run Ingestion Pipeline (validation).
    3. Persist to Ledger (if valid).
    4. Send Webhook (if configured).
    """
    log = logger.bind(
        correlation_id=correlation_id,
        job="ingestion",
        file=file_path
    )
    log.info("job_started")

    status = "failed"
    result_summary = {}

    try:
        # 1. Read File
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            filename = os.path.basename(file_path)
        except Exception as e:
            log.error("file_read_error", error=str(e))
            raise Exception(f"Failed to read file: {e}")

        # 2. Pipeline Execution (CPU-bound)
        pipeline_result = ingest_file(filename, content)

        match pipeline_result:
            case Ok(transactions):
                # 3. Persistence (IO-bound)
                saved_count = 0
                rejected_count = 0
                errors = []

                async with db.session_factory() as session:
                    repo = PostgresLedgerRepository(session)

                    for tx in transactions:
                        res = await repo.save_transaction(tx)
                        match res:
                            case Ok(_):
                                saved_count += 1
                            case Err(e):
                                rejected_count += 1
                                errors.append(str(e.reason))
                                log.warning("transaction_persistence_failed", tx_id=str(tx.id), reason=str(e.reason))

                status = "success"
                result_summary = {
                    "transactions_processed": saved_count,
                    "transactions_rejected": rejected_count,
                    "total_amount": str(sum(tx.amount for tx in transactions)),
                    "currency": transactions[0].currency if transactions else "N/A",
                    "errors": errors[:5] if errors else [] # Cap error list
                }
                log.info("ingestion_success", count=saved_count)

            case Err(error):
                status = "failed"
                result_summary = {"error": str(error.reason)}
                log.warning("ingestion_validation_failed", reason=str(error.reason))

    except Exception as e:
        log.error("job_crashed", error=str(e))
        status = "error"
        result_summary = {"crash_reason": str(e)}

    finally:
        # Cleanup temp file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError:
                pass

    # 4. Send Webhook
    if webhook_url:
        payload = {
            "event": "ingestion_completed",
            "job_id": ctx["job_id"],
            "status": status,
            "correlation_id": correlation_id,
            "result": result_summary
        }
        await send_webhook(webhook_url, payload)

class WorkerSettings:
    functions = [process_ingestion_job]
    redis_settings = RedisSettings.from_dsn(os.getenv("REDIS_URL", "redis://localhost:6379"))
    on_startup = startup
    on_shutdown = shutdown
