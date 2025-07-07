#Makefile to bring up and shutdown local development env

#bring environment up
up:
	cd docker-compose ; \
	docker compose up

#take environment down
down:
	docker ps -a | grep trading | awk '{print $$1}' | xargs docker kill | xargs docker container rm
	docker ps -a | grep mongo | awk '{print $$1}' | xargs docker kill | xargs docker container rm

