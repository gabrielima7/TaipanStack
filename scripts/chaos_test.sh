#!/bin/bash
set -e

echo "🔥 THE TREASURY FIRE DRILL - STARTING 🔥"

# 1. Start Environment
echo "[1/5] Starting Infrastructure..."

# Prefer poetry run podman-compose if available
if [ -f ".venv/bin/podman-compose" ]; then
    COMPOSE=".venv/bin/podman-compose"
    echo "Using .venv/bin/podman-compose"
elif poetry run podman-compose --version >/dev/null 2>&1; then
    COMPOSE="poetry run podman-compose"
    echo "Using poetry run podman-compose"
elif type podman-compose >/dev/null 2>&1; then
    COMPOSE="podman-compose"
    echo "Using global podman-compose"
elif type docker-compose >/dev/null 2>&1; then
    COMPOSE="docker-compose"
    echo "Using docker-compose"
else
    echo "Error: neither podman-compose nor docker-compose found."
    exit 1
fi

$COMPOSE up -d --build
echo "Waiting for services to be healthy..."
sleep 15 # Give time for postgres healthcheck/entrypoint

# 2. Start Load
echo "[2/5] Injecting Load (Locust)..."
# Run locust in background, headless, validation mode
# We use poetry run to ensure locust is available
poetry run locust -f tests/performance/locustfile.py --headless -u 10 -r 2 -t 30s --host http://localhost:8000 > locust_log.txt 2>&1 &
LOCUST_PID=$!
echo "Locust started with PID $LOCUST_PID. Bombarding API..."

sleep 10

# 3. The Chaos
echo "[3/5] 💥 KILLING DATABASE 💥"
# Find DB container using podman/docker directly with label filter or name match
# podman-compose often names containers as <project>_<service>_1
if command -v podman &> /dev/null; then
    # Try finding by label first (if podman-compose sets com.docker.compose.service)
    DB_CONTAINER=$(podman ps --format "{{.ID}}" --filter "label=io.podman.compose.service=db" | head -n 1)

    # Fallback to name match if label not found
    if [ -z "$DB_CONTAINER" ]; then
        DB_CONTAINER=$(podman ps --format "{{.ID}}" --filter "name=invario_db_1" | head -n 1)
    fi
else
    DB_CONTAINER=$(docker ps -q -f name=invario_db_1)
fi

echo "Found DB Container ID: $DB_CONTAINER"

if [ -z "$DB_CONTAINER" ]; then
    echo "Error: Could not find DB container. Aborting."
    exit 1
fi

# Use podman or docker command directly to kill
if command -v podman &> /dev/null; then
    podman kill $DB_CONTAINER
else
    docker kill $DB_CONTAINER
fi

echo "Database killed. API should start failing (503 or 500)."
sleep 5

# 4. Recovery
echo "[4/5] 🚑 Restarting Database..."
if command -v podman &> /dev/null; then
    podman start $DB_CONTAINER
    echo "Database started. restarting API to refresh connection pool..."

    # Find API container
    API_CONTAINER=$(podman ps --format "{{.ID}}" --filter "label=io.podman.compose.service=api" | head -n 1)
    if [ -z "$API_CONTAINER" ]; then
        API_CONTAINER=$(podman ps --format "{{.ID}}" --filter "name=invario_api_1" | head -n 1)
    fi

    if [ ! -z "$API_CONTAINER" ]; then
        podman restart $API_CONTAINER
    else
        echo "Warning: API container not found for restart."
    fi
else
    docker start $DB_CONTAINER
    # Docker equivalent (assuming standard compose naming)
    docker restart invario_api_1 || true
fi
echo "System recovering..."
sleep 30 # Wait for recovery (DB startup + API reconnect)

# 5. Audit
echo "[5/5] 🕵️ Auditing System Health..."
HEALTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)
METRICS=$(curl -s http://localhost:8000/metrics)
INTEGRITY=$(echo "$METRICS" | grep "invario_ledger_integrity_status" | awk '{print $2}')

echo "---------------------------------------------------"
echo "Health Check HTTP Code: $HEALTH_STATUS"
echo "Ledger Integrity Status: $INTEGRITY"
echo "---------------------------------------------------"

if [ "$HEALTH_STATUS" -eq 200 ] && [ "$INTEGRITY" == "1.0" ]; then
    echo "✅ TEST PASSED: System recovered and Ledger is intact."
    exit 0
else
    echo "❌ TEST FAILED: System did not recover correctly."
    exit 1
fi
