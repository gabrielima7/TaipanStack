import tempfile
from pathlib import Path

import pytest

from taipanstack.security.guards import SecurityError, guard_path_traversal


def test_fuzz_guard_symlink_loop_guard_path_traversal_symlink_loop_runtime_error_expected() -> (
    None
):
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        link1 = base / "link1"
        link2 = base / "link2"
        link1.symlink_to("link2")
        link2.symlink_to("link1")

        with pytest.raises(
            SecurityError, match=r"Invalid path|Symlinks are not allowed"
        ):
            guard_path_traversal(link1, base, allow_symlinks=False)
