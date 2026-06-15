"""
SAIFS - Doubt Routes
Ask doubts, view answers, threaded replies.
"""
from flask import Blueprint, render_template, request, redirect, flash, session
from utils.db_connection import get_db_connection

doubt_bp = Blueprint("doubt", __name__, url_prefix="/doubts")


@doubt_bp.route("/", methods=["GET", "POST"])
def doubts():
    conn = get_db_connection()

    if request.method == "POST":
        subject  = request.form.get("subject", "").strip()
        question = request.form.get("question", "").strip()
        asked_by = session.get("user_id")

        if not subject or not question:
            flash("Subject and question are required.", "danger")
        else:
            conn.execute(
                "INSERT INTO doubts (subject,question,asked_by) VALUES (?,?,?)",
                (subject, question, asked_by)
            )
            conn.commit()
            flash("Doubt submitted! A teacher will respond soon. 🎓", "success")
            conn.close()
            return redirect("/doubts")

    subject_filter = request.args.get("subject", "")
    status_filter  = request.args.get("status", "")
    search         = request.args.get("search", "")

    query = """
        SELECT d.*, u.name as student_name, t.name as teacher_name
        FROM doubts d
        LEFT JOIN users u ON d.asked_by=u.id
        LEFT JOIN users t ON d.answered_by=t.id
    """
    conditions = []
    params = []

    if subject_filter:
        conditions.append("d.subject LIKE ?")
        params.append(f"%{subject_filter}%")
    if status_filter:
        conditions.append("d.status=?")
        params.append(status_filter)
    if search:
        conditions.append("(d.subject LIKE ? OR d.question LIKE ?)")
        params.extend([f"%{search}%", f"%{search}%"])

    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY d.asked_at DESC"

    doubts_list = conn.execute(query, params).fetchall()
    subjects = conn.execute("SELECT DISTINCT subject FROM doubts ORDER BY subject").fetchall()
    conn.close()

    return render_template(
        "features/doubts.html",
        doubts=doubts_list,
        subjects=subjects,
        filter=subject_filter,
        status_filter=status_filter,
        search=search,
    )


@doubt_bp.route("/answer/<int:doubt_id>", methods=["POST"])
def answer_doubt(doubt_id):
    answer = request.form.get("answer", "").strip()
    if answer:
        conn = get_db_connection()
        conn.execute(
            "UPDATE doubts SET answer=?, status='Answered', answered_by=?, answered_at=datetime('now','localtime') WHERE id=?",
            (answer, session.get("user_id"), doubt_id)
        )
        conn.commit()
        conn.close()
        flash("Answer submitted successfully! ✅", "success")
    return redirect("/doubts")