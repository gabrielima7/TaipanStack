"""API Integration Tests."""

from fastapi.testclient import TestClient
from invario.api.main import app
from invario.ledger.repository import InMemoryLedgerRepository
from invario.api.dependencies import get_ledger_repository, get_db_session

client = TestClient(app)

# Override dependency to use in-memory repo explicitly for testing
# (Though default behavior without env var is memory, explicit is better)
memory_repo = InMemoryLedgerRepository()

async def override_get_repo():
    return memory_repo

app.dependency_overrides[get_ledger_repository] = override_get_repo

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_ingest_csv_success():
    csv_content = """type,amount,currency,source_account,target_account,document,settlement_date,bank_code
credit,100.50,BRL,123,456,12345678901,2025-01-01,001"""

    files = {"file": ("test.csv", csv_content, "text/csv")}
    response = client.post("/v1/ingest", files=files)

    assert response.status_code == 201
    data = response.json()
    assert data["transactions_processed"] == 1
    assert data["filename"] == "test.csv"

def test_audit_ledger():
    response = client.get("/v1/ledger/audit")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["integrity_valid"] is True
    # Should have 1 entry from previous test (if state persists)
    # TestClient resets app state? No, memory_repo is global here.
    assert data["total_entries"] >= 1

def test_ingest_duplicate_rejection():
    # Try to ingest same file again
    csv_content = """type,amount,currency,source_account,target_account,document,settlement_date,bank_code
credit,100.50,BRL,123,456,12345678901,2025-01-01,001"""

    files = {"file": ("test.csv", csv_content, "text/csv")}
    response = client.post("/v1/ingest", files=files)

    # Should be 409 Conflict due to duplicate content hash
    assert response.status_code == 409

def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "invario_transactions_total" in response.text
    assert "invario_ledger_integrity_status" in response.text
