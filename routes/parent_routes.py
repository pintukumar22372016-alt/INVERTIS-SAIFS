"""
SAIFS - Parent Routes
Parent dashboard, student progress, feedback view.
"""
from flask import Blueprint, render_template
from utils.auth_utils import login_required
from utils.db_connection import get_db_connection

parent_bp = Blueprint("parent", __name__, url_prefix="/parent")


@parent_bp.route("/dashboard")
@login_required
def dashboard():
    conn = get_db_connection()

    total_feedback   = conn.execute("SELECT COUNT(*) as total FROM feedback").fetchone()["total"]
    total_complaints = conn.execute("SELECT COUNT(*) as total FROM complaints").fetchone()["total"]
    total_notes      = conn.execute("SELECT COUNT(*) as total FROM notes").fetchone()["total"]

    avg_rating = conn.execute("SELECT ROUND(AVG(rating),1) AS avg FROM feedback").fetchone()["avg"] or 0

    # Attendance overview (all students for parent view)
    attendance_total   = conn.execute("SELECT COUNT(*) as total FROM attendance").fetchone()["total"]
    attendance_present = conn.execute("SELECT COUNT(*) as total FROM attendance WHERE status='Present'").fetchone()["total"]
    attendance_pct = round((attendance_present / attendance_total * 100) if attendance_total else 0)

    # Recent feedback list
    recent_feedback = conn.execute(
        "SELECT * FROM feedback ORDER BY created_at DESC LIMIT 5"
    ).fetchall()

    # Recent complaints
    recent_complaints = conn.execute(
        "SELECT * FROM complaints ORDER BY created_at DESC LIMIT 5"
    ).fetchall()

    # Upcoming events
    events = conn.execute(
        "SELECT * FROM events WHERE event_date >= date('now','localtime') ORDER BY event_date ASC LIMIT 5"
    ).fetchall()

    conn.close()

    return render_template(
        "dashboards/parent_dashboard.html",
        total_feedback=total_feedback,
        total_complaints=total_complaints,
        total_notes=total_notes,
        avg_rating=avg_rating,
        attendance_pct=attendance_pct,
        attendance_total=attendance_total,
        attendance_present=attendance_present,
        recent_feedback=recent_feedback,
        recent_complaints=recent_complaints,
        events=events,
    )


@parent_bp.route("/student-progress")
@login_required
def student_progress():
    conn = get_db_connection()
    attendance = conn.execute(
        "SELECT * FROM attendance ORDER BY date DESC"
    ).fetchall()
    conn.close()
    return render_template("features/attendance.html", attendance=attendance, view="parent")


@parent_bp.route("/feedback")
@login_required
def parent_feedback():
    conn = get_db_connection()
    feedbacks = conn.execute(
        "SELECT * FROM feedback ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return render_template("features/feedback.html", feedbacks=feedbacks, view="parent")