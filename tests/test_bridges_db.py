import pytest
from unittest.mock import patch
import sys
import types

def test_db_bridge_imports_successful():
    mock_sa = types.ModuleType("sqlalchemy")
    mock_sa.text = types.ModuleType("sqlalchemy.text")
    mock_sa_ext = types.ModuleType("sqlalchemy.ext")
    mock_sa_ext.asyncio = types.ModuleType("sqlalchemy.ext.asyncio")
    mock_sa_ext.asyncio.AsyncSession = type("AsyncSession", (), {})

    mock_redis = types.ModuleType("redis")
    mock_redis.asyncio = types.ModuleType("redis.asyncio")

    with patch.dict(sys.modules, {
        "sqlalchemy": mock_sa,
        "sqlalchemy.ext": mock_sa_ext,
        "sqlalchemy.ext.asyncio": mock_sa_ext.asyncio,
        "redis": mock_redis,
        "redis.asyncio": mock_redis.asyncio,
    }):
        if "taipanstack.bridges.db_bridge" in sys.modules:
            del sys.modules["taipanstack.bridges.db_bridge"]

        import taipanstack.bridges.db_bridge as db_bridge
        assert db_bridge._HAS_SQLALCHEMY is True
        assert db_bridge._HAS_REDIS is True

def test_db_bridge_imports_missing():
    with patch.dict(sys.modules, {"sqlalchemy": None, "redis.asyncio": None}):
        if "taipanstack.bridges.db_bridge" in sys.modules:
            del sys.modules["taipanstack.bridges.db_bridge"]
        import taipanstack.bridges.db_bridge as db_bridge
        assert db_bridge._HAS_SQLALCHEMY is False
        assert db_bridge._HAS_REDIS is False
