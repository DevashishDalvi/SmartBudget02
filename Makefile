.PHONY: install format lint test run

install:
	uv pip sync pyproject.toml

format:
	uv run ruff format .

lint:
	uv run ruff check .

test:
	uv run pytest test/ -v

run-etl:
	uv run python -m src.smart_budget.etl.pipelines
