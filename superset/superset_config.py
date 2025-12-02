"""Code"""
# superset_config.py
import os

# Get the database path from an environment variable
DB_PATH = os.environ.get("DUCKDB_PATH", "/app/data/smartbudget.db")

# Construct the SQLAlchemy URI
SQLALCHEMY_DATABASE_URI = f"duckdb:///{DB_PATH}"

# Feature flags
FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
}

# Allow file uploads
CSV_UPLOAD = True
