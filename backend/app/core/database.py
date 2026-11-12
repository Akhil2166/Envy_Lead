import sqlite3
from contextlib import contextmanager
from pathlib import Path

from app.core.config import get_settings


def _db_path() -> Path:
    url = get_settings().database_url
    # support sqlite:///./file.db and sqlite:///absolute/path.db
    if url.startswith("sqlite:///"):
        path = url[len("sqlite:///"):]
    else:
        path = url
    p = Path(path)
    if not p.is_absolute():
        p = Path.cwd() / p
    return p


def init_db() -> None:
    path = _db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                budget TEXT,
                location TEXT,
                property_type TEXT,
                bhk TEXT,
                intent TEXT,
                notes TEXT,
                transcript TEXT,
                language TEXT,
                source TEXT DEFAULT 'voice',
                status TEXT DEFAULT 'new',
                priority TEXT DEFAULT 'medium',
                summary TEXT,
                next_action TEXT,
                request_id TEXT,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                updated_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        conn.commit()


@contextmanager
def get_db():
    conn = sqlite3.connect(_db_path())
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def row_to_dict(row: sqlite3.Row) -> dict:
    return {k: row[k] for k in row.keys()}
