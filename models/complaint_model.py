from utils.db_connection import get_db_connection


class ComplaintModel:

    @staticmethod
    def add_complaint(
        title,
        description
    ):

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO complaints
            (
                title,
                description
            )
            VALUES (?,?)
            """,
            (
                title,
                description
            )
        )

        conn.commit()
        conn.close()

    @staticmethod
    def get_all_complaints():

        conn = get_db_connection()

        complaints = conn.execute(
            """
            SELECT * FROM complaints
            ORDER BY id DESC
            """
        ).fetchall()

        conn.close()

        return complaints

    @staticmethod
    def update_status(
        complaint_id,
        status
    ):

        conn = get_db_connection()

        conn.execute(
            """
            UPDATE complaints
            SET status=?
            WHERE id=?
            """,
            (
                status,
                complaint_id
            )
        )

        conn.commit()
        conn.close()