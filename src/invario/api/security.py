from hashlib import sha256
from typing import Annotated

from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from invario.adapters.postgres.models import ApiKeyModel
from invario.api.dependencies import get_db_session as get_db

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(
    api_key: Annotated[str | None, Security(API_KEY_HEADER)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApiKeyModel:
    """Validate API Key and return the owner model."""
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing API Key header (X-API-Key)",
        )

    # Calculate SHA-256 hash of the provided key
    key_hash = sha256(api_key.encode()).hexdigest()

    # Query DB for active key
    result = await db.execute(
        select(ApiKeyModel).where(
            ApiKeyModel.key_hash == key_hash,
            ApiKeyModel.is_active == True  # noqa: E712
        )
    )
    api_key_record = result.scalar_one_or_none()

    if not api_key_record:
        raise HTTPException(
            status_code=403,
            detail="Invalid or inactive API Key",
        )

    return api_key_record
