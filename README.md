# SmartBudget ETL & Analytics

This project provides a containerized ETL pipeline and analytics environment for personal expense tracking. It uses Docker to orchestrate a Python-based ETL process that feeds a DuckDB database, which is then visualized using Apache Superset.

## Key Features

- **Containerized Environment**: Uses Docker and Docker Compose for a reproducible and isolated setup.
- **Automated ETL Pipeline**: Ingests raw CSV data, transforms it, and calculates priority scores and recommendations.
- **Embedded Analytics**: Includes a pre-configured Apache Superset instance for data exploration and visualization.
- **Extensible Data Model**: The DuckDB database can be easily extended to accommodate new data sources and analytics.

## How to Run

### Prerequisites

- Docker
- Docker Compose (v2)

### Steps

1.  **Build and Run the Containers**:

    ```bash
    docker compose up --build
    ```

    This command will:
    -   Build the `etl` service image, installing all necessary Python dependencies.
    -   Start the `postgres`, `superset`, and `etl` services.
    -   The `etl` service will run automatically, process the data in `data/sample.csv`, and then exit.

2.  **Access Superset**:

    -   Open your web browser and navigate to `http://localhost:8088`.
    -   Log in with the default credentials (`admin`/`admin`).

3.  **Connect to the Database**:

    -   In Superset, go to **Data -> Databases** and click on the **+ Database** button.
    -   Select **DuckDB** from the list of supported databases.
    -   In the **SQLAlchemy URI** field, enter the following connection string:

        ```
        duckdb:////app/data/smartbudget.db
        ```

    -   Click **Test Connection** to verify that Superset can connect to the database, then click **Connect**.

4.  **Explore Your Data**:

    -   You can now create charts and dashboards to visualize your expense data. For example, you can create a chart to show your spending by category, or a table to view the generated recommendations.

## Project Structure

-   `compose.yaml`: The main Docker Compose file that defines the services.
-   `Dockerfile`: The Dockerfile for the `etl` service.
-   `main.py`: The main entrypoint for the ETL pipeline.
-   `etl/`: The directory containing the Python scripts for the ETL process (seed, ingest, transform, scoring, recommendations).
-   `data/`: The directory for your raw data files. Includes a `sample.csv` to get you started.
-   `superset/`: The directory for Superset configuration files.
-   `superset/superset_config.py`: The configuration file for Superset.
