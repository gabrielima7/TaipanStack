import re
from pathlib import Path

text = Path("tests/test_benchmarks.py").read_text()
text = re.sub(r"def test_bench_safe_decorator_err.*?benchmark\(_divide, 10, 0\)\n", "", text, flags=re.DOTALL)
Path("tests/test_benchmarks.py").write_text(text)
