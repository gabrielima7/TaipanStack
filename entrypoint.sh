#!/bin/bash
set -e

# Wait for DB to be ready (though docker-compose depends_on healthcheck handles mostly)
# Double check with pg_isready if needed, or rely on alembic retry/wait logic if implemented.
# Docker compose healthcheck is usually sufficient.

# Alembic uses sync driver (psycopg2) for migrations, while app uses async (asyncpg).
# We need to provide the sync URL for alembic if env.py doesn't handle the switch (which it now does via async engine).
# However, env.py uses async engine now, so the asyncpg URL passed via env var is fine.

echo "Running database migrations..."
# Run migrations
alembic upgrade head

echo "Starting Invario API..."
exec uvicorn invario.api.main:app --host 0.0.0.0 --port 8000
