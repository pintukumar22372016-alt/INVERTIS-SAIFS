"""
SAIFS - Teacher Routes
Teacher dashboard, notes management, doubts management.
"""
from flask import Blueprint, render_template, request, redirect, flash, session, send_from_directory, current_app
from werkzeug.utils import secure_filename
from utils.auth_utils import login_required
from utils.db_connection import get_db_connection
import os

teacher_bp = Blueprint("teacher", __name__, url_prefix="/teacher")


@teacher_bp.route("/dashboard")
@login_required
def dashboard():
    conn = get_db_connection()

    total_notes = conn.execute("SELECT COUNT(*) as total FROM notes").fetchone()["total"]
    total_doubts = conn.execute("SELECT COUNT(*) as total FROM doubts WHERE status='Open'").fetchone()["total"]
    total_feedback = conn.execute("SELECT COUNT(*) as total FROM feedback").fetchone()["total"]

    avg_rating = conn.execute("SELECT ROUND(AVG(rating),1) as avg FROM feedback").fetchone()["avg"] or 0

    # Recent doubts
    recent_doubts = conn.execute(
        "SELECT * FROM doubts ORDER BY asked_at DESC LIMIT 5"
    ).fetchall()

    # Rating distribution for chart
    rating_dist = conn.execute(
        "SELECT rating, COUNT(*) as cnt FROM feedback GROUP BY rating ORDER BY rating"
    ).fetchall()

    rating_data = {str(i): 0 for i in range(1, 6)}
    for row in rating_dist:
        rating_data[str(row["rating"])] = row["cnt"]

    # Recent notes
    recent_notes = conn.execute(
        "SELECT * FROM notes ORDER BY uploaded_at DESC LIMIT 5"
    ).fetchall()

    conn.close()

    return render_template(
        "dashboards/teacher_dashboard.html",
        total_notes=total_notes,
        total_doubts=total_doubts,
        total_feedback=total_feedback,
        avg_rating=avg_rating,
        recent_doubts=recent_doubts,
        rating_data=rating_data,
        recent_notes=recent_notes,
    )


@teacher_bp.route("/notes", methods=["GET", "POST"])
@login_required
def teacher_notes():
    conn = get_db_connection()

    if request.method == "POST":
        subject     = request.form.get("subject", "")
        description = request.form.get("description", "")
        file        = request.files.get("notes")

        if file and file.filename:
            filename = secure_filename(file.filename)
            upload_path = current_app.config["UPLOAD_FOLDER"]
            os.makedirs(upload_path, exist_ok=True)
            file.save(os.path.join(upload_path, filename))

            conn.execute(
                "INSERT INTO notes (subject,file_name,description,uploaded_by) VALUES (?,?,?,?)",
                (subject, filename, description, session.get("user_id"))
            )
            conn.commit()
            flash("Notes uploaded successfully! ✅", "success")
        else:
            flash("Please select a file to upload.", "danger")

        conn.close()
        return redirect("/teacher/notes")

    subject_filter = request.args.get("subject", "")
    if subject_filter:
        notes = conn.execute(
            "SELECT n.*, u.name as uploader FROM notes n LEFT JOIN users u ON n.uploaded_by=u.id WHERE n.subject LIKE ? ORDER BY n.uploaded_at DESC",
            (f"%{subject_filter}%",)
        ).fetchall()
    else:
        notes = conn.execute(
            "SELECT n.*, u.name as uploader FROM notes n LEFT JOIN users u ON n.uploaded_by=u.id ORDER BY n.uploaded_at DESC"
        ).fetchall()

    subjects = conn.execute("SELECT DISTINCT subject FROM notes ORDER BY subject").fetchall()
    conn.close()

    return render_template("features/notes.html", notes=notes, subjects=subjects, filter=subject_filter)


@teacher_bp.route("/doubts")
@login_required
def teacher_doubts():
    conn = get_db_connection()
    doubts = conn.execute(
        "SELECT d.*, u.name as student_name FROM doubts d LEFT JOIN users u ON d.asked_by=u.id ORDER BY d.asked_at DESC"
    ).fetchall()
    conn.close()
    return render_template("features/doubts.html", doubts=doubts, view="teacher")


@teacher_bp.route("/doubts/answer/<int:doubt_id>", methods=["POST"])
@login_required
def answer_doubt(doubt_id):
    answer = request.form.get("answer", "")
    conn = get_db_connection()
    conn.execute(
        "UPDATE doubts SET answer=?, status='Answered', answered_by=?, answered_at=datetime('now','localtime') WHERE id=?",
        (answer, session.get("user_id"), doubt_id)
    )
    conn.commit()
    conn.close()
    flash("Doubt answered successfully!", "success")
    return redirect("/teacher/doubts")