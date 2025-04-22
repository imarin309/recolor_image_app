lint:
	poetry run ruff check .
	poetry run ruff format . --check --diff
	poetry run mypy .

format:
	poetry run ruff format .

exe:
	poetry run streamlit run src/app.py
