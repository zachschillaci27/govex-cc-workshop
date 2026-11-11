.PHONY: install test lint run

install:
	python -m pip install -e ".[dev]"

test:
	python -m pytest -q

lint:
	ruff check src tests && ruff format --check src tests

run:
	python -m service_metrics data/sample_311.csv --html dashboard.html
