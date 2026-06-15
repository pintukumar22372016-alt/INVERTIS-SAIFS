"""
SAIFS - Complaint Routes
Submit and track complaints with priority and category.
"""
from flask import Blueprint, render_template, request, redirect, flash, session
from utils.db_connection import get_db_connection

complaint_bp = Blueprint("complaint", __name__, url_prefix="/complaint")


@complaint_bp.route("/", methods=["GET", "POST"])
def complaint():
    conn = get_db_connection()

    if request.method == "POST":
        title       = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category    = request.form.get("category", "General")
        priority    = request.form.get("priority", "Medium")
        student_id  = session.get("user_id")

        if not title or not description:
            flash("Title and description are required.", "danger")
        else:
            conn.execute(
                "INSERT INTO complaints (student_id,title,description,category,priority) VALUES (?,?,?,?,?)",
                (student_id, title, description, category, priority)
            )
            conn.commit()
            flash("Complaint submitted successfully! We'll review it soon. 📋", "success")
            conn.close()
            return redirect("/complaint")

    status_filter = request.args.get("status", "")
    if status_filter:
        complaints = conn.execute(
            "SELECT c.*, u.name as student_name FROM complaints c LEFT JOIN users u ON c.student_id=u.id WHERE c.status=? ORDER BY c.created_at DESC",
            (status_filter,)
        ).fetchall()
    else:
        complaints = conn.execute(
            "SELECT c.*, u.name as student_name FROM complaints c LEFT JOIN users u ON c.student_id=u.id ORDER BY c.created_at DESC"
        ).fetchall()

    conn.close()
    return render_template("features/complaint.html", complaints=complaints, filter=status_filter)