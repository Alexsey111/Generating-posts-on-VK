.PHONY: install install-dev install-web test test-cov lint format type-check clean run run-web init-db prod-setup

# Default target
all: install-dev test lint format type-check

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

install-web:
	pip install flask flask-login flask-wtf flask-sqlalchemy werkzeug

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

# Web application commands
run-web: install-web
	python app.py

init-db: install-web
	python init_db.py

prod-setup: install-web
	@echo "Setting up production environment..."
	@echo "Please ensure your .env file is properly configured for production"
	@echo "Run 'cp .env.example .env' and edit the file with production values"

# Cleanup
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	find . -type d -name "htmlcov" -delete
	find . -type d -name ".coverage" -delete
	find . -type d -name "*.egg-info" -delete
	rm -rf build/
	rm -rf dist/
	rm -f app.db
	rm -f *.log

# Full CI pipeline
ci: install-dev test-cov lint format type-check
	@echo "✅ All checks passed!"