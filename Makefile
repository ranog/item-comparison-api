init: install-deps

install-deps:
	@pip install --upgrade pip setuptools wheel
	@pip install --upgrade poetry
	@poetry install --no-root
	@pre-commit install --hook-type commit-msg
	@pre-commit run --all-files

run: init
	@poetry run env $(shell grep -v ^\# .env | xargs) uvicorn src.main:app --reload --port 8080

format:
	@poetry run ruff check --select I --fix
	@poetry run ruff format
	@poetry run ruff check --fix --exit-non-zero-on-fix

poetry-export:
	@poetry export --with dev -vv --no-ansi --no-interaction --without-hashes --format requirements.txt --output requirements.txt

build-container:
	@docker build \
		--tag secure:wardrobe-project \
		--build-arg GIT_HASH=$(shell git rev-parse HEAD) \
		-f Dockerfile \
		.

run-container: poetry-export build-container
	@docker run --rm -it \
		--name secure-wardrobe-project \
		--env-file .env \
		--env PORT=8080 \
		--publish 8080:8080 \
		secure:wardrobe-project

tests: init
	@poetry run env $(shell grep -v ^\# .env | xargs) pytest
