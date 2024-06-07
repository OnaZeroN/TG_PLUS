project_dir := .
bot_dir := src
translations_dir := translations

# Lint code
.PHONY: lint
lint:
	@poetry run black --check --diff $(project_dir)
	@poetry run ruff check $(project_dir)
	@poetry run mypy $(project_dir) --strict

# Reformat code
.PHONY: reformat
reformat:
	@poetry run black $(project_dir)
	@poetry run ruff check $(project_dir) --fix

.PHONY: app-build
app-build:
	docker-compose build

.PHONY: app-run-db
app-run-db:
	docker compose stop
	docker compose up -d postgres --remove-orphans

.PHONY: app-run
app-run:
	docker-compose stop
	docker-compose up -d --remove-orphans

.PHONY: app-stop
app-stop:
	docker-compose stop

.PHONY: app-down
app-down:
	docker-compose down

.PHONY: app-destroy
app-destroy:
	docker-compose down -v --remove-orphans

.PHONY: app-logs
app-logs:
	docker-compose logs -f bot
