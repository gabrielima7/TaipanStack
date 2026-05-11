from pathlib import Path

path = Path("tests/test_optimizations_operations.py")
content = path.read_text()

# Ah! OptimizationProfile doesn't have `experimental_jit` and `experimental_free_threading`.
# Let's see what features `_apply_experimental` actually checks.
# Wait, it checks `if features.has_jit:` and `if features.has_free_threading:`
# It does NOT check `profile.experimental_jit`.
# It only checks `profile.enable_experimental`.

new_test = """
    def test_optimizations_apply_no_skipped(self) -> None:
        from taipanstack.core.optimizations import apply_optimizations, OptimizationProfile
        import sys

        class MockFeatures:
            has_jit = True
            has_free_threading = True
            has_gc_freeze = True

        from unittest.mock import patch
        with patch("taipanstack.core.optimizations.get_features", return_value=MockFeatures()):
            from dataclasses import replace
            from taipanstack.core.optimizations import OptimizationProfile
            profile = OptimizationProfile()
            profile = replace(profile, enable_perf_hints=True, enable_experimental=True)

            result = apply_optimizations(profile=profile, apply_gc=True, freeze_after=False)
            assert len(result.skipped) == 0
"""

import re
content = re.sub(r'    def test_optimizations_apply_no_skipped.*?(?=    def|$)', new_test.strip("\n") + "\n\n", content, flags=re.DOTALL)
path.write_text(content)
