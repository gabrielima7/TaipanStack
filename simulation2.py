import asyncio
import threading
import time
from typing import Any
from uuid import uuid4
from pydantic import SecretStr

from app.secure_system import UserService, InMemoryUserRepository, UserCreate
from taipanstack.core.result import Ok, Err
from taipanstack.utils.logging import get_logger

logger = get_logger(__name__)

def test_user_creation_concurrency():
    repo = InMemoryUserRepository()
    service = UserService(repo)

    class MockUser:
        def __init__(self, username, email, id):
            self.username = username
            self.email = email
            self.id = id

    # Pre-populate with 100,000 users to test O(N) degradation
    for i in range(100000):
        repo._storage[uuid4()] = MockUser(f"old_{i}", f"old_{i}@x.com", uuid4()) # type: ignore

    barrier = threading.Barrier(100)

    def worker(i):
        barrier.wait()
        user = UserCreate(
            username=f"user_{i}",
            email=f"user_{i}@example.com",
            password=SecretStr("StrongP4ssword!")
        )
        service.create_user(user)

    threads = []

    start_time = time.time()
    for i in range(100):
        t = threading.Thread(target=worker, args=(i,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    end_time = time.time()
    print(f"Time taken for 100 concurrent creations with 100k existing users: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    test_user_creation_concurrency()
