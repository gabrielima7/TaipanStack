import pytest
from unittest.mock import patch
import app.main

def test_greet():
    assert app.main.greet("Test") == "Hello, Test!"

@patch("app.main.logger")
def test_main(mock_logger):
    app.main.main()
    mock_logger.info.assert_called_once_with("Hello, World!")

def test_main_block():
    with patch("app.main.main") as mock_main:
        with patch.object(app.main, "__name__", "__main__"):
            # Since the module is already imported, the if block was evaluated
            # when __name__ was "app.main".
            # The only way to get coverage to see it evaluated as "__main__"
            # is to re-execute the module code using exec.
            import sys
            import runpy
            runpy.run_path(app.main.__file__, run_name="__main__")
