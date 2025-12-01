FROM python:3.9-alpine

WORKDIR /app

# Install build dependencies, then remove them
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && \
    pip install --no-cache-dir poetry && \
    apt-get remove -y build-essential && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

# Copy only the files needed for dependency installation
COPY pyproject.toml poetry.lock ./

# Install dependencies using poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application code
COPY . .

# The main command to run the ETL pipeline
CMD ["python", "main.py"]
