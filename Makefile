.DEFAULT_GOAL := help

ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
ENV_FILE ?= $(ROOT)/.env
NAME ?= poc
COMPOSE = docker compose --env-file "$(ENV_FILE)" -f "$(ROOT)/docker/compose.yaml"

.PHONY: help init config build generate app migrations migrate serve rebuild stop-web check test superuser shell manage

help:
	@printf '%s\n' \
	  'make init                    Create .env if it does not exist' \
	  'make config                  Validate the Compose configuration' \
	  'make build                   Build the Python image' \
	  'make generate                Generate the project and app (NAME=poc by default)' \
	  'make app NAME=app            Generate an additional Django app' \
	  'make migrations              Generate migration files' \
	  'make migrate                 Apply database migrations' \
	  'make serve                   Start services in foreground' \
	  'make rebuild                 Rebuild the image and recreate web' \
	  'make stop-web                Stop web before using PyCharm Run/Debug' \
	  'make check                   Run Django system checks' \
	  'make test                    Run all tests in app/tests/' \
	  'make superuser               Create a Django administrator' \
	  'make shell                   Open the Django Python shell' \
	  'make manage ARGS="..."       Run another manage.py command'

init:
	@if [ -f "$(ROOT)/.env" ]; then \
	  printf '%s\n' '.env already exists; kept unchanged'; \
	else \
	  cp "$(ROOT)/.env.example" "$(ROOT)/.env"; \
	  printf '%s\n' 'Created .env from .env.example'; \
	fi

config:
	$(COMPOSE) config

build:
	$(COMPOSE) build web

generate:
	@test -n "$(NAME)" || { printf '%s\n' 'Error: NAME must not be empty' >&2; exit 1; }
	@if [ -d "$(ROOT)/app/src" ] && [ -n "$$(ls -A "$(ROOT)/app/src")" ]; then \
	  printf '%s\n' 'Error: app/src/ must be empty before running make generate' >&2; \
	  exit 1; \
	fi
	@mkdir -p "$(ROOT)/app/src"
	$(COMPOSE) run --rm --no-deps web python /opt/poc/scaffold.py project "$(NAME)"
	$(MAKE) --no-print-directory -f "$(ROOT)/Makefile" app NAME="$(NAME)"
	$(COMPOSE) run --rm --no-deps web python /opt/poc/scaffold.py hello "$(NAME)"

app:
	@test -n "$(NAME)" || { printf '%s\n' 'Usage: make app NAME=hello'; exit 1; }
	$(COMPOSE) run --rm --no-deps web python /opt/poc/scaffold.py app "$(NAME)"

migrations:
	$(COMPOSE) run --rm web python manage.py makemigrations $(ARGS)

migrate:
	$(COMPOSE) run --rm web python manage.py migrate

serve:
	$(COMPOSE) up web

rebuild:
	$(COMPOSE) up -d --build web

stop-web:
	$(COMPOSE) stop web

check:
	$(COMPOSE) run --rm web python manage.py check

test:
	$(COMPOSE) run --rm web python manage.py test /app/tests

superuser:
	$(COMPOSE) run --rm web python manage.py createsuperuser

shell:
	$(COMPOSE) run --rm web python manage.py shell

manage:
	$(COMPOSE) run --rm web python manage.py $(ARGS)
