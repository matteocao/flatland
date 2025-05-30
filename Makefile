install:
	poetry install --with dev

test:
	poetry run black .
	poetry run isort .
	poetry run mypy .
	poetry run pytest -vs --cov=. --cov-report=xml

run:
	poetry run python3 -m flatland

doc:
	poetry run pdoc -o docs_html flatland