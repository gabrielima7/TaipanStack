from pathlib import Path

import pytest
from pydantic import BaseModel

from taipanstack.core.result import Err
from taipanstack.resilience.watchdogs.config_watcher import ConfigWatcher


class DummyConfig(BaseModel):
    foo: str


@pytest.mark.asyncio
async def test_chaos_config_watcher_extreme_callback_failure() -> None:
    """Chaos test: Ensure ConfigWatcher handles extreme callback failures gracefully."""

    def exploding_callback(model: BaseModel) -> None:
        raise SystemError("Chaos injected in success callback")

    def exploding_error_callback(exc: Exception) -> None:
        raise SystemError("Chaos injected in error callback")

    watcher = ConfigWatcher(
        config_paths=[Path("dummy.json")],
        config_model=DummyConfig,
        on_config_change=exploding_callback,
        on_validation_error=exploding_error_callback,
    )

    # Validate and apply usually calls the callback on success
    # However, this test will simulate failure to see if it bubbles up

    # We test _handle_validation_success and _handle_validation_failure
    with pytest.raises(SystemError, match="Chaos injected in success callback"):
        watcher._handle_validation_success(Path("dummy.json"), DummyConfig(foo="bar"))

    with pytest.raises(SystemError, match="Chaos injected in error callback"):
        watcher._handle_validation_failure(Path("dummy.json"), ValueError("test"))


@pytest.mark.asyncio
async def test_chaos_config_watcher_corrupted_file_type(tmp_path: Path) -> None:
    """Chaos test: Ensure ConfigWatcher handles reading a directory as a file."""

    watcher = ConfigWatcher(
        config_paths=[tmp_path],
        config_model=DummyConfig,
    )

    # Should return Err instead of crashing when reading a directory
    result = watcher._validate_and_apply(tmp_path)
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
