import asyncio
from uuid import uuid4
from pydantic import SecretStr

from app.secure_system import (
    InMemoryUserRepository,
    UserCreate,
    UserService,
    UserAlreadyExistsError,
    UserInDB
)
from taipanstack.core.result import Ok, Err

class SlowRepository(InMemoryUserRepository):
    def save(self, user: UserInDB) -> None:
        import time
        time.sleep(0.01) # block
        super().save(user)

async def main():
    repo = SlowRepository()
    service = UserService(repo)

    # Chaos test concurrency
    async def create_user(idx):
        u = UserCreate(
            username=f"user_{idx}",
            email=f"user{idx}@example.com",
            password=SecretStr("secure_password")
        )
        # Using executor to avoid blocking the event loop entirely
        return await asyncio.to_thread(service.create_user, u)

    tasks = [create_user(i) for i in range(100)]
    results = await asyncio.gather(*tasks)

    ok_count = sum(1 for r in results if isinstance(r, Ok))
    err_count = sum(1 for r in results if isinstance(r, Err))
    print(f"Created: {ok_count}, Errors: {err_count}")

asyncio.run(main())
