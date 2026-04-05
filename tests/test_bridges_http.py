import pytest
from unittest.mock import patch
import sys
import types

def test_http_bridge_imports_missing():
    with patch.dict(sys.modules, {"httpx": None}):
        if "taipanstack.bridges.http_bridge" in sys.modules:
            del sys.modules["taipanstack.bridges.http_bridge"]
        import taipanstack.bridges.http_bridge as http_bridge
        assert http_bridge._HAS_HTTPX is False

def test_http_bridge_imports_successful():
    mock_httpx = types.ModuleType("httpx")
    with patch.dict(sys.modules, {"httpx": mock_httpx}):
        if "taipanstack.bridges.http_bridge" in sys.modules:
            del sys.modules["taipanstack.bridges.http_bridge"]
        import taipanstack.bridges.http_bridge as http_bridge
        assert http_bridge._HAS_HTTPX is True
