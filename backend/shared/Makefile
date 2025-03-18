venv:
	python3 -m venv .venv; \
	. .venv/bin/activate; \
	pip install -r ../../pip-requirements.txt; \
	pip install -r ../../dev-requirements.txt; \
	pip install -r requirements.txt

clean:
	rm -rf .pytest_cache/ .ruff_cache/ .venv/

test:
	python -m pytest -n auto --strict-markers ./tests

dev-server:
	fastapi dev conduit/app.py

types:
	pyright

format:
	ruff check --select I --fix; \
	ruff format --quiet

lint:
	ruff check --quiet

check: format types lint
