venv:
	python3 -m venv .venv; \
	. .venv/bin/activate; \
	pip install -r pip-requirements.txt; \
	pip install -r dev-requirements.txt

docker_build:
	docker-compose up -d --build

docker_up:
	docker-compose up -d

docker_down:
	docker-compose down

docker_restart:
	docker-compose stop
	docker-compose up -d

lint:
	ruff check --quiet

format:
	ruff check --select I --fix; \
	ruff format --quiet
