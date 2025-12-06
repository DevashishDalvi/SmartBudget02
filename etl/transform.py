import duckdb

def transform_and_load(db_path: str):
    """Transforms raw data, loads it into the canonical schema, and assigns labels."""
    con = duckdb.connect(database=db_path, read_only=False)
    
    # 1. Log unmapped categories before attempting to transform
    con.execute("""
        INSERT INTO unmapped_categories (raw_value, source_system, first_seen_at)
        SELECT DISTINCT
            raw.category,
            'google_sheets',
            MIN(raw.ingested_at)
        FROM raw_source_google raw
        LEFT JOIN category_mappings cm ON raw.category = cm.raw_value AND cm.source_system = 'google_sheets'
        WHERE cm.category_id IS NULL AND raw.category IS NOT NULL
        GROUP BY raw.category
        ON CONFLICT (raw_value, source_system) DO NOTHING;
    """)
    
    # 2. Transform and insert into the expenses table
    con.execute("""
        INSERT INTO expenses (expense_id, occurred_at, product_name, quantity, unit_price, amount, category_id, notes, source_system, source_row_id)
        SELECT
            abs(hash(raw.id::VARCHAR)) AS expense_id,
            strptime(raw.date, '%Y-%m-%d')::TIMESTAMP,
            raw.item,
            1,
            CAST(raw.price AS DOUBLE),
            CAST(raw.price AS DOUBLE),
            cm.category_id,
            raw.notes,
            'google_sheets',
            raw.id::VARCHAR
        FROM raw_source_google raw
        LEFT JOIN category_mappings cm ON raw.category = cm.raw_value AND cm.source_system = 'google_sheets'
        ON CONFLICT (expense_id) DO UPDATE SET
            occurred_at = excluded.occurred_at,
            product_name = excluded.product_name,
            amount = excluded.amount,
            category_id = excluded.category_id;
    """)

    # 3. Assign labels to expenses based on category
    con.execute("""
        -- Assign 'essential' label to Groceries
        INSERT INTO expense_labels (expense_id, label_id)
        SELECT e.expense_id, 101 -- essential
        FROM expenses e
        WHERE e.category_id = 1 -- Groceries
        ON CONFLICT DO NOTHING;

        -- Assign 'discretionary' label to Dining
        INSERT INTO expense_labels (expense_id, label_id)
        SELECT e.expense_id, 102 -- discretionary
        FROM expenses e
        WHERE e.category_id = 2 -- Dining
        ON CONFLICT DO NOTHING;
    """)

    print("Transformed, loaded, and labeled expenses.")
    con.close()