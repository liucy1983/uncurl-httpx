SHELL := /bin/bash

init:
	@uv sync --extra dev

test:
	@PYTHONPATH=. uv run pytest ./tests/

publish:
	uv run python -m build
	uv run python -m twine check dist/*
	uv run python -m twine upload dist/*
