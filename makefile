.PHONY: install test

install:
	uv pip install -e '.[dev]'

test:
	uv run pytest -n 5 -s --cov=src/misstea ./tests
