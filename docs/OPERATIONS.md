# Invario Operations Guide

This guide is intended for Site Reliability Engineers (SREs) and System Administrators managing an Invario deployment.

## 🔐 Key Management

All API Keys are managed via the `manage.py` CLI utility.

### Prerequisite: Database Connection
The CLI needs access to the Postgres database.
- **Docker**: `docker-compose exec api ...` (Recommended)
- **Local**: `export DATABASE_URL=...` then `poetry run python ...`

### 1. Generating a Key
Create a new key for a client. The key is shown **once**.

```bash
python manage.py create-key --owner "ClientName" --scopes '{"write": true}'
```

**Output**:
```text
✅ API Key Created for 'ClientName'
🔑 Key: inv_live_aBcDeFgHiJkLmNoPqRsTuVwXyZ123456
⚠️  SAVE THIS KEY NOW. It will not be shown again.
```

### 2. Revoking Access
Immediate revocation of all active keys for a specific owner.

```bash
python manage.py revoke-key --owner "ClientName"
```

---

## 🚨 Disaster Recovery (DR)

### Scenario: Ledger Corruption
**Symptom**: `invario_ledger_integrity_status` metric drops to `0`. `GET /health` returns specific error about hash mismatch.

**Root Cause**:
- Database manipulation (row update/delete) bypassing the API.
- Bit rot or disk failure.

**Recovery Procedure**:
1. **Quarantine**: Stop the Ingestion API immediately to prevent adding on top of a broken chain.
   ```bash
   docker-compose stop api
   ```
2. **Audit**: connect to DB and identify the first broken link.
   ```sql
   SELECT * FROM ledger_entries ORDER BY sequence_number DESC LIMIT 10;
   ```
3. **Forensics**: Compare `entry_hash` vs. re-calculated hash of the `transaction_id`.
4. **Resolution (Last Resort)**: If data was tampered with, restore from the last known good backup. **Invario does not support modifying the ledger to "fix" hashes.**

---

## 📜 Logging & Observability

### Log Format
Invario uses structured JSON logging.

**Example**:
```json
{
  "timestamp": "2023-10-27T10:00:00Z",
  "level": "info",
  "event": "transaction_processed",
  "correlation_id": "req_123abc",
  "transaction_id": "uuid-v4...",
  "amount": "100.50",
  "currency": "BRL"
}
```

### Critical Events to Monitor
- `level="error"`: Any application error.
- `event="integrity_check_failed"`: **CRITICAL**. Ledger is broken.
- `event="batch_rejected"`: High frequency might indicate a client sending bad data.

### Prometheus Metrics
Exposed at `:8000/metrics`.

| Metric | Type | Description |
|--------|------|-------------|
| `invario_transactions_total` | Counter | Total transactions ingested. |
| `invario_ledger_integrity_status` | Gauge | **1** = Healthy, **0** = Corrupted. Alert immediately on 0. |

---

## 🧹 Maintenance

### Database Migrations
Always apply migrations before starting the new API version.

```bash
# Docker
docker-compose run --rm api alembic upgrade head
```

### Backup Strategy
Standard PostgreSQL backup (`pg_dump`) is sufficient. Ensure `ledger_head`, `ledger_entries`, and `transactions` are backed up consistently (in the same transaction snapshot).
