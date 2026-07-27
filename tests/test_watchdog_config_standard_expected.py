"""Tests for the ConfigWatcher and related utilities."""

import asyncio
import json
import unittest.mock
from pathlib import Path

import pytest
from pydantic import BaseModel, Field

from taipanstack.core.result import Err, Ok
from taipanstack.resilience.watchdogs.config_watcher import (
    ConfigWatcher,
    _hash_file,
    _load_file_data,
    _parse_env,
    _parse_json,
    validate_config,
)


class SampleConfig(BaseModel):
    """Minimal Pydantic model for testing."""

    host: str = Field(default="localhost")
    port: int = Field(default=8080)


class TestParseEnv:
    """Tests for _parse_env helper."""

    def test_watchdog_config_basic_parsing_expected(self) -> None:
        """Parse simple key=value pairs."""
        text = "HOST=localhost\nPORT=8080\n"
        result = _parse_env(text)
        assert result == {"HOST": "localhost", "PORT": "8080"}

    def test_watchdog_config_skips_comments_and_blanks_expected(self) -> None:
        """Comments and empty lines are ignored."""
        text = "# comment\n\nKEY=value\n"
        result = _parse_env(text)
        assert result == {"KEY": "value"}

    def test_watchdog_config_strips_quotes_expected(self) -> None:
        """Surrounding quotes are removed from values."""
        text = "KEY=\"quoted\"\nK2='single'\n"
        result = _parse_env(text)
        assert result["KEY"] == "quoted"
        assert result["K2"] == "single"

    def test_watchdog_config_skips_lines_without_equals_expected(self) -> None:
        """Lines without '=' are skipped."""
        text = "invalid_line\nKEY=value\n"
        result = _parse_env(text)
        assert result == {"KEY": "value"}


class TestParseJson:
    """Tests for _parse_json helper."""

    def test_watchdog_config_valid_json_expected(self) -> None:
        """Parses valid JSON object."""
        result = _parse_json('{"host": "db", "port": 5432}')
        assert isinstance(result, Ok)
        assert result.ok_value == {"host": "db", "port": 5432}

    def test_watchdog_config_invalid_json_expected(self) -> None:
        """Returns Err for malformed JSON."""
        result = _parse_json("{broken")
        assert isinstance(result, Err)

    def test_watchdog_config_non_dict_json_expected(self) -> None:
        """Returns Err when JSON root is not an object."""
        result = _parse_json("[1, 2, 3]")
        assert isinstance(result, Err)
        assert isinstance(result.err_value, TypeError)


class TestHashFile:
    """Tests for _hash_file helper."""

    def test_watchdog_config_hash_existing_file_expected(self, tmp_path: Path) -> None:
        """Returns Ok with hash for existing file."""
        f = tmp_path / "test.txt"
        f.write_text("hello")
        result = _hash_file(f)
        assert isinstance(result, Ok)
        assert len(result.ok_value) == 64  # SHA-256 hex digest

    def test_watchdog_config_hash_missing_file_expected(self, tmp_path: Path) -> None:
        """Returns Err for missing file."""
        result = _hash_file(tmp_path / "missing.txt")
        assert isinstance(result, Err)
        assert isinstance(result.err_value, OSError)


class TestLoadFileData:
    """Tests for _load_file_data helper."""

    def test_watchdog_config_load_json_file_expected(self, tmp_path: Path) -> None:
        """Loads and parses a .json file."""
        f = tmp_path / "config.json"
        f.write_text(json.dumps({"host": "db"}))
        result = _load_file_data(f)
        assert isinstance(result, Ok)
        assert result.ok_value["host"] == "db"

    def test_watchdog_config_load_env_file_expected(self, tmp_path: Path) -> None:
        """Loads and parses a .env file."""
        f = tmp_path / ".env"
        f.write_text("HOST=db\nPORT=3306\n")
        result = _load_file_data(f)
        assert isinstance(result, Ok)
        assert result.ok_value["HOST"] == "db"

    def test_watchdog_config_unsupported_extension_expected(
        self, tmp_path: Path
    ) -> None:
        """Returns Err for unsupported file extensions."""
        f = tmp_path / "config.xml"
        f.write_text("<config/>")
        result = _load_file_data(f)
        assert isinstance(result, Err)
        assert "Unsupported" in str(result.err_value)

    def test_watchdog_config_missing_file_expected(self, tmp_path: Path) -> None:
        """Returns Err for missing file."""
        result = _load_file_data(tmp_path / "nope.json")
        assert isinstance(result, Err)
        assert isinstance(result.err_value, OSError)


class TestValidateConfig:
    """Tests for validate_config."""

    def test_watchdog_config_valid_data_expected(self) -> None:
        """Returns Ok(model) for valid data."""
        result = validate_config({"host": "db", "port": 5432}, SampleConfig)
        assert isinstance(result, Ok)
        val = result.ok_value
        assert isinstance(val, SampleConfig)
        assert val.host == "db"
        assert val.port == 5432

    def test_watchdog_config_invalid_data_expected(self) -> None:
        """Returns Err for data that fails validation."""
        result = validate_config({"port": "not_a_number"}, SampleConfig)
        assert isinstance(result, Err)


class TestConfigWatcher:
    """Tests for the ConfigWatcher background task."""

    @pytest.mark.asyncio
    async def test_watchdog_config_start_stop_lifecycle(self, tmp_path: Path) -> None:
        """Watcher can be started and stopped."""
        f = tmp_path / "config.json"
        f.write_text(json.dumps({"host": "a", "port": 1}))

        watcher = ConfigWatcher(
            config_paths=[f],
            config_model=SampleConfig,
            interval=0.05,
        )
        result = await watcher.start()
        assert isinstance(result, Ok)
        assert watcher.is_running

        await asyncio.sleep(0.1)
        await watcher.stop()
        assert not watcher.is_running

    @pytest.mark.asyncio
    async def test_watchdog_config_detects_file_change(self, tmp_path: Path) -> None:
        """Callback fires when a config file changes."""
        f = tmp_path / "config.json"
        f.write_text(json.dumps({"host": "old", "port": 1}))

        changes: list[BaseModel] = []
        watcher = ConfigWatcher(
            config_paths=[f],
            config_model=SampleConfig,
            interval=0.05,
            on_config_change=changes.append,
        )

        # First start — records initial hash
        await watcher.start()
        await asyncio.sleep(0.1)

        # Modify file
        f.write_text(json.dumps({"host": "new", "port": 2}))
        await asyncio.sleep(0.2)
        await watcher.stop()

        assert len(changes) >= 1
        model = changes[-1]
        assert isinstance(model, SampleConfig)
        assert model.host == "new"

    @pytest.mark.asyncio
    async def test_watchdog_config_invalid_config_calls_error_callback(
        self, tmp_path: Path
    ) -> None:
        """Validation error callback fires on bad config."""
        f = tmp_path / "config.json"
        f.write_text(json.dumps({"host": "ok", "port": 1}))

        errors: list[Exception] = []
        watcher = ConfigWatcher(
            config_paths=[f],
            config_model=SampleConfig,
            interval=0.05,
            on_validation_error=errors.append,
        )

        await watcher.start()
        await asyncio.sleep(0.1)

        # Write invalid data
        f.write_text(json.dumps({"port": "bad"}))
        await asyncio.sleep(0.2)
        await watcher.stop()

        assert len(errors) >= 1

    @pytest.mark.asyncio
    async def test_watchdog_config_missing_file_does_not_crash(
        self, tmp_path: Path
    ) -> None:
        """A watched file that disappears is handled gracefully."""
        f = tmp_path / "will_vanish.json"
        f.write_text(json.dumps({"host": "x", "port": 1}))

        watcher = ConfigWatcher(
            config_paths=[f],
            config_model=SampleConfig,
            interval=0.05,
        )
        await watcher.start()
        await asyncio.sleep(0.1)

        f.unlink()
        await asyncio.sleep(0.15)
        await watcher.stop()

    def test_watchdog_config_detect_changes_no_change_expected(
        self, tmp_path: Path
    ) -> None:
        """No changed paths when files haven't been modified."""
        f = tmp_path / "config.json"
        f.write_text(json.dumps({"host": "a", "port": 1}))

        watcher = ConfigWatcher(
            config_paths=[f],
            config_model=SampleConfig,
        )

        # First call seeds the hashes
        result1 = watcher._detect_changes()
        assert isinstance(result1, Ok)
        assert result1.ok_value == []

        # Second call — no change
        result2 = watcher._detect_changes()
        assert isinstance(result2, Ok)
        assert result2.ok_value == []

    def test_watchdog_config_validate_and_apply_with_env_file_expected(
        self, tmp_path: Path
    ) -> None:
        """Hot-reload works for .env files."""

        class EnvConfig(BaseModel):
            """Simple env config."""

            HOST: str = "localhost"

        f = tmp_path / ".env"
        f.write_text("HOST=myhost\n")

        changes: list[BaseModel] = []
        watcher = ConfigWatcher(
            config_paths=[f],
            config_model=EnvConfig,
            on_config_change=changes.append,
        )
        result = watcher._validate_and_apply(f)
        assert isinstance(result, Ok)
        assert len(changes) == 1

    def test_watchdog_config_validate_and_apply_missing_file_expected(
        self, tmp_path: Path
    ) -> None:
        """_validate_and_apply returns Err when file can't be loaded."""
        watcher = ConfigWatcher(
            config_paths=[],
            config_model=SampleConfig,
        )
        result = watcher._validate_and_apply(tmp_path / "nonexistent.json")
        assert isinstance(result, Err)
        assert isinstance(result.err_value, OSError)

    def test_watchdog_config_validate_and_apply_invalid_without_error_callback(
        self, tmp_path: Path
    ) -> None:
        """No crash when validation fails and on_validation_error is None."""
        f = tmp_path / "config.json"
        f.write_text(json.dumps({"port": "not_a_number"}))

        watcher = ConfigWatcher(
            config_paths=[f],
            config_model=SampleConfig,
            # No on_validation_error callback
        )
        result = watcher._validate_and_apply(f)
        assert isinstance(result, Err)

    def test_watchdog_config_validate_and_apply_valid_without_change_callback_expected(
        self, tmp_path: Path
    ) -> None:
        """No crash when config is valid and on_config_change is None."""
        f = tmp_path / "config.json"
        f.write_text(json.dumps({"host": "ok", "port": 1}))

        watcher = ConfigWatcher(
            config_paths=[f],
            config_model=SampleConfig,
            # No on_config_change callback
        )
        result = watcher._validate_and_apply(f)
        assert isinstance(result, Ok)


def test_watchdog_config_config_watcher_hash_err_branch_expected() -> None:
    from pydantic import BaseModel

    from taipanstack.resilience.watchdogs.config_watcher import ConfigWatcher

    class DummyConfig(BaseModel):
        val: int

    def mock_on_error(err):
        return None

    from pathlib import Path

    watcher = ConfigWatcher(
        config_paths=[Path("nonexistent_file_xyz.json")],
        config_model=DummyConfig,
        on_validation_error=mock_on_error,
    )
    # _detect_changes calls _hash_file, which returns Err on missing file
    # This covers the Err branch of match hash_result:
    watcher._detect_changes()


def test_watchdog_config_config_watcher_validate_and_apply_err_without_error_callback_branch() -> (
    None
):
    import json

    from pydantic import BaseModel

    from taipanstack.resilience.watchdogs.config_watcher import ConfigWatcher

    class DummyConfig(BaseModel):
        val: int

    from pathlib import Path

    with Path("test_bad_validate.json").open("w") as f:
        json.dump({"val": "not an int"}, f)

    from pathlib import Path

    watcher = ConfigWatcher(
        config_paths=[Path("test_bad_validate.json")],
        config_model=DummyConfig,
        on_validation_error=None,
    )
    watcher._validate_and_apply(Path("test_bad_validate.json"))
    Path("test_bad_validate.json").unlink()


def test_watchdog_config_config_watcher_validate_and_apply_ok_without_change_callback_branch() -> (
    None
):
    import json

    from pydantic import BaseModel

    from taipanstack.resilience.watchdogs.config_watcher import ConfigWatcher

    class DummyConfig(BaseModel):
        val: int

    from pathlib import Path

    with Path("test_good_validate.json").open("w") as f:
        json.dump({"val": 1}, f)

    from pathlib import Path

    watcher = ConfigWatcher(
        config_paths=[Path("test_good_validate.json")],
        config_model=DummyConfig,
        on_config_change=None,
    )
    watcher._validate_and_apply(Path("test_good_validate.json"))
    Path("test_good_validate.json").unlink()


@pytest.mark.asyncio
async def test_watchdog_config_config_watcher_change_detection_error_coverage_expected() -> (
    None
):
    """Test config_watcher change detection error logging."""
    from unittest.mock import MagicMock, patch

    from taipanstack.resilience.watchdogs.config_watcher import ConfigWatcher

    class MockConfig(BaseModel): ...

    watcher = ConfigWatcher(config_paths=["foo.json"], config_model=MockConfig)
    watcher._detect_changes = MagicMock(return_value=Err(RuntimeError("mock error")))

    with patch(
        "taipanstack.resilience.watchdogs.config_watcher.logger.error"
    ) as mock_logger:
        with patch("asyncio.sleep", side_effect=asyncio.CancelledError) as mock_sleep:
            try:
                await watcher._run()
            except asyncio.CancelledError:
                assert mock_sleep.called
        mock_logger.assert_called_with(
            "Change detection failed: %s",
            watcher._detect_changes.return_value.err_value,
        )


def test_watchdog_config_hash_file_too_large_expected(tmp_path: Path) -> None:
    f = tmp_path / "large.txt"
    f.write_text("a" * 10)
    from taipanstack.resilience.watchdogs.config_watcher import _hash_file

    with unittest.mock.patch("pathlib.Path.stat") as mock_stat:
        mock_stat.return_value.st_size = 11 * 1024 * 1024
        result = _hash_file(f)
    assert isinstance(result, Err)
    assert "exceeds max size" in str(result.err_value)


def test_watchdog_config_load_file_too_large_expected(tmp_path: Path) -> None:
    f = tmp_path / "large.json"
    f.write_text("{}")
    from taipanstack.resilience.watchdogs.config_watcher import _load_file_data

    with unittest.mock.patch("pathlib.Path.stat") as mock_stat:
        mock_stat.return_value.st_size = 11 * 1024 * 1024
        result = _load_file_data(f)
    assert isinstance(result, Err)
    assert "exceeds max size" in str(result.err_value)
