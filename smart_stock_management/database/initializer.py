from pathlib import Path
from smart_stock_management.database.connection import get_connection

# schema directory
BASE_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = BASE_DIR / "schema.sql"


def initialize_database():
    """
    Initialize database tables using schema.sql.
    """
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError("schema.sql not found in database directory")

    connection = get_connection()
    cursor = connection.cursor()

    with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
        schema_sql = schema_file.read()

    cursor.executescript(schema_sql)
    connection.commit()
    connection.close()
