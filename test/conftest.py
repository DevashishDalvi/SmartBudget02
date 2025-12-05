# File: tests/conftest.py
import pytest

from src.SmartBudget.utils.logger import setup_logging


@pytest.fixture(scope="session", autouse=True)
def configure_test_env() -> None:
    """
    Auto-runs once before any tests start.
    Sets up logging so tests have clean output.
    """
    setup_logging()
