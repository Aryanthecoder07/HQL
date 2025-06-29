# core/db_utils.py
import sqlite3

def get_connection(db_path: str):
    """Connect to SQLite DB."""
    return sqlite3.connect(db_path, check_same_thread=False)

def list_tables(cursor):
    """Get all table names."""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    return [row[0] for row in cursor.fetchall()]

def fetch_table(cursor, sql_query):
    """Fetch rows and columns from SELECT query."""
    cursor.execute(sql_query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return rows, columns
