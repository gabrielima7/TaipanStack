"""
Dependency injection for Invario API.

Handles database sessions and repository selection based on configuration.
"""

import os
from collections.abc import AsyncGenerator, Callable
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from invario.adapters.postgres.database import db
from invario.adapters.postgres.repository import PostgresLedgerRepository
from invario.ledger.repository import InMemoryLedgerRepository, LedgerRepository

# Singleton in-memory repo for testing/dev if Postgres not active
_MEMORY_REPO = InMemoryLedgerRepository()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session."""
    # Only verify connection if we are planning to use it
    if os.getenv("STORAGE_TYPE", "postgres") == "postgres":
        async for session in db.get_session():
            yield session
    else:
        # Yield dummy session or raise error?
        # For memory repo, we don't need a session.
        # But Depends(get_db_session) might be called.
        # We can yield None or a mock if types allow.
        # However, PostgresLedgerRepository requires a session.
        yield None  # type: ignore


async def get_ledger_repository(
    session: Annotated[AsyncSession | None, Depends(get_db_session)],
) -> LedgerRepository:
    """Get the active ledger repository based on config."""
    storage_type = os.getenv("STORAGE_TYPE", "postgres")

    if storage_type == "postgres":
        if session is None:
            raise RuntimeError("Database session failed to initialize for postgres storage")
        return PostgresLedgerRepository(session)

    return _MEMORY_REPO


# Type alias for easy injection
LedgerRepoDep = Annotated[LedgerRepository, Depends(get_ledger_repository)]
