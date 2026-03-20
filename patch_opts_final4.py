import re

with open("tests/test_optimizations.py", "r") as f:
    content = f.read()

# Fix the test
content = re.sub(
    r"config = OptimizationProfile\(enable_experimental=True\)",
    """from src.taipanstack.core.optimizations import get_optimization_profile
    config = get_optimization_profile()
    """,
    content, flags=re.DOTALL
)

with open("tests/test_optimizations.py", "w") as f:
    f.write(content)
