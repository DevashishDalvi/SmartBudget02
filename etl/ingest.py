import pandas as pd
import duckdb
from datetime import datetime

def ingest_csv(csv_path: str, db_path: str):
    """Ingests a CSV file into a raw table in DuckDB."""
    con = duckdb.connect(database=db_path, read_only=False)
    
    # Use pandas to read the CSV
    df = pd.read_csv(csv_path)
    
    # Add an ingestion timestamp and a unique ID
    df['ingested_at'] = datetime.now()
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'id'}, inplace=True)

    # Create the table and insert the data
    con.execute("CREATE OR REPLACE TABLE raw_source_google AS SELECT * FROM df")
    
    print(f"Ingested {len(df)} rows from {csv_path} into raw_source_google.")
    con.close()
