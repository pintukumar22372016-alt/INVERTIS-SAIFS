"""
SAIFS - Student Routes
Student dashboard and related pages.
"""
from flask import Blueprint, render_template, session
from utils.auth_utils import login_required
from utils.db_connection import get_db_connection

student_bp = Blueprint("student", __name__, url_prefix="/student")


@student_bp.route("/dashboard")
@login_required
def dashboard():
    user_id = session.get("user_id")
    conn = get_db_connection()

    feedback_count = conn.execute(
        "SELECT COUNT(*) as total FROM feedback WHERE student_id=?", (user_id,)
    ).fetchone()

    complaint_count = conn.execute(
        "SELECT COUNT(*) as total FROM complaints WHERE student_id=?", (user_id,)
    ).fetchone()

    notes_count = conn.execute(
        "SELECT COUNT(*) as total FROM notes"
    ).fetchone()

    # Attendance summary
    attendance_total = conn.execute(
        "SELECT COUNT(*) as total FROM attendance WHERE student_id=?", (user_id,)
    ).fetchone()["total"]

    attendance_present = conn.execute(
        "SELECT COUNT(*) as total FROM attendance WHERE student_id=? AND status='Present'", (user_id,)
    ).fetchone()["total"]

    attendance_pct = round((attendance_present / attendance_total * 100) if attendance_total else 0)

    # Recent notifications
    notifications = conn.execute(
        "SELECT * FROM notifications WHERE user_id=? ORDER BY created_at DESC LIMIT 5", (user_id,)
    ).fetchall()

    # Upcoming events
    events = conn.execute(
        "SELECT * FROM events WHERE event_date >= date('now','localtime') ORDER BY event_date ASC LIMIT 5"
    ).fetchall()

    # Recent feedback
    recent_feedback = conn.execute(
        "SELECT * FROM feedback WHERE student_id=? ORDER BY created_at DESC LIMIT 3", (user_id,)
    ).fetchall()

    # Complaint status breakdown
    pending_complaints = conn.execute(
        "SELECT COUNT(*) as total FROM complaints WHERE student_id=? AND status='Pending'", (user_id,)
    ).fetchone()["total"]

    doubts_count = conn.execute(
        "SELECT COUNT(*) as total FROM doubts WHERE asked_by=?", (user_id,)
    ).fetchone()["total"]

    conn.close()

    return render_template(
        "dashboards/student_dashboard.html",
        feedback_count=feedback_count["total"],
        complaint_count=complaint_count["total"],
        notes_count=notes_count["total"],
        attendance_pct=attendance_pct,
        attendance_total=attendance_total,
        attendance_present=attendance_present,
        notifications=notifications,
        events=events,
        recent_feedback=recent_feedback,
        pending_complaints=pending_complaints,
        doubts_count=doubts_count,
    )