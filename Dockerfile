FROM python:3.9-alpine

WORKDIR /app

# Install build dependencies, then remove them
RUN apk update && apk add --no-cache build-base && \
    pip install --no-cache-dir poetry && \
    apk del build-base && rm -rf /var/cache/apk/*

# Copy only the files needed for dependency installation
COPY pyproject.toml poetry.lock ./

# Install dependencies using poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application code
COPY . .

# The main command to run the ETL pipeline
CMD ["python", "main.py"]
