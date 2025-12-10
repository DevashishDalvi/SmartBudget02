# Makefile for SmartBudget

# Shell used to execute commands. For cross-platform compatibility (Linux/macOS/Windows with WSL or PowerShell).

# --- Configuration ---

# Define the targets for the Continuous Integration (CI) process
CI_TARGETS := format lint test

# --- Phony Targets ---

# Declare targets that are not actual files. This prevents conflicts and improves performance.
.PHONY: all help install format lint test ci run-etl clean

# Set the default goal to 'help' so that running 'make' without arguments shows the help message.
.DEFAULT_GOAL := help

# --- User-Facing Commands ---

all: ci

help:
	@echo "✨ SmartBudget Makefile ✨"
	@echo ""
	@echo "Usage:"
	@echo "  make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  install        - 📦 Install dependencies and the project in editable mode."
	@echo "  format         - 💅 Format the codebase using Ruff."
	@echo "  lint           - 🧐 Lint the codebase using Ruff."
	@echo "  test           - ✅ Run tests using Pytest."
	@echo "  ci             - 🚀 Run the full CI pipeline (format, lint, test)."
	@echo "  run-etl        - 🏃 Execute the main ETL pipeline."
	@echo "  clean          - 🧹 Remove temporary files and caches."
	@echo ""

install:
	@echo "📦 Installing project dependencies..."
	uv pip install -e .[dev]
	@echo "✅ Dependencies installed successfully."

format:
	@echo "💅 Formatting code with Ruff..."
	uv run ruff format .
	@echo "✅ Formatting complete."

lint:
	@echo "🧐 Linting code with Ruff..."
	uv run ruff check .
	@echo "✅ Linting complete."

test:
	@echo "✅ Running tests with Pytest..."
	uv run python -m pytest -v
	@echo "✅ Tests passed."

# The 'ci' target runs all checks. It depends on 'install' to ensure dependencies are present.
ci: install
	@echo "🚀 Starting CI pipeline..."
	@$(foreach target,$(CI_TARGETS),echo "--- Running $(target) ---"; $(MAKE) $(target) || exit 1;)
	@echo "🎉 CI pipeline completed successfully!"

run-etl: install
	@echo "🏃 Running the ETL pipeline..."
	uv run python -m src.SmartBudget.etl.pipelines

clean:
	@echo "🧹 Cleaning up temporary files and caches..."
	@# Using '|| true' to prevent errors if files/directories don't exist
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf src/*.egg-info
	find . -type d -name "__pycache__" -exec rm -r {} + || true
	find . -type f -name "*.py[co]" -delete || true
	@echo "🧼 Cleanup complete."
