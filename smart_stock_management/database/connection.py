import sqlite3
from pathlib import Path

# database directory
BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "smart_stock.db"


def get_connection():
    """
    Create and return a SQLite database connection.
    """
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection
