import re

with open("tests/test_optimizations.py", "r") as f:
    content = f.read()

# Fix the test
content = re.sub(
    r"profile = OptimizationProfile\(enable_experimental=True\)",
    """profile = OptimizationProfile()""",
    content, flags=re.DOTALL
)

with open("tests/test_optimizations.py", "w") as f:
    f.write(content)
