# Invario: Zero-Trust Financial Middleware

> **High-Integrity Settlement & Compliance Engine**

Invario is a specialized middleware designed to ingest, validate, and ledger financial transactions with cryptographic integrity. It acts as a Zero-Trust gateway between external partners and core banking systems, ensuring that only 100% compliant and valid data is processed.

## 🏗 Architecture

```mermaid
graph LR
    Client[External Client] -->|HTTPS + X-API-Key| API[Invario API]
    API -->|Validation Guards| Pipeline[Ingestion Pipeline]
    Pipeline -->|Valid Tx| Ledger[Cryptographic Ledger]
    Ledger -->|Hash Chain| DB[(PostgreSQL)]

    subgraph "Zero-Trust Core"
    Pipeline
    Ledger
    end
```

- **API Layer**: FastAPI with Async/Await.
- **Security**: API Key authentication (SHA-256 hashed).
- **Pipeline**: CNAB/CSV/JSON parsing with strict financial guards (CPF, ISO 4217, Idempotency).
- **Ledger**: Immutable, hash-chained transaction log (Blockchain-like integrity).

## 🚀 Quickstart

### Prerequisites
- Docker & Docker Compose (or Podman)
- Python 3.11+ (for local CLI usage)

### 1. Launch the Stack
```bash
docker-compose up -d
```
*This starts Postgres, the Invario API (port 8000), and Prometheus.*

### 2. Create an API Key
Generate a key for your local client using the management CLI inside the container:

```bash
docker-compose exec api python manage.py create-key --owner "LocalDev"
```
*> 🔑 Key: inv_live_... (Save this key!)*

### 3. Test the System
Check health (Public):
```bash
curl http://localhost:8000/health
```

Ingest a Transaction (Protected):
```bash
curl -X POST http://localhost:8000/v1/ingest \
  -H "X-API-Key: YOUR_KEY_HERE" \
  -F "file=@./samples/valid_transaction.csv"
```

## 📖 API Documentation

The interactive Swagger UI is available at:
**[http://localhost:8000/docs](http://localhost:8000/docs)**

1. Click **Authorize**.
2. Paste your API Key.
3. Try out the `/v1/ingest` or `/v1/ledger/audit` endpoints.

## ⚙️ Operations

### Key Management
Use the `manage.py` CLI to handle credentials.

**Create a Key**:
```bash
# Inside container
python manage.py create-key --owner "Partner Name" --scopes '{"write": true}'

# Local (requires env var)
export DATABASE_URL="postgresql+asyncpg://postgres:password@localhost:5432/invario"
poetry run python manage.py create-key --owner "Partner Name"
```

**Revoke a Key**:
```bash
python manage.py revoke-key --owner "Partner Name"
```

### Observability
- **Metrics**: `GET /metrics` (Prometheus format). Critical gauge: `invario_ledger_integrity_status` (1 = Healthy, 0 = Corrupted).
- **Logs**: JSON formatted structure logs via `structlog`. Look for `correlation_id` to trace requests.

### Disaster Recovery
If `invario_ledger_integrity_status` drops to `0`, the ledger is cryptographically broken.
**Procedure**:
1. Stop ingestion immediately.
2. Run audit: `curl ... /v1/ledger/audit`.
3. Check logs for "Hash Mismatch".
4. Consult `docs/RUNBOOK.md`.

## 🛡 Security
- **No Plaintext Keys**: Keys are stored as SHA-256 hashes.
- **Non-Root Containers**: Docker image runs as `invario` user.
- **Input Validation**: All inputs are treated as hostile until validated by Guards.

---
*Built with ❤️ by the Invario Team.*
