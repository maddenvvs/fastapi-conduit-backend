venv:
	python3 -m venv .venv; \
	. .venv/bin/activate; \
	pip install -r requirements-dev.txt

test:
	python -m pytest -n auto --strict-markers ./tests

dev-server:
	fastapi dev gameapp/app.py

docker_build:
	docker-compose up -d --build

docker_up:
	docker-compose up -d

docker_down:
	docker-compose down

docker_restart:
	docker-compose stop
	docker-compose up -d

types:
	mypy

format:
	ruff format --quiet

lint:
	ruff check --quiet

check: format types lint
