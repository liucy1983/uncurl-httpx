SHELL := /bin/bash

init:
	@uv sync --extra dev

test:
	@PYTHONPATH=. uv run pytest ./tests/

publish:
	uv run python scripts/publish.py
