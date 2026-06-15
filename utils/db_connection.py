import sqlite3
import threading
from config import Config

# ── Global write lock — only ONE write can happen at a time ──
_write_lock = threading.Lock()


def get_db_connection():
    """
    Returns a SQLite connection for READ operations.
    Always close() the connection after use (use try/finally).
    """
    conn = sqlite3.connect(
        Config.DATABASE,
        timeout=30,
        check_same_thread=False
    )
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=15000;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn


def safe_write(sql, params=()):
    """
    Thread-safe write helper.
    Acquires a global lock, executes the SQL, commits, and
    ALWAYS closes the connection — even if an exception occurs.
    Returns None on success, raises Exception on error.
    """
    with _write_lock:          # only one write at a time
        conn = sqlite3.connect(
            Config.DATABASE,
            timeout=30,
            check_same_thread=False
        )
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA busy_timeout=15000;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        try:
            conn.execute(sql, params)
            conn.commit()
        except Exception:
            conn.rollback()
            raise            # re-raise so caller can handle it
        finally:
            conn.close()     # ALWAYS closed, no matter what
