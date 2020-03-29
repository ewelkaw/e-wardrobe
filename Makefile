# Makefile

build:
	docker build . -t ewardrobe

run:
	docker-compose up