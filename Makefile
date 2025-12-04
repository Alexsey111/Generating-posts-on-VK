.PHONY: install install-dev test test-cov lint format type-check clean run

# Default target
all: install-dev test lint format type-check

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

# Testing
test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=. --cov-report=html --cov-report=term-missing

# Code quality
lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics

format:
	black . --line-length 88

type-check:
	mypy .

# Development workflow
dev-setup: install-dev
	@echo "Setting up development environment..."
	cp .env.example .env

run:
	python test.py

# Cleanup
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	find . -type d -name "htmlcov" -delete
	find . -type d -name ".coverage" -delete
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/

# Full CI pipeline
ci: install-dev test-cov lint format type-check
	@echo "✅ All checks passed!"