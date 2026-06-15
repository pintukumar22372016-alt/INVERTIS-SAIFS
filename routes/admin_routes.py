"""
SAIFS - Admin Routes
Admin dashboard, user management, complaint resolution.
"""
from flask import Blueprint, render_template, request, redirect, flash, session
from utils.auth_utils import login_required
from utils.db_connection import get_db_connection

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    conn = get_db_connection()

    total_users    = conn.execute("SELECT COUNT(*) AS total FROM users").fetchone()["total"]
    total_students = conn.execute("SELECT COUNT(*) AS total FROM users WHERE role='student'").fetchone()["total"]
    total_teachers = conn.execute("SELECT COUNT(*) AS total FROM users WHERE role='teacher'").fetchone()["total"]
    total_parents  = conn.execute("SELECT COUNT(*) AS total FROM users WHERE role='parent'").fetchone()["total"]

    total_feedback   = conn.execute("SELECT COUNT(*) AS total FROM feedback").fetchone()["total"]
    total_complaints = conn.execute("SELECT COUNT(*) AS total FROM complaints").fetchone()["total"]
    total_doubts     = conn.execute("SELECT COUNT(*) AS total FROM doubts").fetchone()["total"]
    total_notes      = conn.execute("SELECT COUNT(*) AS total FROM notes").fetchone()["total"]

    avg_rating = conn.execute("SELECT ROUND(AVG(rating),1) AS avg FROM feedback").fetchone()["avg"] or 0

    pending_complaints  = conn.execute("SELECT COUNT(*) AS total FROM complaints WHERE status='Pending'").fetchone()["total"]
    resolved_complaints = conn.execute("SELECT COUNT(*) AS total FROM complaints WHERE status='Resolved'").fetchone()["total"]

    # Rating distribution for doughnut chart
    rating_dist = conn.execute(
        "SELECT rating, COUNT(*) as cnt FROM feedback GROUP BY rating ORDER BY rating"
    ).fetchall()
    rating_data = {str(i): 0 for i in range(1, 6)}
    for row in rating_dist:
        rating_data[str(row["rating"])] = row["cnt"]

    # Complaint category breakdown
    cat_dist = conn.execute(
        "SELECT category, COUNT(*) as cnt FROM complaints GROUP BY category ORDER BY cnt DESC"
    ).fetchall()

    # Recent users
    recent_users = conn.execute(
        "SELECT * FROM users ORDER BY created_at DESC LIMIT 10"
    ).fetchall()

    # All users for management panel
    all_users = conn.execute(
        "SELECT * FROM users ORDER BY role, name"
    ).fetchall()

    conn.close()

    return render_template(
        "dashboards/admin_dashboard.html",
        total_users=total_users,
        total_students=total_students,
        total_teachers=total_teachers,
        total_parents=total_parents,
        total_feedback=total_feedback,
        total_complaints=total_complaints,
        total_doubts=total_doubts,
        total_notes=total_notes,
        avg_rating=avg_rating,
        pending_complaints=pending_complaints,
        resolved_complaints=resolved_complaints,
        rating_data=rating_data,
        cat_dist=cat_dist,
        recent_users=recent_users,
        all_users=all_users,
    )


@admin_bp.route("/users/delete/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    flash("User deleted successfully.", "success")
    return redirect("/admin/dashboard")


@admin_bp.route("/complaints")
@login_required
def admin_complaints():
    conn = get_db_connection()
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
    return render_template("features/complaint.html", complaints=complaints, view="admin", filter=status_filter)


@admin_bp.route("/complaints/resolve/<int:complaint_id>", methods=["POST"])
@login_required
def resolve_complaint(complaint_id):
    resolution = request.form.get("resolution", "Resolved by admin.")
    conn = get_db_connection()
    conn.execute(
        "UPDATE complaints SET status='Resolved', resolution=?, resolved_by=?, resolved_at=datetime('now','localtime') WHERE id=?",
        (resolution, session.get("user_id"), complaint_id)
    )
    conn.commit()
    conn.close()
    flash("Complaint resolved successfully! ✅", "success")
    return redirect("/admin/complaints")


@admin_bp.route("/analytics")
@login_required
def admin_analytics():
    from services.analytics_service import AnalyticsService
    data = AnalyticsService.dashboard_data()
    return render_template("features/analytics.html", **data)