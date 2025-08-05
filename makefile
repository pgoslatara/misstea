.PHONY: install test

install:
	uv pip install -e '.[dev]' $(argument)

test:
	pytest -n 5 --cov=misstea
