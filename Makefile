install:
	poetry install --with dev

test:
	poetry run black .
	poetry run isort .
	poetry run mypy .
	poetry run pytest -vs --cov=. --cov-report=html

check:
	poetry run black --check .
	poetry run isort --check .
	poetry run mypy .
	poetry run pytest -vs --cov=. --cov-report=html

run:
	poetry run python3 -m flatland

doc:
	poetry run pdoc -o docs_html flatland

client:
	poetry run python3 -m flatland.multiplayer

server:
	poetry run python3 flatland/run_server.py