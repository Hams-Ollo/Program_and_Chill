.PHONY: install test lint format clean run help

help:
	@echo "Available commands:"
	@echo "make install    - Install dependencies"
	@echo "make test      - Run tests"
	@echo "make lint      - Run linting"
	@echo "make format    - Format code"
	@echo "make clean     - Clean up cache files"
	@echo "make run       - Run the application"

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v --cov=app

lint:
	flake8 app/ tests/
	mypy app/ tests/

format:
	black app/ tests/
	isort app/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

run:
	streamlit run frontend/streamlit.py
