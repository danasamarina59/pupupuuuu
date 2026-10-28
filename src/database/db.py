import sqlite3
from contextlib import contextmanager
from pathlib import Path

# Файл базы данных и schema.sql лежат в той же папке database
DB_PATH = Path(__file__).parent / "beauty_salon.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.commit()

@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()