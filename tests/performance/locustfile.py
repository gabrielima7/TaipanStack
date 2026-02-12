import random
import uuid
from locust import HttpUser, task, between, events

# Test Data Constants
VALID_HEADER = "header,1,20230101,INVARIO"
VALID_TRAILER = "trailer,1,100.00"

# Helper to generate a valid transaction line
def generate_valid_csv_content(batch_size=10) -> str:
    lines = [VALID_HEADER]
    total = 0.0
    for i in range(batch_size):
        # type, amount, currency, date, holder_doc, bank_code, integration_id
        amount = round(random.uniform(10.0, 1000.0), 2)
        total += amount
        # Unique integration ID to ensure no accidental duplicates
        integration_id = uuid.uuid4()
        line = f"2,{amount},BRL,2023-01-01,12345678909,001,{integration_id}"
        lines.append(line)

    lines.append(f"trailer,{batch_size},{total:.2f}")
    return "\n".join(lines)

# Helper to generate invalid/fraudulent content
def generate_fraud_content() -> str:
    # Invalid currency and negative amount
    return "header,1,20230101,INVARIO\n2,-500.00,XXX,2100-01-01,INVALID_DOC,000,fake_id\ntrailer,1,-500.00"

class InvarioUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def ingest_high_throughput(self):
        """Scenario 1: High Throughput - Valid CSVs."""
        content = generate_valid_csv_content(batch_size=50)
        files = {'file': ('valid_batch.csv', content, 'text/csv')}
        self.client.post("/v1/ingest", files=files, name="/v1/ingest (Valid)")

    @task(1)
    def ingest_fraud_storm(self):
        """Scenario 2: Fraud Storm - Invalid Data."""
        content = generate_fraud_content()
        files = {'file': ('fraud.csv', content, 'text/csv')}
        # Expecting 422 Unprocessable Entity
        with self.client.post("/v1/ingest", files=files, catch_response=True, name="/v1/ingest (Fraud)") as response:
            if response.status_code == 422:
                response.success()
            elif response.status_code != 422:
                response.failure(f"Expected 422, got {response.status_code}")

    @task(1)
    def double_spending_attack(self):
        """Scenario 3: Double Spending - Resending same file."""
        # Create a file with specific ID
        integration_id = str(uuid.uuid4())
        content = f"header,1,20230101,INVARIO\n2,100.00,BRL,2023-01-01,12345678909,001,{integration_id}\ntrailer,1,100.00"
        files = {'file': ('replay.csv', content, 'text/csv')}

        # First attempt: Should succeed
        with self.client.post(
            "/v1/ingest",
            files=files,
            name="/v1/ingest (Double Spend - 1st)",
            catch_response=True
        ) as response:
            if response.status_code not in [201, 409]: # 409 if execution is super fast and previous loop sent it? Unlikely with new UUID.
                 response.failure(f"1st attempt failed: {response.status_code}")

        # Second attempt: Should fail with 409 Conflict
        # Re-upload same content
        files_replay = {'file': ('replay.csv', content, 'text/csv')}
        with self.client.post("/v1/ingest", files=files_replay, catch_response=True, name="/v1/ingest (Double Spend - 2nd)") as response:
            if response.status_code == 409:
                response.success()
            else:
                response.failure(f"Replay allowed! Expected 409, got {response.status_code}")

    @task(1)
    def health_check(self):
        """Monitor system health."""
        self.client.get("/health", name="/health")

