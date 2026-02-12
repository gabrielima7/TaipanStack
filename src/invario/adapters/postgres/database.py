"""
Database connection setup for Invario.

Configures AsyncEngine and AsyncSession factory for PostgreSQL.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

import os

# Default to Docker Compose service name if running inside container, else localhost
DEFAULT_URL = "postgresql+asyncpg://postgres:password@localhost:5432/invario"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_URL)


class Database:
    """Database connection manager."""

    def __init__(self, url: str = DATABASE_URL) -> None:
        """Initialize database engine."""
        self.engine = create_async_engine(
            url,
            echo=False,
            future=True,
            pool_pre_ping=True,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    async def close(self) -> None:
        """Close database connection."""
        await self.engine.dispose()

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Dependency for FastAPI to get a session."""
        async with self.session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


# Global database instance
db = Database()
