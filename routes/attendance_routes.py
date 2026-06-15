"""
SAIFS - Attendance Routes
Attendance recording, listing, and reports.
"""
from flask import Blueprint, render_template, request, redirect, flash, session
from utils.auth_utils import login_required
from utils.db_connection import get_db_connection

attendance_bp = Blueprint("attendance", __name__, url_prefix="/attendance")


@attendance_bp.route("/", methods=["GET", "POST"])
@login_required
def attendance():
    conn = get_db_connection()

    if request.method == "POST":
        student_name = request.form.get("student_name", "").strip()
        subject      = request.form.get("subject", "").strip()
        status       = request.form.get("status", "Present")
        date         = request.form.get("date", "")
        recorded_by  = session.get("user_id")

        if not student_name or not subject:
            flash("Student name and subject are required.", "danger")
        else:
            conn.execute(
                "INSERT INTO attendance (student_name,subject,status,date,recorded_by) VALUES (?,?,?,?,?)",
                (student_name, subject, status, date or None, recorded_by)
            )
            conn.commit()
            flash("Attendance recorded successfully! ✅", "success")
            conn.close()
            return redirect("/attendance")

    # Filters
    subject_filter = request.args.get("subject", "")
    status_filter  = request.args.get("status", "")
    date_filter    = request.args.get("date", "")

    query = "SELECT a.*, u.name as recorder FROM attendance a LEFT JOIN users u ON a.recorded_by=u.id"
    conditions, params = [], []

    if subject_filter:
        conditions.append("a.subject LIKE ?")
        params.append(f"%{subject_filter}%")
    if status_filter:
        conditions.append("a.status=?")
        params.append(status_filter)
    if date_filter:
        conditions.append("a.date=?")
        params.append(date_filter)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY a.date DESC, a.id DESC"

    attendance_list = conn.execute(query, params).fetchall()

    # Summary stats
    total   = len(attendance_list)
    present = sum(1 for a in attendance_list if a["status"] == "Present")
    absent  = sum(1 for a in attendance_list if a["status"] == "Absent")
    late    = sum(1 for a in attendance_list if a["status"] == "Late")

    subjects = conn.execute("SELECT DISTINCT subject FROM attendance ORDER BY subject").fetchall()
    conn.close()

    return render_template(
        "features/attendance.html",
        attendance=attendance_list,
        subjects=subjects,
        total=total,
        present=present,
        absent=absent,
        late=late,
        filter_subject=subject_filter,
        filter_status=status_filter,
        filter_date=date_filter,
    )
