.PHONY: install migrate makemigrations runserver superuser update test

install:
	poetry install
	
migrate:
	poetry run python3 -m core.manage migrate

makemigrations:
	poetry run python3 -m core.manage makemigrations

runserver:
	poetry run python3 -m core.manage runserver

superuser:
	poetry run python3 -m core.manage createsuperuser

startapp:
	poetry run python3 -m core.manage startapp $(name) $(path)

shell:
	poetry run python3 -m core.manage shell

test:
	poetry run pytest -v -rs -n auto --show-capture=no


.PHONY: up-dependencies-only
up-dependencies-only:
	test -f .env || touch .env
	docker-compose -f docker-compose.dev.yml up --force-recreate db


update: install migrate ; @echo "Update complete!"


