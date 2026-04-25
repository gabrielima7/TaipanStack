import importlib
import sys
import types
from unittest.mock import patch


def test_bridge_http_fallback_httpx_expected():
    original_httpx = sys.modules.get("httpx")

    try:
        if "httpx" in sys.modules:
            del sys.modules["httpx"]
        with patch.dict(sys.modules, {"httpx": None}):
            if "taipanstack.bridges.http_bridge" in sys.modules:
                del sys.modules["taipanstack.bridges.http_bridge"]
            import taipanstack.bridges.http_bridge

            importlib.reload(taipanstack.bridges.http_bridge)
            assert not taipanstack.bridges.http_bridge._HAS_HTTPX
    finally:
        if original_httpx is not None:
            sys.modules["httpx"] = original_httpx
        elif "httpx" in sys.modules:
            del sys.modules["httpx"]


def test_bridge_http_success_httpx_expected():
    original_httpx = sys.modules.get("httpx")
    try:
        dummy_httpx = types.ModuleType("httpx")
        dummy_httpx.Response = type("Response", (), {})
        sys.modules["httpx"] = dummy_httpx
        if "taipanstack.bridges.http_bridge" in sys.modules:
            del sys.modules["taipanstack.bridges.http_bridge"]
        import taipanstack.bridges.http_bridge

        importlib.reload(taipanstack.bridges.http_bridge)
        assert taipanstack.bridges.http_bridge._HAS_HTTPX
    finally:
        if original_httpx is not None:
            sys.modules["httpx"] = original_httpx
        elif "httpx" in sys.modules:
            del sys.modules["httpx"]
