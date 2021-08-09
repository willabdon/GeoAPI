#!make
include .env
export $(shell sed 's/=.*//' .env)

start-dev:
	docker compose up -d

start:
	docker compose up

stop:
	docker compose down

ssh-nginx:
	docker exec -it geo_nginx_server sh

ssh-backend:
	docker exec -it geo sh

ssh-db:
	docker exec -it geo_db bash
