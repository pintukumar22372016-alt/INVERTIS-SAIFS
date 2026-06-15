"""
SAIFS - Analytics Service
Rich analytics data for dashboards and charts.
"""
from utils.db_connection import get_db_connection


class AnalyticsService:

    @staticmethod
    def dashboard_data():
        conn = get_db_connection()

        total_students  = conn.execute("SELECT COUNT(*) FROM users WHERE role='student'").fetchone()[0]
        total_teachers  = conn.execute("SELECT COUNT(*) FROM users WHERE role='teacher'").fetchone()[0]
        total_parents   = conn.execute("SELECT COUNT(*) FROM users WHERE role='parent'").fetchone()[0]
        total_users     = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        total_feedback  = conn.execute("SELECT COUNT(*) FROM feedback").fetchone()[0]
        total_complaints = conn.execute("SELECT COUNT(*) FROM complaints").fetchone()[0]
        total_notes     = conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
        total_doubts    = conn.execute("SELECT COUNT(*) FROM doubts").fetchone()[0]

        avg_rating_raw  = conn.execute("SELECT AVG(rating) FROM feedback").fetchone()[0]
        avg_rating      = round(avg_rating_raw, 2) if avg_rating_raw else 0

        # Rating distribution 1–5
        rating_rows = conn.execute(
            "SELECT rating, COUNT(*) as cnt FROM feedback GROUP BY rating ORDER BY rating"
        ).fetchall()
        rating_dist = {str(i): 0 for i in range(1, 6)}
        for row in rating_rows:
            rating_dist[str(row["rating"])] = row["cnt"]

        # Complaint status breakdown
        status_rows = conn.execute(
            "SELECT status, COUNT(*) as cnt FROM complaints GROUP BY status"
        ).fetchall()
        complaint_status = {"Pending": 0, "In Review": 0, "Resolved": 0, "Closed": 0}
        for row in status_rows:
            complaint_status[row["status"]] = row["cnt"]

        # Complaint category breakdown
        cat_rows = conn.execute(
            "SELECT category, COUNT(*) as cnt FROM complaints GROUP BY category ORDER BY cnt DESC"
        ).fetchall()
        complaint_categories = {row["category"]: row["cnt"] for row in cat_rows}

        # Teacher-wise feedback avg
        teacher_rows = conn.execute(
            "SELECT teacher_name, ROUND(AVG(rating),1) as avg_rating, COUNT(*) as cnt FROM feedback GROUP BY teacher_name ORDER BY avg_rating DESC"
        ).fetchall()
        teacher_feedback = [dict(row) for row in teacher_rows]

        # Monthly feedback trend (last 6 months)
        monthly_rows = conn.execute("""
            SELECT strftime('%Y-%m', created_at) as month, COUNT(*) as cnt
            FROM feedback
            WHERE created_at >= date('now','-6 months','localtime')
            GROUP BY month
            ORDER BY month ASC
        """).fetchall()
        monthly_feedback = {"labels": [], "data": []}
        for row in monthly_rows:
            monthly_feedback["labels"].append(row["month"])
            monthly_feedback["data"].append(row["cnt"])

        # Attendance overview
        att_total   = conn.execute("SELECT COUNT(*) FROM attendance").fetchone()[0]
        att_present = conn.execute("SELECT COUNT(*) FROM attendance WHERE status='Present'").fetchone()[0]
        att_absent  = conn.execute("SELECT COUNT(*) FROM attendance WHERE status='Absent'").fetchone()[0]
        att_late    = conn.execute("SELECT COUNT(*) FROM attendance WHERE status='Late'").fetchone()[0]

        conn.close()

        return {
            "total_students":       total_students,
            "total_teachers":       total_teachers,
            "total_parents":        total_parents,
            "total_users":          total_users,
            "total_feedback":       total_feedback,
            "total_complaints":     total_complaints,
            "total_notes":          total_notes,
            "total_doubts":         total_doubts,
            "avg_rating":           avg_rating,
            "rating_dist":          rating_dist,
            "complaint_status":     complaint_status,
            "complaint_categories": complaint_categories,
            "teacher_feedback":     teacher_feedback,
            "monthly_feedback":     monthly_feedback,
            "att_total":            att_total,
            "att_present":          att_present,
            "att_absent":           att_absent,
            "att_late":             att_late,
        }

    @staticmethod
    def average_rating():
        conn = get_db_connection()
        result = conn.execute("SELECT AVG(rating) FROM feedback").fetchone()[0]
        conn.close()
        return round(result, 2) if result else 0