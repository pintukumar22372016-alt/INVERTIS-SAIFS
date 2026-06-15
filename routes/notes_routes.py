"""
SAIFS - Notes Routes
Upload, list, download notes.
"""
from flask import Blueprint, render_template, request, redirect, flash, session, send_from_directory, current_app
from werkzeug.utils import secure_filename
from utils.db_connection import get_db_connection
import os

notes_bp = Blueprint("notes", __name__, url_prefix="/notes")

ALLOWED = {"pdf", "doc", "docx", "ppt", "pptx", "txt", "zip"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED


@notes_bp.route("/", methods=["GET", "POST"])
def notes():
    conn = get_db_connection()

    if request.method == "POST":
        subject     = request.form.get("subject", "").strip()
        description = request.form.get("description", "").strip()
        file        = request.files.get("notes")

        if not subject:
            flash("Subject is required.", "danger")
        elif not file or not file.filename:
            flash("Please select a file to upload.", "danger")
        elif not allowed_file(file.filename):
            flash("Invalid file type. Allowed: PDF, DOC, DOCX, PPT, PPTX, TXT, ZIP", "danger")
        else:
            filename = secure_filename(file.filename)
            upload_path = current_app.config["UPLOAD_FOLDER"]
            os.makedirs(upload_path, exist_ok=True)
            file.save(os.path.join(upload_path, filename))

            conn.execute(
                "INSERT INTO notes (subject,file_name,description,uploaded_by) VALUES (?,?,?,?)",
                (subject, filename, description, session.get("user_id"))
            )
            conn.commit()
            flash("Notes uploaded successfully! 📚", "success")
            conn.close()
            return redirect("/notes")

    subject_filter = request.args.get("subject", "")
    search = request.args.get("search", "")

    query = "SELECT n.*, u.name as uploader FROM notes n LEFT JOIN users u ON n.uploaded_by=u.id"
    params = []

    conditions = []
    if subject_filter:
        conditions.append("n.subject LIKE ?")
        params.append(f"%{subject_filter}%")
    if search:
        conditions.append("(n.subject LIKE ? OR n.file_name LIKE ? OR n.description LIKE ?)")
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY n.uploaded_at DESC"
    notes_list = conn.execute(query, params).fetchall()
    subjects = conn.execute("SELECT DISTINCT subject FROM notes ORDER BY subject").fetchall()
    conn.close()

    return render_template(
        "features/notes.html",
        notes=notes_list,
        subjects=subjects,
        filter=subject_filter,
        search=search
    )


@notes_bp.route("/download/<filename>")
def download_note(filename):
    upload_path = current_app.config["UPLOAD_FOLDER"]
    return send_from_directory(upload_path, filename, as_attachment=True)


@notes_bp.route("/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    conn = get_db_connection()
    note = conn.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
    if note:
        try:
            path = os.path.join(current_app.config["UPLOAD_FOLDER"], note["file_name"])
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass
        conn.execute("DELETE FROM notes WHERE id=?", (note_id,))
        conn.commit()
        flash("Note deleted.", "info")
    conn.close()
    return redirect("/notes")