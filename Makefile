PROJECT_NAME=hireme
DOCKER_REPO=$(PROJECT_NAME)
DOCKER_URL=<aws_account_id>.dkr.ecr.us-east-1.amazonaws.com
DOCKER_TAG?=latest

all:

build:
	@docker build -t $(DOCKER_REPO) .

publish: build
	@docker tag $(DOCKER_REPO) $(DOCKER_URL)/$(DOCKER_REPO):$(DOCKER_TAG)
	@docker push $(DOCKER_URL)/$(DOCKER_REPO):$(DOCKER_TAG)

stop-local:
	@docker rm -f mysql || true
	@docker rm -f hireme || true

run-local:
	@docker run -d --name mysql \
	-p 3306:3306 \
	-e MYSQL_ROOT_PASSWORD=supersecret \
	-e MYSQL_DATABASE=hireme \
	-e MYSQL_USER=hireme \
	-e MYSQL_PASSWORD=hireme \
	mysql:5.7
	@echo waiting 20 seconds for mysql to stabilize..
	@sleep 20
	@docker run -d --name hireme -e ENV=local -p 8000:5000 \
	--link mysql $(DOCKER_REPO)
	@echo Started hireme on http://127.0.0.1:8000

re-run-no-database: build
	@docker rm -f hireme || true
	@docker run -d --name hireme -e ENV=local -p 8000:5000 \
	--link mysql $(DOCKER_REPO)
	@echo Started hireme on http://127.0.0.1:8000/

first-run: build run-local

re-run: build stop-local run-local

PHONY: all build stop-local run-local
