test:
	poetry run black .
	poetry run isort .
	poetry run mypy .
	poetry run pytest .