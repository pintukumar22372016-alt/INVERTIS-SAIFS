"""
SAIFS - Main Application Entry Point
Smart Academic Interaction & Feedback System
"""
from flask import Flask, render_template, session, redirect, g
from config import Config

#  Blueprints 
from routes.auth_routes       import auth_bp
from routes.student_routes    import student_bp
from routes.teacher_routes    import teacher_bp
from routes.admin_routes      import admin_bp
from routes.parent_routes     import parent_bp
from routes.feedback_routes   import feedback_bp
from routes.complaint_routes  import complaint_bp
from routes.notes_routes      import notes_bp
from routes.doubt_routes      import doubt_bp
from routes.chatbot_routes    import chatbot_bp
from routes.analytics_routes  import analytics_bp
from routes.notifications_routes import notifications_bp
from routes.attendance_routes import attendance_bp

from utils.db_connection import get_db_connection
import os

app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload directory exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(teacher_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(parent_bp)
app.register_blueprint(feedback_bp)
app.register_blueprint(complaint_bp)
app.register_blueprint(notes_bp)
app.register_blueprint(doubt_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(notifications_bp)
app.register_blueprint(attendance_bp)


# ── DB connection management (one per request, auto-closed) ──
def get_db():
    """Get or create a DB connection stored in Flask's g for this request."""
    if "db" not in g:
        g.db = get_db_connection()
    return g.db


@app.teardown_appcontext
def close_db(error=None):
    """Automatically close DB connection at end of every request."""
    db = g.pop("db", None)
    if db is not None:
        try:
            db.close()
        except Exception:
            pass


# Context Processor 
@app.context_processor
def inject_globals():
    """Inject common data into all templates."""
    unread_count = 0
    user_name = session.get("user_name", "")
    user_role = session.get("role", "")
    user_id   = session.get("user_id")

    if user_id:
        try:
            conn = get_db_connection()   # fresh short-lived read connection
            result = conn.execute(
                "SELECT COUNT(*) FROM notifications WHERE user_id=? AND is_read=0",
                (user_id,)
            ).fetchone()
            unread_count = result[0] if result else 0
            conn.close()                 # close immediately after read
        except Exception:
            pass

    return dict(
        unread_notifications=unread_count,
        current_user_name=user_name,
        current_user_role=user_role,
        current_user_id=user_id,
    )


# Error Handlers 
@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("errors/500.html"), 500


@app.errorhandler(403)
def forbidden(error):
    return render_template("errors/404.html"), 403

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000, threaded=True, use_reloader=False)