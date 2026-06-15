-- ============================================================
-- SAIFS - Smart Academic Interaction & Feedback System
-- Enhanced Database Schema v2.0
-- ============================================================

PRAGMA foreign_keys = ON;

-- ============================================================
-- USERS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    college_id  TEXT    UNIQUE NOT NULL,
    email       TEXT    UNIQUE,
    password    TEXT    NOT NULL,
    role        TEXT    NOT NULL CHECK(role IN ('student','teacher','admin','parent')),
    department  TEXT    DEFAULT 'General',
    phone       TEXT    DEFAULT '',
    profile_pic TEXT    DEFAULT '',
    created_at  TIMESTAMP DEFAULT (datetime('now','localtime'))
);

-- ============================================================
-- FEEDBACK TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS feedback (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id   INTEGER REFERENCES users(id) ON DELETE SET NULL,
    teacher_name TEXT    NOT NULL,
    subject      TEXT    NOT NULL,
    rating       INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
    comments     TEXT    DEFAULT '',
    is_anonymous INTEGER DEFAULT 0,
    created_at   TIMESTAMP DEFAULT (datetime('now','localtime'))
);

-- ============================================================
-- COMPLAINTS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS complaints (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id  INTEGER REFERENCES users(id) ON DELETE SET NULL,
    title       TEXT    NOT NULL,
    description TEXT    NOT NULL,
    category    TEXT    DEFAULT 'General'
                        CHECK(category IN ('Academic','Infrastructure','Faculty','Administration','Hostel','Other','General')),
    priority    TEXT    DEFAULT 'Medium'
                        CHECK(priority IN ('Low','Medium','High','Critical')),
    status      TEXT    DEFAULT 'Pending'
                        CHECK(status IN ('Pending','In Review','Resolved','Closed')),
    resolved_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    resolution  TEXT    DEFAULT '',
    created_at  TIMESTAMP DEFAULT (datetime('now','localtime')),
    resolved_at TIMESTAMP
);

-- ============================================================
-- NOTES TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS notes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    subject     TEXT    NOT NULL,
    file_name   TEXT    NOT NULL,
    description TEXT    DEFAULT '',
    uploaded_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    uploaded_at TIMESTAMP DEFAULT (datetime('now','localtime'))
);

-- ============================================================
-- DOUBTS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS doubts (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    subject     TEXT    NOT NULL,
    question    TEXT    NOT NULL,
    answer      TEXT    DEFAULT '',
    asked_by    INTEGER REFERENCES users(id) ON DELETE SET NULL,
    answered_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    status      TEXT    DEFAULT 'Open' CHECK(status IN ('Open','Answered','Closed')),
    asked_at    TIMESTAMP DEFAULT (datetime('now','localtime')),
    answered_at TIMESTAMP
);

-- ============================================================
-- ATTENDANCE TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS attendance (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name  TEXT    NOT NULL,
    student_id    INTEGER REFERENCES users(id) ON DELETE SET NULL,
    subject       TEXT    NOT NULL,
    status        TEXT    NOT NULL CHECK(status IN ('Present','Absent','Late')),
    date          DATE    DEFAULT (date('now','localtime')),
    recorded_by   INTEGER REFERENCES users(id) ON DELETE SET NULL
);

-- ============================================================
-- NOTIFICATIONS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS notifications (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER REFERENCES users(id) ON DELETE CASCADE,
    message    TEXT    NOT NULL,
    type       TEXT    DEFAULT 'info' CHECK(type IN ('info','success','warning','danger')),
    is_read    INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT (datetime('now','localtime'))
);

-- ============================================================
-- EVENTS TABLE (new)
-- ============================================================
CREATE TABLE IF NOT EXISTS events (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    description TEXT    DEFAULT '',
    event_date  DATE    NOT NULL,
    created_by  INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at  TIMESTAMP DEFAULT (datetime('now','localtime'))
);

-- ============================================================
-- DOUBT REPLIES TABLE (new - threaded discussions)
-- ============================================================
CREATE TABLE IF NOT EXISTS doubt_replies (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    doubt_id   INTEGER NOT NULL REFERENCES doubts(id) ON DELETE CASCADE,
    replied_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    reply      TEXT    NOT NULL,
    created_at TIMESTAMP DEFAULT (datetime('now','localtime'))
);

-- ============================================================
-- SEED DATA - Demo Admin Account
-- ============================================================
INSERT OR IGNORE INTO users (name, college_id, password, role, department)
VALUES (
    'Admin',
    'ADM2026001',
    'pbkdf2:sha256:600000$saifs2026$hashedpassword',
    'admin',
    'Administration'
);