.PHONY: help install test lint format typecheck security clean all

help:
	@echo "Python Stack Bootstrapper - Development Commands"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install    Install dependencies with Poetry"
	@echo "  test       Run tests with pytest"
	@echo "  lint       Run ruff linter"
	@echo "  format     Format code with ruff"
	@echo "  typecheck  Run mypy type checker"
	@echo "  security   Run security checks (bandit, safety)"
	@echo "  clean      Clean cache and temporary files"
	@echo "  all        Run all checks (lint, typecheck, security, test)"

install:
	poetry install

test:
	poetry run pytest tests/ -v --cov=. --cov-report=html --cov-report=term-missing

lint:
	poetry run ruff check stack.py tests/

format:
	poetry run ruff format stack.py tests/

typecheck:
	poetry run mypy stack.py

security:
	@echo "Running Bandit security scanner..."
	poetry run bandit -r stack.py
	@echo ""
	@echo "Running Safety dependency checker..."
	poetry run safety check

clean:
	@echo "Cleaning cache and temporary files..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name "*.bak" -delete 2>/dev/null || true
	rm -rf htmlcov/ .coverage 2>/dev/null || true
	@echo "Clean complete!"

all: lint typecheck security test
	@echo ""
	@echo "✅ All checks passed!"
