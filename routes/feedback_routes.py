"""
SAIFS - Feedback Routes
Submit, view, and manage feedback.
"""
from flask import Blueprint, render_template, request, redirect, flash, session
from utils.db_connection import get_db_connection

feedback_bp = Blueprint("feedback", __name__, url_prefix="/feedback")


@feedback_bp.route("/", methods=["GET", "POST"])
def feedback():
    conn = get_db_connection()

    if request.method == "POST":
        teacher_name = request.form.get("teacher_name", "").strip()
        subject      = request.form.get("subject", "").strip()
        rating       = request.form.get("rating", "3")
        comments     = request.form.get("comments", "").strip()
        is_anonymous = 1 if request.form.get("is_anonymous") else 0
        student_id   = session.get("user_id")

        if not teacher_name or not subject:
            flash("Teacher name and subject are required.", "danger")
        else:
            conn.execute(
                "INSERT INTO feedback (student_id,teacher_name,subject,rating,comments,is_anonymous) VALUES (?,?,?,?,?,?)",
                (student_id, teacher_name, subject, int(rating), comments, is_anonymous)
            )
            conn.commit()
            flash("Feedback submitted successfully! Thank you. 🌟", "success")
            conn.close()
            return redirect("/feedback")

    feedbacks = conn.execute(
        "SELECT f.*, u.name as student_name FROM feedback f LEFT JOIN users u ON f.student_id=u.id ORDER BY f.created_at DESC"
    ).fetchall()

    # Teachers list for dropdown
    teachers = conn.execute(
        "SELECT name FROM users WHERE role='teacher' ORDER BY name"
    ).fetchall()

    conn.close()
    return render_template("features/feedback.html", feedbacks=feedbacks, teachers=teachers)


@feedback_bp.route("/delete/<int:fid>", methods=["POST"])
def delete_feedback(fid):
    conn = get_db_connection()
    conn.execute("DELETE FROM feedback WHERE id=?", (fid,))
    conn.commit()
    conn.close()
    flash("Feedback deleted.", "info")
    return redirect("/feedback")