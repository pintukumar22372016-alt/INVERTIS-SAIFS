"""
One-time migration: add college_id column to existing users table
and backfill demo accounts.
"""
import sqlite3

DB_PATH = "database/db.sqlite3"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Step 1: Add the column (no UNIQUE on ALTER TABLE in SQLite with existing rows)
try:
    cursor.execute("ALTER TABLE users ADD COLUMN college_id TEXT")
    print("Added college_id column.")
except sqlite3.OperationalError as e:
    print(f"Column step: {e}")

# Step 2: Backfill existing demo users by role (one per role)
updates = [
    ("ADM2026001", "admin"),
    ("BCS2020345", "student"),
    ("TCH2024010", "teacher"),
    ("PAR2025001", "parent"),
]
for cid, role in updates:
    cursor.execute(
        "UPDATE users SET college_id=? WHERE role=? AND (college_id IS NULL OR college_id='')",
        (cid, role)
    )
    print(f"Backfilled {role} -> {cid} ({cursor.rowcount} rows updated)")

conn.commit()

# Step 3: Create unique index (works after backfill ensures no NULLs/duplicates)
try:
    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_college_id ON users(college_id)")
    print("Unique index created on college_id.")
except sqlite3.OperationalError as e:
    print(f"Index step: {e}")

conn.commit()

# Step 4: Verify
print("\nCurrent users:")
rows = cursor.execute("SELECT id, name, college_id, email, role FROM users").fetchall()
for r in rows:
    print(dict(r))

conn.close()
print("\nMigration complete.")
