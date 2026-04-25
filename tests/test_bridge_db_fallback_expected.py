import importlib
import sys
import types
from unittest.mock import patch


def test_bridge_db_fallback_sqlalchemy_expected():
    original_sa = sys.modules.get("sqlalchemy")
    original_sa_ext = sys.modules.get("sqlalchemy.ext.asyncio")

    try:
        if "sqlalchemy" in sys.modules:
            del sys.modules["sqlalchemy"]
        if "sqlalchemy.ext.asyncio" in sys.modules:
            del sys.modules["sqlalchemy.ext.asyncio"]
        with patch.dict(
            sys.modules, {"sqlalchemy": None, "sqlalchemy.ext.asyncio": None}
        ):
            if "taipanstack.bridges.db_bridge" in sys.modules:
                del sys.modules["taipanstack.bridges.db_bridge"]
            import taipanstack.bridges.db_bridge

            importlib.reload(taipanstack.bridges.db_bridge)
            assert not taipanstack.bridges.db_bridge._HAS_SQLALCHEMY
    finally:
        if original_sa is not None:
            sys.modules["sqlalchemy"] = original_sa
        elif "sqlalchemy" in sys.modules:
            del sys.modules["sqlalchemy"]
        if original_sa_ext is not None:
            sys.modules["sqlalchemy.ext.asyncio"] = original_sa_ext
        elif "sqlalchemy.ext.asyncio" in sys.modules:
            del sys.modules["sqlalchemy.ext.asyncio"]


def test_bridge_db_fallback_redis_expected():
    original_redis = sys.modules.get("redis")
    original_redis_asyncio = sys.modules.get("redis.asyncio")

    try:
        if "redis" in sys.modules:
            del sys.modules["redis"]
        if "redis.asyncio" in sys.modules:
            del sys.modules["redis.asyncio"]
        with patch.dict(sys.modules, {"redis.asyncio": None, "redis": None}):
            if "taipanstack.bridges.db_bridge" in sys.modules:
                del sys.modules["taipanstack.bridges.db_bridge"]
            import taipanstack.bridges.db_bridge

            importlib.reload(taipanstack.bridges.db_bridge)
            assert not taipanstack.bridges.db_bridge._HAS_REDIS
    finally:
        if original_redis is not None:
            sys.modules["redis"] = original_redis
        elif "redis" in sys.modules:
            del sys.modules["redis"]
        if original_redis_asyncio is not None:
            sys.modules["redis.asyncio"] = original_redis_asyncio
        elif "redis.asyncio" in sys.modules:
            del sys.modules["redis.asyncio"]


def test_bridge_db_success_sqlalchemy_expected():
    original_sa = sys.modules.get("sqlalchemy")
    original_sa_ext = sys.modules.get("sqlalchemy.ext")
    original_sa_ext_asyncio = sys.modules.get("sqlalchemy.ext.asyncio")

    try:
        dummy_sa = types.ModuleType("sqlalchemy")
        dummy_sa.text = lambda x: x
        dummy_sa_ext = types.ModuleType("sqlalchemy.ext")
        dummy_sa_ext_asyncio = types.ModuleType("sqlalchemy.ext.asyncio")
        dummy_sa_ext_asyncio.AsyncSession = type("AsyncSession", (), {})

        with patch.dict(
            sys.modules,
            {
                "sqlalchemy": dummy_sa,
                "sqlalchemy.ext": dummy_sa_ext,
                "sqlalchemy.ext.asyncio": dummy_sa_ext_asyncio,
            },
        ):
            if "taipanstack.bridges.db_bridge" in sys.modules:
                del sys.modules["taipanstack.bridges.db_bridge"]
            import taipanstack.bridges.db_bridge

            importlib.reload(taipanstack.bridges.db_bridge)
            assert taipanstack.bridges.db_bridge._HAS_SQLALCHEMY
    finally:
        if original_sa is not None:
            sys.modules["sqlalchemy"] = original_sa
        elif "sqlalchemy" in sys.modules:
            del sys.modules["sqlalchemy"]
        if original_sa_ext is not None:
            sys.modules["sqlalchemy.ext"] = original_sa_ext
        elif "sqlalchemy.ext" in sys.modules:
            del sys.modules["sqlalchemy.ext"]
        if original_sa_ext_asyncio is not None:
            sys.modules["sqlalchemy.ext.asyncio"] = original_sa_ext_asyncio
        elif "sqlalchemy.ext.asyncio" in sys.modules:
            del sys.modules["sqlalchemy.ext.asyncio"]


def test_bridge_db_success_redis_expected():
    original_redis = sys.modules.get("redis")
    original_redis_asyncio = sys.modules.get("redis.asyncio")

    try:
        dummy_redis = types.ModuleType("redis")
        dummy_redis_asyncio = types.ModuleType("redis.asyncio")
        dummy_redis_asyncio.Redis = type("Redis", (), {})

        with patch.dict(
            sys.modules, {"redis": dummy_redis, "redis.asyncio": dummy_redis_asyncio}
        ):
            if "taipanstack.bridges.db_bridge" in sys.modules:
                del sys.modules["taipanstack.bridges.db_bridge"]
            import taipanstack.bridges.db_bridge

            importlib.reload(taipanstack.bridges.db_bridge)
            assert taipanstack.bridges.db_bridge._HAS_REDIS
    finally:
        if original_redis is not None:
            sys.modules["redis"] = original_redis
        elif "redis" in sys.modules:
            del sys.modules["redis"]
        if original_redis_asyncio is not None:
            sys.modules["redis.asyncio"] = original_redis_asyncio
        elif "redis.asyncio" in sys.modules:
            del sys.modules["redis.asyncio"]
