import importlib
import sys
from unittest.mock import patch


def test_db_bridge_fallback_sqlalchemy():
    if "taipanstack.bridges.db_bridge" in sys.modules:
        del sys.modules["taipanstack.bridges.db_bridge"]

    with patch.dict(sys.modules, {"sqlalchemy": None, "sqlalchemy.ext.asyncio": None}):
        import taipanstack.bridges.db_bridge

        importlib.reload(taipanstack.bridges.db_bridge)
        assert not taipanstack.bridges.db_bridge._HAS_SQLALCHEMY


def test_db_bridge_fallback_redis():
    if "taipanstack.bridges.db_bridge" in sys.modules:
        del sys.modules["taipanstack.bridges.db_bridge"]

    with patch.dict(sys.modules, {"redis.asyncio": None, "redis": None}):
        import taipanstack.bridges.db_bridge

        importlib.reload(taipanstack.bridges.db_bridge)
        assert not taipanstack.bridges.db_bridge._HAS_REDIS
