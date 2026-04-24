import importlib
import sys
from unittest.mock import patch


def test_http_bridge_fallback_httpx():
    if "taipanstack.bridges.http_bridge" in sys.modules:
        del sys.modules["taipanstack.bridges.http_bridge"]

    with patch.dict(sys.modules, {"httpx": None}):
        import taipanstack.bridges.http_bridge

        importlib.reload(taipanstack.bridges.http_bridge)
        assert not taipanstack.bridges.http_bridge._HAS_HTTPX
