import re

with open("tests/test_optimizations.py", "r") as f:
    content = f.read()

# Fix the test
content = re.sub(
    r"def test_apply_optimizations_errors_branch\(\) -> None:.*",
    """def test_apply_optimizations_errors_branch() -> None:
    \"\"\"Test apply_optimizations when errors list is populated.\"\"\"
    from src.taipanstack.core.optimizations import apply_optimizations, get_optimization_profile
    import unittest.mock

    config = get_optimization_profile(force_refresh=True)

    def mock_gc_tuning(profile, applied, errors):
        errors.append("test error")

    with unittest.mock.patch("src.taipanstack.core.optimizations._apply_gc_tuning", side_effect=mock_gc_tuning):
         result = apply_optimizations(profile=config) # type: ignore
         assert "test error" in result.errors
""",
    content, flags=re.DOTALL
)

with open("tests/test_optimizations.py", "w") as f:
    f.write(content)
