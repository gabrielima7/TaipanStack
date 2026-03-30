with open("tests/test_watchdog_config.py", "r") as f:
    code = f.read()

code = code.replace(
    'watcher = ConfigWatcher(["nonexistent_file_xyz.json"], DummyConfig, on_config_error=mock_on_error)',
    'from pathlib import Path\n    watcher = ConfigWatcher(config_paths=[Path("nonexistent_file_xyz.json")], config_model=DummyConfig, on_validation_error=mock_on_error)'
)
code = code.replace(
    'watcher = ConfigWatcher(["test_bad_validate.json"], DummyConfig, on_config_error=None)',
    'from pathlib import Path\n    watcher = ConfigWatcher(config_paths=[Path("test_bad_validate.json")], config_model=DummyConfig, on_validation_error=None)'
)
code = code.replace(
    'watcher = ConfigWatcher(["test_good_validate.json"], DummyConfig, on_config_change=None)',
    'from pathlib import Path\n    watcher = ConfigWatcher(config_paths=[Path("test_good_validate.json")], config_model=DummyConfig, on_config_change=None)'
)
code = code.replace(
    'watcher._validate_and_apply("test_bad_validate.json")',
    'watcher._validate_and_apply(Path("test_bad_validate.json"))'
)
code = code.replace(
    'watcher._validate_and_apply("test_good_validate.json")',
    'watcher._validate_and_apply(Path("test_good_validate.json"))'
)

with open("tests/test_watchdog_config.py", "w") as f:
    f.write(code)
