# File: scripts/migrate_tags.py
import duckdb

def _get_label_id(con, label_name: str) -> int:
    result = con.execute("SELECT label_id FROM labels WHERE name = ?", (label_name,)).fetchone()
    if not result:
        raise ValueError(f"Label '{label_name}' not found.")
    return result[0]

def rename_label(db_path: str, old_name: str, new_name: str):
    """Renames a label."""
    con = duckdb.connect(database=db_path, read_only=False)
    con.execute("UPDATE labels SET name = ? WHERE name = ?", (new_name, old_name))
    print(f"Renamed label '{old_name}' to '{new_name}'.")
    con.close()

def merge_labels(db_path: str, source_labels: list[str], target_label: str):
    """Merges one or more source labels into a single target label."""
    con = duckdb.connect(database=db_path, read_only=False)
    
    target_id = _get_label_id(con, target_label)
    source_ids = tuple(_get_label_id(con, name) for name in source_labels)
    
    # Re-assign expense_labels
    con.execute(f"UPDATE expense_labels SET label_id = {target_id} WHERE label_id IN {source_ids}")
    
    # De-activate old labels (or delete)
    con.execute(f"DELETE FROM labels WHERE label_id IN {source_ids}")
    
    print(f"Merged {source_labels} into '{target_label}'.")
    con.close()

def split_label(db_path: str, source_label: str, new_label: str, expense_ids_to_move: list[int]):
    """Splits a label by moving a subset of its expenses to a new label."""
    con = duckdb.connect(database=db_path, read_only=False)
    
    # Create the new label
    con.execute("INSERT INTO labels (name) VALUES (?) ON CONFLICT DO NOTHING", (new_label,))
    new_label_id = _get_label_id(con, new_label)
    
    # Move specified expenses
    ids_tuple = tuple(expense_ids_to_move)
    con.execute(f"UPDATE expense_labels SET label_id = {new_label_id} WHERE expense_id IN {ids_tuple}")
    
    print(f"Split {len(expense_ids_to_move)} expenses from '{source_label}' to '{new_label}'.")
    con.close()
