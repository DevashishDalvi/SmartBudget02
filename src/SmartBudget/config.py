# File: src/smart_budget/config.py
import os
from enum import Enum


class Environment(str, Enum):
    LOCAL = "local"
    PRODUCTION = "production"


class Config:
    # Default to INFO if not set
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
    ENV: str = os.getenv("APP_ENV", "local")
    # JSON_LOGS: str = f"logs/los{}.jsonl"

    # We will add DB paths here later


settings = Config()
