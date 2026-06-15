"""
Assign College IDs to users that have NULL college_id.
Generates IDs like STU0000001 based on user id.
"""
import sqlite3

DB_PATH = "database/db.sqlite3"
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

users_needing_id = cursor.execute(
    "SELECT id, name, role FROM users WHERE college_id IS NULL OR college_id = ''"
).fetchall()

for u in users_needing_id:
    # Generate a College ID: first 3 chars of role (uppercased) + user id padded to 7 digits
    role_prefix = (u["role"] or "USR")[:3].upper()
    generated_id = f"{role_prefix}{u['id']:07d}"
    cursor.execute(
        "UPDATE users SET college_id=? WHERE id=?",
        (generated_id, u["id"])
    )
    print(f"  User '{u['name']}' (id={u['id']}) -> college_id={generated_id}")

conn.commit()

print("\nAll users after update:")
rows = cursor.execute("SELECT id, name, college_id, role FROM users").fetchall()
for r in rows:
    print(f"  {dict(r)}")

conn.close()
print("\nDone.")
