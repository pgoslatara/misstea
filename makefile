.PHONY: install test

install:
	uv pip install -e '.[dev]'

test:
	pytest -n 5 --cov=misstea
