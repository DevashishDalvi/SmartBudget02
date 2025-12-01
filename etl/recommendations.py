import duckdb

def generate_recommendations(db_path: str):
    """Generates and stores recommendations based on high-priority scores."""
    con = duckdb.connect(database=db_path, read_only=False)
    
    # Generate recommendations for high-priority items
    high_priority_expenses = con.execute("""
        WITH expense_scores AS (
            SELECT 
                e.expense_id, 
                e.amount, 
                e.product_name,
                COALESCE(lw.weight, 1.0) AS weight,
                e.amount * COALESCE(lw.weight, 1.0) AS score,
                NTILE(4) OVER (ORDER BY e.amount * COALESCE(lw.weight, 1.0) DESC) as score_priority_bucket_num
            FROM expenses e
            LEFT JOIN expense_labels el ON e.expense_id = el.expense_id
            LEFT JOIN label_weights lw ON el.label_id = lw.label_id
        )
        SELECT
            es.expense_id,
            es.product_name,
            es.amount,
            es.score
        FROM expense_scores es 
        WHERE es.score_priority_bucket_num = 1 -- 'High' bucket
    """).fetchall()
    
    for expense_id, product, amount, score in high_priority_expenses:
        message = f"High priority spending detected on '{product}' (Amount: ${amount:.2f}). Consider reviewing this expense."
        confidence = score
        
        # Use a stable, idempotent ID based on the expense ID
        recommendation_id = abs(hash(f"rec_{expense_id}"))

        con.execute(
            """
            INSERT INTO recommendations (recommendation_id, generated_at, message, confidence, related_expense_id)
            VALUES (?, NOW(), ?, ?, ?)
            ON CONFLICT (recommendation_id) DO UPDATE SET
                generated_at = excluded.generated_at,
                confidence = excluded.confidence;
            """,
            (recommendation_id, message, confidence, expense_id)
        )
        
    print(f"Generated {len(high_priority_expenses)} recommendations.")
    con.close()
