"""
Telemetry configuration for Invario (Logging & Metrics).
"""

import logging
import os
import sys
import time
import uuid
from collections.abc import Callable

import structlog
from fastapi import Request, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Counter,
    Gauge,
    generate_latest,
    multiprocess,
)
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

# --- Metrics Configuration ---

# Registry for metrics
REGISTRY = CollectorRegistry()

# Multiprocess collector support (if configured)
if "PROMETHEUS_MULTIPROC_DIR" in os.environ:
    multiprocess.MultiProcessCollector(REGISTRY)

# Business Metrics
TRANSACTION_COUNTER = Counter(
    "invario_transactions_total",
    "Total number of processed transactions",
    ["status", "type"],
    registry=REGISTRY,
)

REJECTED_AMOUNT_COUNTER = Counter(
    "invario_rejected_amount_total",
    "Total monetary amount rejected by guards",
    registry=REGISTRY,
)

LEDGER_INTEGRITY_GAUGE = Gauge(
    "invario_ledger_integrity_status",
    "Ledger integrity status (1=OK, 0=Corrupted)",
    registry=REGISTRY,
)


def setup_logging() -> None:
    """Configure structlog for JSON output."""
    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    if sys.stderr.isatty():
        # Pretty print for local dev works
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(),
        ]
    else:
        # JSON for production
        processors = shared_processors + [
            structlog.processors.JSONRenderer(),
        ]

    structlog.configure(
        processors=processors,  # type: ignore
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Configure standard logging to intercept and redirect to structlog
    logging.basicConfig(format="%(message)s", level=logging.INFO)


class TelemetryMiddleware(BaseHTTPMiddleware):
    """Middleware for structured logging and metrics."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
        )

        start_time = time.perf_counter()

        try:
            response = await call_next(request)

            process_time = time.perf_counter() - start_time

            # Log completion
            status_code = response.status_code
            log = structlog.get_logger()
            if status_code >= 500:
                log.error("request_failed", status=status_code, duration=process_time)
            elif status_code >= 400:
                log.warning("request_client_error", status=status_code, duration=process_time)
            else:
                log.info("request_completed", status=status_code, duration=process_time)

            return response

        except Exception:
            process_time = time.perf_counter() - start_time
            structlog.get_logger().exception("request_crashed", duration=process_time)
            raise


def metrics_endpoint(request: Request) -> Response:
    """Expose Prometheus metrics."""
    return Response(
        generate_latest(REGISTRY),
        media_type=CONTENT_TYPE_LATEST,
    )
