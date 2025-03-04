docker_build:
	docker-compose up -d --build

docker_up:
	docker-compose up -d

docker_down:
	docker-compose down

docker_restart:
	docker-compose stop
	docker-compose up -d
