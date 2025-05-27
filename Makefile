install:
	poetry install --with dev

test:
	poetry run black .
	poetry run isort .
	poetry run mypy .
	poetry run pytest .

run:
	poetry run python3 -m flatland.main
