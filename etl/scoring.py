import duckdb

def calculate_scores(db_path: str):
    """Calculates and updates scores in the database."""
    con = duckdb.connect(database=db_path, read_only=False)
    
    # This query calculates priority scores for all expenses
    con.execute("""
        CREATE OR REPLACE TEMP VIEW expense_scores AS
        WITH scored_labels AS (
            SELECT
                el.expense_id,
                e.amount,
                lw.weight,
                DATE_DIFF('month', e.occurred_at, NOW()) as month_diff
            FROM expense_labels el
            JOIN expenses e ON el.expense_id = e.expense_id
            JOIN label_weights lw ON el.label_id = lw.label_id
            WHERE lw.effective_to IS NULL
        ),
        priority_scores AS (
            SELECT
                expense_id,
                SUM(amount * weight * POWER(0.6, month_diff)) AS priority_score
            FROM scored_labels
            GROUP BY expense_id
        ),
        max_score AS (
            SELECT MAX(priority_score) as max_val FROM priority_scores
        )
        SELECT
            ps.expense_id,
            ps.priority_score,
            ps.priority_score / ms.max_val AS score_norm,
            CASE
                WHEN (ps.priority_score / ms.max_val) > 0.7 THEN 'High'
                WHEN (ps.priority_score / ms.max_val) > 0.4 THEN 'Medium'
                ELSE 'Low'
            END AS score_priority_bucket
        FROM priority_scores ps, max_score ms;
    """)
    
    print("Calculated priority scores. View is available at 'expense_scores'.")
    con.close()
