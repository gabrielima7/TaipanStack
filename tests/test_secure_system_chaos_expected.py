import threading
from uuid import uuid4

from pydantic import SecretStr
from src.app.secure_system import InMemoryUserRepository, UserCreate, UserService
from src.taipanstack.core.result import Ok
from src.taipanstack.resilience.circuit_breaker import circuit_breaker


def test_secure_system_concurrent_chaos_expected():
    repo = InMemoryUserRepository()
    service = UserService(repo)

    @circuit_breaker(failure_threshold=3, timeout=0.1)
    def create_user_api(i):
        user_data = UserCreate(
            username=f"user_{i}_{uuid4().hex[:6]}",
            email=f"user_{i}@example.com",
            password=SecretStr("StrongPass123!"),
        )
        return service.create_user(user_data)

    results = []
    results_lock = threading.Lock()

    def worker(worker_id):
        for i in range(20):
            try:
                res = create_user_api(worker_id * 100 + i)
                with results_lock:
                    results.append(res)
            except Exception as e:
                with results_lock:
                    results.append(e)

    threads = []
    for i in range(10):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    successes = sum(1 for r in results if isinstance(r, Ok))
    assert successes > 0, "No users were created successfully"
    assert len(results) == 200, "Not all concurrent attempts finished"
