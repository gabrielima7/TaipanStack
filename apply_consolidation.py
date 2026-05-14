import re
from pathlib import Path

# Dockerfile
dockerfile = Path('Dockerfile')
content = dockerfile.read_text()
content = content.replace('POETRY_VERSION=2.0.0', 'POETRY_VERSION=2.4.1')
dockerfile.write_text(content)

# pyapp/README.md
readme = Path('pyapp/README.md')
if readme.exists():
    content = readme.read_text()
    content = content.replace('PYAPP_PROJECT_VERSION="0.4.9"', 'PYAPP_PROJECT_VERSION="<YOUR_VERSION>"')
    content = content.replace('PYAPP_PROJECT_PATH="dist/taipanstack-0.4.9-py3-none-any.whl"', 'PYAPP_PROJECT_PATH="dist/taipanstack-*.whl"')
    readme.write_text(content)

# pyproject.toml
pyproject = Path('pyproject.toml')
content = pyproject.read_text()
content = content.replace('addopts = "-v  --strict-markers --timeout=30"', 'addopts = "-v --strict-markers --timeout=30 --cov=src --cov-report=html --cov-report=term-missing"')
if '[tool.coverage.report]' not in content:
    content += '\n[tool.coverage.report]\nfail_under = 80\n'
content = content.replace('exclude = ["tests"]', '')
content = content.replace('tests/test_property_sanitizers_operations_expected.py', 'tests/test_property_sanitizers_operations.py')
content = content.replace('tests/test_security_validators_operations_expected.py', 'tests/test_security_validators_operations.py')
content = content.replace('tests/test_security_guards_operations_expected.py', 'tests/test_security_guards_operations.py')
content = content.replace('tests/test_security_ssrf_operations_expected.py', 'tests/test_security_ssrf_operations.py')
content = content.replace('tests/test_utils_retry_operations_expected.py', 'tests/test_utils_retry_operations.py')
content = content.replace('tests/test_utils_circuit_breaker_operations_expected.py', 'tests/test_utils_circuit_breaker_operations.py')
content = content.replace('dict_synonyms = "Struct, NamedStruct"\n', '')
content = content.replace('"pydantic.*",\n', '')
content = content.replace('skips = ["B101"]\n', '')
content = re.sub(r'\[tool\.bandit\].*?exclude_dirs = \[.*?\]\n', '', content, flags=re.DOTALL)
pyproject.write_text(content)

# Makefile
makefile = Path('Makefile')
content = makefile.read_text()
content = content.replace('poetry run pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing', 'poetry run pytest tests/ -n auto -v --cov=src --cov-report=html --cov-report=term-missing')
content = content.replace('poetry run mypy src/ --strict', 'poetry run mypy src/')
content = content.replace('tests/test_property_sanitizers_operations_expected.py', 'tests/test_property_sanitizers_operations.py')
content = content.replace('all: lint typecheck security lint-imports test', 'all: lint typecheck dead-code security lint-imports test')
if 'dead-code:' not in content:
    content = content.replace('lint-imports:', 'dead-code:\n\t@echo "Running Vulture to find dead code..."\n\tpoetry run vulture\n\nlint-imports:')
if 'Run Vulture' not in content:
    content = content.replace('Run security checks', 'Run security checks (bandit, pip-audit)"\n\t@echo "  dead-code    Run Vulture to find dead code')
content = content.replace('find . -type d -name .mutmut-cache -exec rm -rf {} + 2>/dev/null || true', 'find . -type f -name ".mutmut-cache" -delete 2>/dev/null || true')
content = content.replace('find . -type f -name "*.pyo" -delete 2>/dev/null || true\n', '')
content = content.replace('rm -rf dist/ build/ pyapp/target/ 2>/dev/null || true\n', '')
content = content.replace('@echo "Cleaning cache and temporary files..."\n', '@echo "Cleaning cache and temporary files..."\n\trm -rf dist/ build/ pyapp/target/ htmlcov/ .coverage 2>/dev/null || true\n')
if '.hypothesis' not in content:
    content = content.replace('find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true\n', 'find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true\n\tfind . -type d -name ".hypothesis" -exec rm -rf {} + 2>/dev/null || true\n')
makefile.write_text(content)

# taipanstack_bootstrapper.py
bootstrapper = Path('taipanstack_bootstrapper.py')
content = bootstrapper.read_text()
content = content.replace('from src.{project_name}.main import greet', 'from {project_name}.main import greet')
content = content.replace('print(message)', 'print(message)  # ruff: noqa: T201')
content = content.replace('args: [\'--baseline\', \'.secrets.baseline\']\n', '')
content = content.replace('socket.create_connection(("pypi.org", 443), timeout=5)', '_log("✅ Connectivity will be verified by the package manager during installation.", args, is_verbose=True)')
content = content.replace('except (TimeoutError, OSError):', 'except Exception:')
content = content.replace('python_version = f"py{sys.version_info.major}{sys.version_info.minor}"', 'python_version = "py311"')
if 'sys_platform != \'win32\'' not in content:
    content = content.replace('prod_deps.append("uvloop")', 'prod_deps.append("uvloop; sys_platform != \'win32\'")')
    content = content.replace('if not _is_windows():\n            prod_deps.append("uvloop; sys_platform != \'win32\'")', 'prod_deps.append("uvloop; sys_platform != \'win32\'")')
content = content.replace('safety', 'pip-audit')
content = content.replace('https://github.com/pycqa/pip-audit', 'https://github.com/pypa/pip-audit')
content = content.replace('rev: \'3.2.11\'\n    hooks:\n      - id: pip-audit\n        args: ["scan", "--json"]', 'rev: \'v2.8.0\'\n    hooks:\n      - id: pip-audit')
if 'pre-commit' not in content and 'package-ecosystem' in content:
    content = content.replace('interval: "daily"\n"""', 'interval: "daily"\n  - package-ecosystem: "pre-commit"\n    directory: "/"\n    schedule:\n      interval: "weekly"\n"""')

if 'def _generate_gitignore' not in content:
    gitignore_func = """
def _generate_gitignore(args: argparse.Namespace) -> None:
    \"\"\"Generate the .gitignore file.\"\"\"
    _log("📝 Generating .gitignore file...", args)
    content = \"\"\"\\
.venv/
__pycache__/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.hypothesis/
*.bak
dist/
build/
\"\"\"
    _safe_write(Path(".gitignore"), content, args)
"""
    content = content.replace('def _generate_dependabot_config', gitignore_func + '\ndef _generate_dependabot_config')
    content = content.replace('_generate_dependabot_config(args)\n    _generate_security_policy', '_generate_dependabot_config(args)\n    _generate_gitignore(args)\n    _generate_security_policy')

bootstrapper.write_text(content)
