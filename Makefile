.PHONY: help build

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

build:
	docker-compose build

up:
	docker-compose up

up-d:
	docker-compose up -d

stop:
	docker-compose stop

down:
	docker-compose down

migrate:
	docker-compose exec brain-ag-web python manage.py flush --no-input
	docker-compose exec brain-ag-web python manage.py migrate

pytest:
	docker-compose exec brain-ag-web pytest --cov=.

linting-check:
	docker-compose exec brain-ag-web flake8 --exclude=.venv,migrations .
	docker-compose exec brain-ag-web isort . --check-only --skip .venv --skip migrations
	docker-compose exec brain-ag-web black --check --exclude '/(\.venv|migrations)/' .

linting-apply:
	docker-compose exec brain-ag-web flake8 --exclude=.venv,migrations .
	docker-compose exec brain-ag-web isort . --skip .venv --skip migrations
	docker-compose exec brain-ag-web black --exclude '/(\.venv|migrations)/' .

# dumpdata-agro:
# 	docker-compose exec brain-ag-web python manage.py dumpdata > fixtures/agro.json

loaddata-agro:
	docker-compose exec brain-ag-web python manage.py loaddata fixtures/agro.json
