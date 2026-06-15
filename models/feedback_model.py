from utils.db_connection import get_db_connection


class FeedbackModel:

    @staticmethod
    def add_feedback(
        teacher_name,
        subject,
        rating,
        comments
    ):

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO feedback
            (
                teacher_name,
                subject,
                rating,
                comments
            )
            VALUES (?,?,?,?)
            """,
            (
                teacher_name,
                subject,
                rating,
                comments
            )
        )

        conn.commit()
        conn.close()

    @staticmethod
    def get_all_feedback():

        conn = get_db_connection()

        feedback = conn.execute(
            """
            SELECT * FROM feedback
            ORDER BY id DESC
            """
        ).fetchall()

        conn.close()

        return feedback

    @staticmethod
    def delete_feedback(feedback_id):

        conn = get_db_connection()

        conn.execute(
            """
            DELETE FROM feedback
            WHERE id=?
            """,
            (feedback_id,)
        )

        conn.commit()
        conn.close()