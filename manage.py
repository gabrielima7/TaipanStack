#!/usr/bin/env python3
"""
Management CLI for Invario.

Usage:
    python manage.py create-key --owner "Client Name" [--scopes '{"read": true}']
    python manage.py revoke-key --owner "Client Name"
    python manage.py update-client --owner "Client Name" [--webhook "https://..."] [--pubkey "..."]
"""
import argparse
import asyncio
import json
import secrets
import sys
from datetime import datetime
from hashlib import sha256
from uuid import uuid4

from sqlalchemy import update
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from invario.adapters.postgres.models import ApiKeyModel
from invario.adapters.postgres.database import DATABASE_URL

# Setup DB connection
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def create_key(owner: str, scopes: dict) -> None:
    """Generate and store a new API Key."""
    # Generate secure random key
    raw_key = f"inv_live_{secrets.token_urlsafe(32)}"
    key_hash = sha256(raw_key.encode()).hexdigest()

    async with AsyncSessionLocal() as session:
        new_key = ApiKeyModel(
            id=uuid4(),
            key_hash=key_hash,
            owner=owner,
            is_active=True,
            scopes=scopes,
            created_at=datetime.utcnow(),
        )
        session.add(new_key)
        await session.commit()

    print(f"\n✅ API Key Created for '{owner}'")
    print(f"🔑 Key: {raw_key}")
    print("⚠️  SAVE THIS KEY NOW. It will not be shown again.\n")


async def revoke_key(owner: str) -> None:
    """Revoke all active keys for an owner."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            update(ApiKeyModel)
            .where(ApiKeyModel.owner == owner, ApiKeyModel.is_active == True)
            .values(is_active=False)
        )
        await session.commit()

    if result.rowcount > 0:
        print(f"\n🚫 Revoked {result.rowcount} active keys for '{owner}'.\n")
    else:
        print(f"\nℹ️  No active keys found for '{owner}'.\n")


async def update_client(owner: str, webhook: str | None, pubkey: str | None) -> None:
    """Update client configuration (Webhook, GPG Key)."""
    values = {}
    if webhook:
        values["webhook_url"] = webhook
    if pubkey:
        values["gpg_public_key"] = pubkey

    if not values:
        print("Nothing to update.")
        return

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            update(ApiKeyModel)
            .where(ApiKeyModel.owner == owner, ApiKeyModel.is_active == True)
            .values(**values)
        )
        await session.commit()

    if result.rowcount > 0:
        print(f"\n✅ Updated {result.rowcount} keys for '{owner}'.\n")
    else:
        print(f"\n❌ No active keys found for '{owner}'.\n")


def main():
    parser = argparse.ArgumentParser(description="Invario Management CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # create-key
    create_parser = subparsers.add_parser("create-key", help="Create a new API Key")
    create_parser.add_argument("--owner", required=True, help="Name of the key owner")
    create_parser.add_argument("--scopes", default="{}", help="JSON string of scopes")

    # revoke-key
    revoke_parser = subparsers.add_parser("revoke-key", help="Revoke keys for an owner")
    revoke_parser.add_argument("--owner", required=True, help="Name of the key owner")

    # update-client
    update_parser = subparsers.add_parser("update-client", help="Update client config")
    update_parser.add_argument("--owner", required=True, help="Name of the key owner")
    update_parser.add_argument("--webhook", help="Webhook URL")
    update_parser.add_argument("--pubkey", help="GPG Public Key")

    args = parser.parse_args()

    if args.command == "create-key":
        try:
            scopes = json.loads(args.scopes)
        except json.JSONDecodeError:
            print("Error: --scopes must be valid JSON")
            sys.exit(1)
        asyncio.run(create_key(args.owner, scopes))

    elif args.command == "revoke-key":
        asyncio.run(revoke_key(args.owner))

    elif args.command == "update-client":
        asyncio.run(update_client(args.owner, args.webhook, args.pubkey))


if __name__ == "__main__":
    main()
