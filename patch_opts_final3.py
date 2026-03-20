import re

with open("tests/test_optimizations.py", "r") as f:
    content = f.read()

# Fix the test
content = re.sub(
    r"config = OptimizationProfile\(\)\n    object.__setattr__\(config, \"enable_gc_tuning\", True\)",
    """config = OptimizationProfile(enable_experimental=True)
    """,
    content, flags=re.DOTALL
)

with open("tests/test_optimizations.py", "w") as f:
    f.write(content)
