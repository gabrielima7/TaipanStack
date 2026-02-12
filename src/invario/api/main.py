"""
FastAPI application entrypoint for Invario.
"""


from contextlib import asynccontextmanager
import os

from arq import create_pool
from arq.connections import RedisSettings

from fastapi import FastAPI

from invario import __version__
from invario.adapters.postgres.database import db
from invario.api.routes import router
from invario.api.telemetry import (
    TelemetryMiddleware,
    metrics_endpoint,
    setup_logging,
)

# Initialize logging before app startup
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events."""
    # Initialize Arq Redis Pool
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    app.state.arq_pool = await create_pool(RedisSettings.from_dsn(redis_url))

    yield
    # Shutdown
    await db.close()
    await app.state.arq_pool.close()


app = FastAPI(
    title="Invario Financial Middleware",
    description="""
    **High-Integrity Settlement & Compliance Middleware**

    Invario provides a Zero-Trust data pipeline for financial transaction ingestion,
    cryptographic ledgering, and compliance validation.

    ## Authentication
    All protected endpoints require an API Key passed in the `X-API-Key` header.
    Key format: `inv_live_<hash>`
    """,
    version=__version__,
    lifespan=lifespan,
    contact={
        "name": "Invario Engineering",
        "url": "https://invario.finance",
    },
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.add_middleware(TelemetryMiddleware)

app.include_router(router)
app.add_route("/metrics", metrics_endpoint)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
