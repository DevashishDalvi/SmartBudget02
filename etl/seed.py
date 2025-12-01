import duckdb

def seed_database(db_path: str):
    """Creates tables and seeds initial data for mappings and labels."""
    con = duckdb.connect(database=db_path, read_only=False)

    # 1. Create all tables if they don't exist
    con.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            expense_id UBIGINT PRIMARY KEY,
            occurred_at TIMESTAMP NOT NULL,
            product_name VARCHAR NOT NULL,
            quantity DOUBLE,
            unit_price DOUBLE,
            amount DOUBLE NOT NULL,
            category_id BIGINT,
            payment_mode_id BIGINT,
            notes VARCHAR,
            source_system VARCHAR,
            source_row_id VARCHAR
        );

        CREATE TABLE IF NOT EXISTS categories (
            category_id BIGINT PRIMARY KEY,
            name VARCHAR NOT NULL UNIQUE,
            description VARCHAR
        );

        CREATE TABLE IF NOT EXISTS labels (
            label_id BIGINT PRIMARY KEY,
            name VARCHAR NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS expense_labels (
            expense_id UBIGINT NOT NULL,
            label_id BIGINT NOT NULL,
            PRIMARY KEY (expense_id, label_id)
        );

        CREATE TABLE IF NOT EXISTS label_weights (
            label_id BIGINT NOT NULL,
            weight DOUBLE NOT NULL,
            effective_from TIMESTAMP NOT NULL,
            effective_to TIMESTAMP,
            PRIMARY KEY (label_id, effective_from)
        );

        CREATE TABLE IF NOT EXISTS payment_modes (
            payment_mode_id BIGINT PRIMARY KEY,
            name VARCHAR NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS category_mappings (
            source_system VARCHAR NOT NULL,
            raw_value VARCHAR NOT NULL,
            category_id BIGINT NOT NULL,
            PRIMARY KEY (source_system, raw_value)
        );

        CREATE TABLE IF NOT EXISTS unmapped_categories (
            raw_value VARCHAR NOT NULL,
            source_system VARCHAR NOT NULL,
            first_seen_at TIMESTAMP NOT NULL,
            PRIMARY KEY (raw_value, source_system)
        );

        CREATE TABLE IF NOT EXISTS raw_source_google (
            id BIGINT PRIMARY KEY,
            ingested_at TIMESTAMP,
            date VARCHAR,
            item VARCHAR,
            category VARCHAR,
            quantity VARCHAR,
            price VARCHAR,
            notes VARCHAR,
            payment_mode VARCHAR
        );

        CREATE TABLE IF NOT EXISTS recommendations (
            recommendation_id BIGINT PRIMARY KEY,
            generated_at TIMESTAMP,
            message VARCHAR,
            confidence DOUBLE,
            related_expense_id UBIGINT
        );
    """)

    # 2. Seed initial mapping and master data
    con.execute("""
        -- Seed Categories
        INSERT INTO categories (category_id, name) VALUES (1, 'Groceries'), (2, 'Dining'), (3, 'Transport') ON CONFLICT DO NOTHING;

        -- Seed Category Mappings
        INSERT INTO category_mappings (source_system, raw_value, category_id)
        VALUES
            ('google_sheets', 'supermarket', 1),
            ('google_sheets', 'groceries', 1),
            ('google_sheets', 'restaurant', 2),
            ('google_sheets', 'uber', 3)
        ON CONFLICT DO NOTHING;

        -- Seed Labels & Weights
        INSERT INTO labels (label_id, name) VALUES (101, 'essential'), (102, 'discretionary'), (103, 'work') ON CONFLICT DO NOTHING;
        INSERT INTO label_weights (label_id, weight, effective_from) 
        VALUES (101, 0.5, NOW()), (102, 1.5, NOW()), (103, 0.8, NOW()) ON CONFLICT DO NOTHING;
    """)

    print("Database seeded successfully.")
    con.close()
