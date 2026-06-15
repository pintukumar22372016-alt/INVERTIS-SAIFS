"""
SAIFS - Notifications Routes
Notification center, mark as read.
"""
from flask import Blueprint, render_template, redirect, jsonify, session
from utils.auth_utils import login_required
from utils.db_connection import get_db_connection

notifications_bp = Blueprint("notifications", __name__, url_prefix="/notifications")


@notifications_bp.route("/")
@login_required
def notifications():
    user_id = session.get("user_id")
    conn = get_db_connection()
    notifs = conn.execute(
        "SELECT * FROM notifications WHERE user_id=? ORDER BY created_at DESC",
        (user_id,)
    ).fetchall()

    # Mark all as read when visiting notification center
    conn.execute(
        "UPDATE notifications SET is_read=1 WHERE user_id=?", (user_id,)
    )
    conn.commit()
    conn.close()

    return render_template("features/notifications.html", notifications=notifs)


@notifications_bp.route("/mark-read/<int:notif_id>", methods=["POST"])
@login_required
def mark_read(notif_id):
    user_id = session.get("user_id")
    conn = get_db_connection()
    conn.execute(
        "UPDATE notifications SET is_read=1 WHERE id=? AND user_id=?",
        (notif_id, user_id)
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})


@notifications_bp.route("/mark-all-read", methods=["POST"])
@login_required
def mark_all_read():
    user_id = session.get("user_id")
    conn = get_db_connection()
    conn.execute("UPDATE notifications SET is_read=1 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()
    return redirect("/notifications")
