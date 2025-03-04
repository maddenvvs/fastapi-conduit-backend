venv:
	python3 -m venv .venv; \
	. .venv/bin/activate; \
	pip install -r requirements-dev.txt

test:
	python -m pytest -n auto --strict-markers ./tests

dev-server:
	fastapi dev gameapp/app.py

types:
	mypy

format:
	ruff format --quiet

lint:
	ruff check --quiet

check: format types lint
