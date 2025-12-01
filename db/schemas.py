import duckdb

"""Schmeas are stored here"""

PATH = ""
con = duckdb.connect(database=PATH)

sql_statements = [
    """CREATE TABLE expenses (
        expense_id BIGINT PRIMARY KEY,
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
    );""",
    """CREATE TABLE categories (
        category_id BIGINT PRIMARY KEY,
        name VARCHAR NOT NULL UNIQUE,
        description VARCHAR
    );""",
    """CREATE TABLE labels (
        label_id BIGINT PRIMARY KEY,
        name VARCHAR NOT NULL UNIQUE
    );""",
    """CREATE TABLE expense_labels (
        expense_id BIGINT NOT NULL,
        label_id BIGINT NOT NULL,
        PRIMARY KEY (expense_id, label_id)
    );""",
    """CREATE TABLE label_weights (
        label_id BIGINT NOT NULL,
        weight DOUBLE NOT NULL,
        effective_from TIMESTAMP NOT NULL,
        effective_to TIMESTAMP,
        PRIMARY KEY (label_id, effective_from)
    );""",
    """CREATE TABLE payment_modes (
        payment_mode_id BIGINT PRIMARY KEY,
        name VARCHAR NOT NULL UNIQUE
    );""",
    """CREATE TABLE category_mappings (
        source_system VARCHAR NOT NULL,
        raw_value VARCHAR NOT NULL,
        category_id BIGINT NOT NULL,
        PRIMARY KEY (source_system, raw_value)
    );""",
    """CREATE TABLE label_mappings (
        old_label_id BIGINT NOT NULL,
        new_label_id BIGINT NOT NULL,
        mapping_date DATE NOT NULL,
        PRIMARY KEY (old_label_id, new_label_id, mapping_date)
    );""",
    """CREATE TABLE unmapped_categories (
        raw_value VARCHAR NOT NULL,
        source_system VARCHAR NOT NULL,
        first_seen_at TIMESTAMP NOT NULL,
        PRIMARY KEY (raw_value, source_system)
    );""",
]

for sql_statement in sql_statements:
    con.execute(sql_statement)
    print(
        f"Executed: {
            sql_statement.split('(', maxsplit=1)[0].replace('CREATE TABLE ', '')
        }"
    )

# Verify table creation
print("\nTables created in DuckDB:")
print(con.execute("SHOW TABLES;").fetchdf())
