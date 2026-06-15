"""
SAIFS - Authentication Routes
Handles login, signup, and logout.
"""
from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from utils.db_connection import get_db_connection, safe_write

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def home():
    if "user_id" in session:
        role = session.get("role", "")
        return redirect(f"/{role}/dashboard")
    return redirect("/login")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("auth.home"))

    if request.method == "POST":
        college_id = request.form.get("college_id", "").strip()
        password = request.form.get("password", "")

        if not college_id or not password:
            flash("Please fill in all fields.", "danger")
            return render_template("auth/login.html")

        user = None
        conn = get_db_connection()
        try:
            user = conn.execute(
                "SELECT * FROM users WHERE college_id = ?", (college_id,)
            ).fetchone()
        finally:
            conn.close()   # ALWAYS closed even if error

        if user and check_password_hash(user["password"], password):
            session["user_id"]         = user["id"]
            session["role"]            = user["role"]
            session["user_name"]       = user["name"]
            session["user_college_id"] = user["college_id"]

            role_redirects = {
                "student": "/student/dashboard",
                "teacher": "/teacher/dashboard",
                "parent":  "/parent/dashboard",
                "admin":   "/admin/dashboard",
            }
            flash(f"Welcome back, {user['name']}! 👋", "success")
            return redirect(role_redirects.get(user["role"], "/login"))

        flash("Invalid College ID or password. Please try again.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if "user_id" in session:
        return redirect(url_for("auth.home"))

    if request.method == "POST":
        name       = request.form.get("name", "").strip()
        college_id = request.form.get("college_id", "").strip()
        password   = request.form.get("password", "")
        role       = request.form.get("role", "student")
        dept       = request.form.get("department", "General").strip()

        if not all([name, college_id, password]):
            flash("All fields are required.", "danger")
            return render_template("auth/signup.html")

        hashed = generate_password_hash(password)

        try:
            # Pass None for email → stored as SQL NULL
            # SQLite UNIQUE allows multiple NULLs, so this never conflicts
            safe_write(
                "INSERT INTO users (name, college_id, email, password, role, department) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (name, college_id, None, hashed, role, dept)
            )
            flash("Account created successfully! Please log in.", "success")
            return redirect("/login")

        except Exception as e:
            err = str(e).lower()
            if "unique" in err and "college_id" in err:
                flash("College ID already registered. Please use a different College ID.", "danger")
            else:
                flash(f"Account creation failed: {e}", "danger")

    return render_template("auth/signup.html")


@auth_bp.route("/logout")
def logout():
    name = session.get("user_name", "")
    session.clear()
    flash(f"Goodbye, {name}! You have been logged out.", "info")
    return redirect("/login")