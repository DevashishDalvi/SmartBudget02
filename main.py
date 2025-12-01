import os
from etl import seed, ingest, transform, scoring, recommendations

# Define the paths
DB_PATH = "data/smartbudget.db"
CSV_PATH = "data/sample.csv"

def main():
    """Runs the entire ETL pipeline."""
    print("Starting ETL pipeline...")

    # Ensure the data directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    # 1. Seed the database with initial data
    seed.seed_database(DB_PATH)

    # 2. Ingest the raw CSV data
    ingest.ingest_csv(CSV_PATH, DB_PATH)

    # 3. Transform the raw data into the canonical schema
    transform.transform_and_load(DB_PATH)

    # 4. Calculate scores
    scoring.calculate_scores(DB_PATH)

    # 5. Generate recommendations
    recommendations.generate_recommendations(DB_PATH)

    print("ETL pipeline finished successfully!")

if __name__ == "__main__":
    main()
