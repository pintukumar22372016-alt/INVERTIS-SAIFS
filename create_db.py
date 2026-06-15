"""
SAIFS - Database Initialization & Migration Script
Handles both fresh creation and migration of existing DB.
"""
import sqlite3
import os

DB_PATH = os.path.join("database", "db.sqlite3")
SCHEMA_PATH = os.path.join("database", "schema.sql")


def migrate_existing_db(conn):
    """Add missing columns to existing tables gracefully."""
    cursor = conn.cursor()

    migrations = [
        # users table — add college_id as the primary identifier
        "ALTER TABLE users ADD COLUMN college_id TEXT UNIQUE",
        "ALTER TABLE users ADD COLUMN department TEXT DEFAULT 'General'",
        "ALTER TABLE users ADD COLUMN phone TEXT DEFAULT ''",
        "ALTER TABLE users ADD COLUMN profile_pic TEXT DEFAULT ''",
        "ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT (datetime('now','localtime'))",

        # feedback table
        "ALTER TABLE feedback ADD COLUMN student_id INTEGER",
        "ALTER TABLE feedback ADD COLUMN is_anonymous INTEGER DEFAULT 0",
        "ALTER TABLE feedback ADD COLUMN created_at TIMESTAMP DEFAULT (datetime('now','localtime'))",

        # complaints table
        "ALTER TABLE complaints ADD COLUMN student_id INTEGER",
        "ALTER TABLE complaints ADD COLUMN category TEXT DEFAULT 'General'",
        "ALTER TABLE complaints ADD COLUMN priority TEXT DEFAULT 'Medium'",
        "ALTER TABLE complaints ADD COLUMN resolved_by INTEGER",
        "ALTER TABLE complaints ADD COLUMN resolution TEXT DEFAULT ''",
        "ALTER TABLE complaints ADD COLUMN created_at TIMESTAMP DEFAULT (datetime('now','localtime'))",
        "ALTER TABLE complaints ADD COLUMN resolved_at TIMESTAMP",

        # notes table
        "ALTER TABLE notes ADD COLUMN description TEXT DEFAULT ''",
        "ALTER TABLE notes ADD COLUMN uploaded_by INTEGER",
        "ALTER TABLE notes ADD COLUMN uploaded_at TIMESTAMP DEFAULT (datetime('now','localtime'))",

        # doubts table
        "ALTER TABLE doubts ADD COLUMN asked_by INTEGER",
        "ALTER TABLE doubts ADD COLUMN answered_by INTEGER",
        "ALTER TABLE doubts ADD COLUMN status TEXT DEFAULT 'Open'",
        "ALTER TABLE doubts ADD COLUMN asked_at TIMESTAMP DEFAULT (datetime('now','localtime'))",
        "ALTER TABLE doubts ADD COLUMN answered_at TIMESTAMP",

        # attendance table
        "ALTER TABLE attendance ADD COLUMN student_id INTEGER",
        "ALTER TABLE attendance ADD COLUMN date DATE DEFAULT (date('now','localtime'))",
        "ALTER TABLE attendance ADD COLUMN recorded_by INTEGER",

        # notifications table
        "ALTER TABLE notifications ADD COLUMN user_id INTEGER",
        "ALTER TABLE notifications ADD COLUMN type TEXT DEFAULT 'info'",
        "ALTER TABLE notifications ADD COLUMN is_read INTEGER DEFAULT 0",
    ]

    for migration in migrations:
        try:
            cursor.execute(migration)
        except sqlite3.OperationalError:
            pass  # Column already exists – skip

    # Create new tables if they don't exist
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS events (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT    NOT NULL,
            description TEXT    DEFAULT '',
            event_date  DATE    NOT NULL,
            created_by  INTEGER,
            created_at  TIMESTAMP DEFAULT (datetime('now','localtime'))
        );

        CREATE TABLE IF NOT EXISTS doubt_replies (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            doubt_id   INTEGER NOT NULL,
            replied_by INTEGER,
            reply      TEXT    NOT NULL,
            created_at TIMESTAMP DEFAULT (datetime('now','localtime'))
        );
    """)

    conn.commit()
    print("Migration applied successfully.")


def seed_demo_data(conn):
    """Insert demo data if tables are empty."""
    from werkzeug.security import generate_password_hash

    cursor = conn.cursor()

    # Check if any users exist
    count = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if count > 0:
        print("Existing data found – skipping seed.")
        return

    users = [
        ("Admin User",    "ADM2026001", generate_password_hash("admin123"),   "admin",   "Administration"),
        ("Rahul Sharma",  "BCS2020345", generate_password_hash("student123"), "student", "Computer Science"),
        ("Dr. Priya Rao", "TCH2024010", generate_password_hash("teacher123"), "teacher", "Computer Science"),
        ("Geeta Sharma",  "PAR2025001", generate_password_hash("parent123"),  "parent",  "General"),
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO users (name,college_id,password,role,department) VALUES (?,?,?,?,?)",
        users
    )

    # Seed events
    events = [
        ("Annual Tech Fest",      "Inter-college technology competition", "2026-07-15", 1),
        ("Parent-Teacher Meeting", "Quarterly progress discussion",       "2026-06-25", 1),
        ("Sports Day",            "Annual sports tournament",             "2026-07-10", 1),
    ]
    cursor.executemany(
        "INSERT INTO events (title,description,event_date,created_by) VALUES (?,?,?,?)",
        events
    )

    # Seed notifications
    notifications = [
        (2, "Welcome to SAIFS! Explore your student dashboard.",      "info"),
        (2, "New notes uploaded for Computer Science.",               "success"),
        (3, "New doubt submitted in Computer Science.",               "warning"),
        (1, "System initialized successfully.",                       "success"),
    ]
    cursor.executemany(
        "INSERT INTO notifications (user_id,message,type) VALUES (?,?,?)",
        notifications
    )

    conn.commit()
    print("Demo data seeded successfully.")


def main():
    is_new_db = not os.path.exists(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    if is_new_db:
        print("Creating fresh database from schema.sql...")
        with open(SCHEMA_PATH, "r") as f:
            schema = f.read()
            # Remove the broken seed INSERT from schema (we handle it here)
            lines = [l for l in schema.split('\n')
                     if not l.strip().startswith('INSERT')]
            conn.executescript('\n'.join(lines))
        print("Schema created.")
    else:
        print("Existing database detected – running migrations...")
        migrate_existing_db(conn)

    seed_demo_data(conn)
    conn.close()
    print("\nDatabase ready at:", DB_PATH)
    print("Demo Accounts (College ID / Password):")
    print("  ADM2026001 / admin123")
    print("  BCS2020345 / student123")
    print("  TCH2024010 / teacher123")
    print("  PAR2025001 / parent123")


if __name__ == "__main__":
    main()