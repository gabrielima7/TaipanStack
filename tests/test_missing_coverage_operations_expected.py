import importlib
import re
from unittest.mock import Mock, patch


def test_db_bridge_fallback_expected():
    import taipanstack.bridges.db_bridge

    with patch.dict("sys.modules", {"sqlalchemy": None, "redis": None}):
        importlib.reload(taipanstack.bridges.db_bridge)
        assert taipanstack.bridges.db_bridge._HAS_SQLALCHEMY is False
        assert taipanstack.bridges.db_bridge._HAS_REDIS is False

    importlib.reload(taipanstack.bridges.db_bridge)


def test_resource_watcher_fallback_expected():
    import taipanstack.resilience.watchdogs.resource_watcher

    with patch.dict("sys.modules", {"psutil": None}):
        importlib.reload(taipanstack.resilience.watchdogs.resource_watcher)
        assert taipanstack.resilience.watchdogs.resource_watcher._HAS_PSUTIL is False

    importlib.reload(taipanstack.resilience.watchdogs.resource_watcher)


def test_sanitizers_fallback_expected():
    from taipanstack.security import sanitizers

    mock_re = Mock()
    mock_re.sub.side_effect = re.error("mocked error")
    with patch("taipanstack.security.sanitizers._INVALID_FILENAME_CHARS_RE", mock_re):
        result = sanitizers.sanitize_filename("test.txt")
        assert result == "test.txt"
