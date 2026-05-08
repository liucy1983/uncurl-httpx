SHELL := /bin/bash

init:
	@python setup.py develop
	@pip install -r requirements.txt

test:
	@PYTHONPATH=. uv run pytest ./tests/

publish:
	python setup.py sdist bdist_wheel upload
