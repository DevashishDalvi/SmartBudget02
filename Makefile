# SHELL := pwsh
# .SHELLFLAGS := -NoProfile -Command

.PHONY: install format lint test run

all: install format lint test

install:
	uv sync

format:
	uv run ruff format .

lint:
	uv run ruff check .

test:
	uv run pytest test/ -v

run-etl:
	uv run python -m src.smart_budget.etl.pipelines

# log:
# 	Get-Content logs/*
#
# del_logs:
# 	del logs/*
