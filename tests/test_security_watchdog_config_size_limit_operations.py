from pathlib import Path

from taipanstack.core.result import Err
from taipanstack.resilience.watchdogs.config_watcher import _hash_file, _load_file_data


def test_security_watchdog_config_size_limit_operations_config_watcher_hash_file_size_limit(
    tmp_path: Path,
) -> None:
    """Test that _hash_file respects MAX_CONFIG_FILE_SIZE."""
    # We patch MAX_CONFIG_FILE_SIZE to make the test fast
    import taipanstack.resilience.watchdogs.config_watcher as cw

    original_size = cw.MAX_CONFIG_FILE_SIZE
    try:
        cw.MAX_CONFIG_FILE_SIZE = 10
        f = tmp_path / "large_file.json"
        f.write_text("a" * 15)

        result = _hash_file(f)
        assert isinstance(result, Err)
        assert isinstance(result.err_value, ValueError)
        assert "exceeds max size" in str(result.err_value)
    finally:
        cw.MAX_CONFIG_FILE_SIZE = original_size


def test_security_watchdog_config_size_limit_operations_config_watcher_load_file_data_size_limit(
    tmp_path: Path,
) -> None:
    """Test that _load_file_data respects MAX_CONFIG_FILE_SIZE."""
    import taipanstack.resilience.watchdogs.config_watcher as cw

    original_size = cw.MAX_CONFIG_FILE_SIZE
    try:
        cw.MAX_CONFIG_FILE_SIZE = 10
        f = tmp_path / "large_file.json"
        f.write_text("a" * 15)

        result = _load_file_data(f)
        assert isinstance(result, Err)
        assert isinstance(result.err_value, ValueError)
        assert "exceeds max size" in str(result.err_value)
    finally:
        cw.MAX_CONFIG_FILE_SIZE = original_size
