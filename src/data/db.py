"""
src/data/db.py — SQLite connection helper.
Uses pathlib for Cloud-safe absolute path resolution.
get_connection() returns a plain sqlite3.Connection.
Use as a context manager via `with get_connection() as conn:` —
sqlite3.Connection supports context-manager protocol (commit/rollback),
but does NOT close on __exit__; caller must close explicitly OR use
the contextlib.closing() wrapper (done in loader.py).
"""
import os
import sqlite3
from pathlib import Path

# Resolve project root relative to this file (src/data/db.py → ../../)
# Works identically on Windows, Linux (Streamlit Cloud) and macOS.
_HERE = Path(__file__).resolve().parent          # src/data/
_SRC  = _HERE.parent                             # src/
APP_ROOT = _SRC.parent                           # project root
DEFAULT_DB_PATH = str(APP_ROOT / "data" / "app.db")


def get_connection(db_path: str = DEFAULT_DB_PATH, read_only: bool = True) -> sqlite3.Connection:
    """
    Returns an ACID-compliant SQLite connection.

    - read_only=True  → URI ?mode=ro for multi-thread Streamlit safety.
    - read_only=False → standard read-write with PRAGMA foreign_keys = ON.

    NOTE: Use `with contextlib.closing(get_connection()) as conn:` to
    guarantee the connection is closed after use, or close() explicitly.
    sqlite3.Connection's context-manager only handles commit/rollback,
    it does NOT close the connection on __exit__.
    """
    db_path = str(Path(db_path).resolve())       # normalise on every OS

    if not Path(db_path).exists():
        raise FileNotFoundError(
            f"Database not found at: {db_path}\n"
            "Ensure data/app.db is committed to the repository and paths are correct."
        )

    if read_only:
        # URI mode: thread-safe, no accidental writes on Streamlit Cloud
        uri_path = f"file:{db_path}?mode=ro"
        conn = sqlite3.connect(uri_path, uri=True, check_same_thread=False)
    else:
        conn = sqlite3.connect(db_path, check_same_thread=False)
        conn.execute("PRAGMA foreign_keys = ON;")

    return conn
