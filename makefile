.PHONY: install test

install:
	uv pip install -e '.[dev]'

test:
	uv run pytest -s --cov=src/misstea ./tests
