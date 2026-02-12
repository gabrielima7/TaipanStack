# Multi-stage Dockerfile for Invario
# Stage 1: Builder
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry

# Copy project files
COPY pyproject.toml poetry.lock ./

# Export requirements.txt without hashes (safer for some builds, though less secure)
# or configure poetry to install in .venv
RUN poetry config virtualenvs.in-project true && \
    poetry install --only main --no-root --no-interaction --no-ansi

# Stage 2: Runtime
FROM python:3.12-slim AS runtime

# Create non-root user
RUN groupadd -r invario && useradd -r -g invario invario

WORKDIR /app

# Install runtime dependencies (libpq for asyncpg/psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    postgresql-client \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Copy virtualenv from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY src ./src
COPY alembic ./alembic
COPY alembic.ini .
COPY pyproject.toml .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/app/src:$PYTHONPATH"

# Change ownership
RUN chown -R invario:invario /app

# Switch to non-root user
USER invario

EXPOSE 8000

# Entrypoint will be defined in docker-compose or via separate script
CMD ["uvicorn", "invario.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
