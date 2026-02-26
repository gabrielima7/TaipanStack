# =============================================================================
# TaipanStack — Hardened Production Dockerfile
# =============================================================================
# Multi-stage build | Alpine runtime | Rootless | Healthcheck
# =============================================================================

# ── Stage 1: Builder ────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# Install Poetry (pinned version for reproducibility)
ENV POETRY_VERSION=2.1.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

RUN python -m pip install --no-cache-dir "poetry==${POETRY_VERSION}"

# Copy only dependency files first (cache-friendly layer)
COPY pyproject.toml poetry.lock ./

# Install production dependencies only (no dev)
RUN poetry install --only main --no-root --no-directory

# Copy source code and install the project itself
COPY src/ src/
COPY README.md LICENSE ./
RUN poetry install --only main


# ── Stage 2: Runtime (Alpine — minimal attack surface) ──────────────────────
FROM python:3.11-alpine AS runtime

# Security labels (OCI Image Spec)
LABEL org.opencontainers.image.title="TaipanStack" \
    org.opencontainers.image.description="Modular, secure, and scalable Python stack" \
    org.opencontainers.image.source="https://github.com/gabrielima7/TaipanStack" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.vendor="gabrielima7"

# Install only runtime system dependencies, then clean up
RUN apk add --no-cache \
    libgcc \
    libstdc++ \
    && rm -rf /var/cache/apk/*

# Create non-root user (UID 1000 — standard unprivileged)
RUN addgroup -g 1000 appgroup \
    && adduser -u 1000 -G appgroup -s /bin/sh -D appuser

# Copy virtualenv from builder (contains all installed packages)
COPY --chown=appuser:appgroup --from=builder /app/.venv /app/.venv

# Copy application source
COPY --chown=appuser:appgroup --from=builder /app/src /app/src

WORKDIR /app

# Set virtualenv on PATH so `python` resolves to the venv's interpreter
ENV PATH="/app/.venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

# Drop to non-root user
USER appuser

EXPOSE 8080

# Healthcheck — verify the library imports correctly
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import taipanstack; print('ok')" || exit 1

# Default entrypoint (override in compose / k8s)
ENTRYPOINT ["python"]
CMD ["-c", "import taipanstack; print(f'TaipanStack {taipanstack.__version__} ready')"]
